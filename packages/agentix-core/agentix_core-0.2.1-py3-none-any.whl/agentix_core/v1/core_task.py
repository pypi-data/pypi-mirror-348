import os
import aiohttp
import logging
import math
import asyncio

logger = logging.getLogger("core.task")

#===================================================================================================
class CoreTask:
    """Handles the calls to core apis."""

    def __init__(
        self, 
        task_key: str, 
        AGENT_NAME: str, 
        CORE_API: str, 
        task_data: dict = None,
    ):
        """Initialize Core Task with task key, task data, agent name, core API URL, job cookie."""

        if not task_key:
            raise ValueError("[INIT] task_key is required and cannot be empty.")
        if not AGENT_NAME:
            raise ValueError("[INIT] AGENT_NAME is required and cannot be empty.")
        if not CORE_API:
            raise ValueError("[INIT] CORE_API is required and cannot be empty.")

        self.task_key = task_key
        self.task_data = task_data
        self.CORE_API = CORE_API.rstrip("/")
        self.AGENT_NAME = AGENT_NAME
        self.JOB_COOKIE = None

    #================================================================================================
    # Connect to Core
    #================================================================================================
    async def connect(self, JOB_COOKIE: dict = None, PASSWORD: str = None) -> bool:
        """Authenticate to Core, exchange JWT for session cookie, and store it in self.JOB_COOKIE."""

        logger.info(f"🔑 Authenticating to Core API with user: {self.AGENT_NAME}")

        if not JOB_COOKIE and not PASSWORD:
            raise ValueError("[CONNECT] JOB_COOKIE or PASSWORD must be provided to connect.")

        if JOB_COOKIE:
            self.JOB_COOKIE = JOB_COOKIE
            logger.info("✅ JOB_COOKIE provided, using existing session.")
            return True

        self.PASSWORD = PASSWORD
        logger.info("🔐 Using username and password for authentication.")

        login_url = f"{self.CORE_API}/auth"
        connect_url = f"{self.CORE_API}/v1/tasks/{self.task_key}/connect"
        headers = {"Referer": self.CORE_API}

        auth_payload = {
            "identifier": self.AGENT_NAME,
            "password": self.PASSWORD
        }

        jwt_token = None
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(login_url, json=auth_payload, headers=headers) as login_response:
                        login_json = await login_response.json()
                        if login_response.status == 200 and "jwt" in login_json:
                            jwt_token = login_json["jwt"]
                            logger.info(f"✅ Login succeeded on attempt {attempt}")
                            break
                        else:
                            logger.warning(f"⚠️ Login failed on attempt {attempt}: {login_response.status} - {login_json}")
            except Exception as e:
                logger.error(f"❌ Login error on attempt {attempt}: {e}")

            if attempt < max_retries:
                logger.info("🔁 Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                raise RuntimeError("[CONNECT] ❌ Authentication failed after maximum retry attempts.")

        try:
            connect_headers = {
                "Authorization": f"Bearer {jwt_token}",
                "Referer": self.CORE_API
            }

            async with aiohttp.ClientSession() as connect_session:
                async with connect_session.post(connect_url, headers=connect_headers) as connect_response:
                    if connect_response.status != 200:
                        raise RuntimeError(f"[CONNECT] ❌ Connect failed: {connect_response.status} - {await connect_response.text()}")

                    self.JOB_COOKIE = connect_session.cookie_jar.filter_cookies(self.CORE_API)
                    logger.info("✅ JOB_COOKIE successfully stored from connect response")
                    return True

        except Exception as e:
            logger.error(f"[CONNECT] ❌ Error during connect request: {e}")
            raise

    #================================================================================================
    # Start Task in Core
    #================================================================================================
    async def start(self, reterive_agent_assignment: bool = False) -> bool:
        """Calls the Start Task API asynchronously to Start Task in Core, includes jobCookie in cookies."""

        if not self.JOB_COOKIE or not isinstance(self.JOB_COOKIE, dict):
            raise ValueError("[START] JOB_COOKIE is required and must be a non-empty dictionary.")

        try:
            logger.info(f"\n>>> Start Task: {self.task_key}")

            start_task_url = f"{self.CORE_API}/v1/tasks/{self.task_key}/start"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Starting Task from {self.AGENT_NAME}",
                    "retrieveAgentAssignment": reterive_agent_assignment
                }
            }

            async with aiohttp.ClientSession(cookies=self.JOB_COOKIE) as session:
                async with session.post(start_task_url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None

                    if response.status == 200 and response_json is not None:
                        self.task_data = response_json
                        logger.info(f"<<<<< ✅ Task Started!")
                        return True
                    else:
                        raise RuntimeError(f"[START] ❌ Failed to start task. HTTP Status: {response.status} - {response_json}")

        except Exception as e:
            self.task_data = None
            logger.error(f"[START] ❌ Error calling Start Task API: {e}")
            raise

    #================================================================================================
    # Submit Task in Core
    #================================================================================================
    async def submit(self):
        """Calls the Submit Task API asynchronously to Submit Task, includes jobCookie in cookies."""

        if not self.JOB_COOKIE or not isinstance(self.JOB_COOKIE, dict):
            raise ValueError("[SUBMIT] JOB_COOKIE is required and must be a non-empty dictionary.")

        try:
            logger.info(f">>> Submit Task: {self.task_key}")

            url = f"{self.CORE_API}/v1/tasks/{self.task_key}/submit"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Submitting Task from {self.AGENT_NAME} - Automated Task Completed"
                }
            }

            async with aiohttp.ClientSession(cookies=self.JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    if response.status != 200:
                        raise RuntimeError(f"[SUBMIT] ❌ Failed to submit task. HTTP Status: {response.status} - {response_json}")
                    logger.info(f"<<<<< ✅ Task Submitted!")
                    return True

        except Exception as e:
            logger.error(f"[SUBMIT] ❌ Error calling Submit Task API: {e}")
            raise

    #================================================================================================
    # Reject Task in Core
    #================================================================================================
    async def reject(self, rejection_reason: str):
        """Calls the Reject Task API asynchronously to Reject Task, includes jobCookie in cookies."""

        if not self.JOB_COOKIE or not isinstance(self.JOB_COOKIE, dict):
            raise ValueError("[REJECT] JOB_COOKIE is required and must be a non-empty dictionary.")

        try:
            logger.info(f"\n>>> Reject Task: {self.task_key}")

            url = f"{self.CORE_API}/v1/tasks/{self.task_key}/reject"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Rejecting Task from {self.AGENT_NAME} - Automated Task Rejected",
                    "reason": rejection_reason
                }
            }

            async with aiohttp.ClientSession(cookies=self.JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    if response.status != 200:
                        raise RuntimeError(f"[REJECT] ❌ Failed to reject task. HTTP Status: {response.status} - {response_json}")
                    logger.info(f"<<<<< ✅ Task Rejected!")
                    return True

        except Exception as e:
            logger.error(f"[REJECT] ❌ Error calling Reject Task API: {e}")
            raise

    #================================================================================================
    # Update Task Usage in Core
    #================================================================================================
    async def update_usage(self, duration_seconds: int):
        """
        Calls the Task Usage Update API asynchronously to log usage in minutes.
        Converts seconds to minutes (ceiling).
        """

        if not self.JOB_COOKIE or not isinstance(self.JOB_COOKIE, dict):
            raise ValueError("[USAGE] JOB_COOKIE is required and must be a non-empty dictionary.")

        try:
            duration_minutes = math.ceil(duration_seconds / 60)
            logger.info(f"\n>>> Update Usage for Task: {self.task_key}, Duration: {duration_seconds}s (~{duration_minutes} min)")

            url = f"{self.CORE_API}/v1/tasks/{self.task_key}/usage"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {"amount": duration_minutes}

            async with aiohttp.ClientSession(cookies=self.JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    if response.status not in [200, 201, 202, 203, 204]:
                        raise RuntimeError(f"[USAGE] ❌ Failed to update usage. HTTP Status: {response.status} - {response_json}")
                    logger.info("✅ Usage updated successfully!")
                    return True

        except Exception as e:
            logger.error(f"[USAGE] ❌ Error calling Update Usage API: {e}")
            raise
