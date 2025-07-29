import os
import aiohttp
import logging
import math
import asyncio

logger = logging.getLogger("core.task")

#===================================================================================================
class Core:
    """Handles the calls to core APIs for task authentication, execution, and lifecycle management."""

    def __init__(
        self, 
        AGENT_NAME: str, 
        CORE_API: str, 
    ):
        """
        Initialize Core API handler with agent credentials and base API URL.

        Args:
            AGENT_NAME (str): The agent's username for authentication.
            CORE_API (str): Base URL of the Core API service.

        Raises:
            ValueError: If AGENT_NAME or CORE_API is missing or empty.
        """

        if not AGENT_NAME:
            raise ValueError("[INIT] AGENT_NAME is required and cannot be empty.")
        if not CORE_API:
            raise ValueError("[INIT] CORE_API is required and cannot be empty.")

        self.CORE_API = CORE_API.rstrip("/")
        self.AGENT_NAME = AGENT_NAME
        self.JWT_TOKEN = None

    #================================================================================================
    # login to Core and get JWT
    #================================================================================================
    async def login(self, PASSWORD: str = None) -> bool:
        """
        Authenticate the agent to Core using username/password and store JWT token.

        Args:
            PASSWORD (str): Password for the agent.

        Returns:
            bool: True if login is successful.

        Raises:
            ValueError: If password is not provided.
            RuntimeError: If authentication fails after retries.
        """

        logger.info(f"🔑 [LOGIN] Authenticating to Core API with user: {self.AGENT_NAME}")
        
        if not PASSWORD:
            raise ValueError("[LOGIN] PASSWORD must be provided to login.")

        logger.info("🔐 [LOGIN] Using username and password for logging to Core.")

        login_url = f"{self.CORE_API}/auth"
        headers = {"Referer": self.CORE_API}

        auth_payload = {
            "identifier": self.AGENT_NAME,
            "password": PASSWORD
        }

        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(login_url, json=auth_payload, headers=headers) as login_response:
                        login_json = await login_response.json()
                        if login_response.status == 200 and "jwt" in login_json:
                            self.JWT_TOKEN = login_json["jwt"]
                            logger.info(f"✅ [LOGIN] Login succeeded on attempt {attempt}")
                            break
                        else:
                            logger.warning(f"⚠️ [LOGIN] Login failed on attempt {attempt}: {login_response.status} - {login_json}")
            except Exception as e:
                logger.error(f"❌ [LOGIN] Login error on attempt {attempt}: {e}")

            if attempt < max_retries:
                logger.info("🔁 [LOGIN] Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                raise RuntimeError("[LOGIN] ❌ Authentication failed after maximum retry attempts.")

        return True
    #================================================================================================
    # Connect to Task in Core
    #================================================================================================
    async def connect_task(self, task_key: str) -> dict:
        """
        Establishes a session for the given task and returns job cookies.

        Args:
            task_key (str): Task key to identify the task session.

        Returns:
            dict: Dictionary of job cookies from the response.

        Raises:
            ValueError: If task_key is not provided or JWT is missing.
            RuntimeError: If the connection fails or cookies are missing.
        """
        logger.info(f"🔑 Authenticating to Core API with user: {self.AGENT_NAME}")

        if not self.JWT_TOKEN:
            logger.error("🔐 [CONNECT] Must login to Core before connecting to task.")
            raise ValueError("[CONNECT] Must login to Core before connecting to task.")
        
        if not task_key:
            logger.error("🔐 [CONNECT] Must provide task_key to connect.")
            raise ValueError("[CONNECT] task_key must be provided to connect.")
        
        connect_url = f"{self.CORE_API}/v1/tasks/{task_key}/connect"
    
        try:
            connect_headers = {
                "Authorization": f"Bearer {self.JWT_TOKEN}",
                "Referer": self.CORE_API
            }

            async with aiohttp.ClientSession() as connect_session:
                async with connect_session.post(connect_url, headers=connect_headers) as connect_response:
                    if connect_response.status != 200:
                        raise RuntimeError(f"❌ [CONNECT] Connect failed: {connect_response.status} - {await connect_response.text()}")

                    JOB_COOKIE = connect_session.cookie_jar.filter_cookies(self.CORE_API)
                    JOB_COOKIE = {k: morsel.value for k, morsel in JOB_COOKIE.items()}

                    if not JOB_COOKIE:
                        logger.error("❌ [CONNECT] No cookies found in the response.")
                        raise RuntimeError("❌ [CONNECT] No cookies found in the response.")
                    
                    logger.info("✅ JOB_COOKIE successfully returned from connect response")
                    return JOB_COOKIE

        except Exception as e:
            logger.error(f"[CONNECT] ❌ Error during connect request: {e}")
            raise RuntimeError(f"[CONNECT] ❌ Error during connect request: {e}")

    #================================================================================================
    # Start Task in Core
    #================================================================================================
    async def start_task(self, JOB_COOKIE: dict, task_key: str, reterive_agent_assignment: bool = False) -> dict:
        """
        Starts a task in Core by calling the `/start` endpoint.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task to start.
            reterive_agent_assignment (bool, optional): If True, Core will return agent assignment details.

        Returns:
            dict: JSON response returned by Core, typically containing updated task state or assignment data.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or response is invalid.
        """
        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [START-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [START-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
        
        if not task_key:
            logger.error("❌ [START-TASK] task_key is required and cannot be empty.")
            raise ValueError("❌ [START-TASK] task_key is required and cannot be empty.")

        try:
            logger.info(f">>> [START-TASK] Starting Task: {task_key}")

            start_task_url = f"{self.CORE_API}/v1/tasks/{task_key}/start"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Starting Task from {self.AGENT_NAME}",
                    "retrieveAgentAssignment": reterive_agent_assignment
                }
            }

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(start_task_url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None

                    if response.status == 200 and response_json is not None:
                        logger.info(f"<<<<< ✅ [START-TASK] Task Started!")
                        return response_json
                    else:
                        logger.error(f"❌ [START-TASK] Failed to start task. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [START-TASK] Failed to start task. HTTP Status: {response.status} - {response_json}")

        except Exception as e:
            logger.error(f"❌ [START-TASK] Error calling Start Task API: {e}")
            raise RuntimeError(f"❌ [START-TASK] Error calling Start Task API: {e}")

    #================================================================================================
    # Submit Task in Core
    #================================================================================================
    async def submit_task(self, JOB_COOKIE: dict, task_key: str) -> bool:
        """
        Submits a task in Core by calling the `/submit` endpoint.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task to submit.

        Returns:
            bool: True if task submission succeeds.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or submission is rejected.
        """

        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [SUBMIT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [SUBMIT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
        
        if not task_key:
            logger.error("❌ [SUBMIT-TASK] task_key is required and cannot be empty.")
            raise ValueError("❌ [SUBMIT-TASK] task_key is required and cannot be empty.")

        try:
            logger.info(f">>> [SUBMIT-TASK] Submit Task: {task_key}")

            url = f"{self.CORE_API}/v1/tasks/{task_key}/submit"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Submitting Task from {self.AGENT_NAME}"
                }
            }

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    
                    if response.status != 200:
                        logger.error(f"❌ [SUBMIT-TASK]Failed to submit task. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [SUBMIT-TASK] Failed to submit task. HTTP Status: {response.status} - {response_json}")
                    
                    logger.info(f"<<<<< ✅ [SUBMIT-TASK] Task Submitted!")
                    return True

        except Exception as e:
            logger.error(f"❌ [SUBMIT-TASK] Error calling Submit Task API: {e}")
            raise RuntimeError(f"❌ [SUBMIT-TASK] Error calling Submit Task API: {e}")

    #================================================================================================
    # Reject Task in Core
    #================================================================================================
    async def reject_task(self, JOB_COOKIE: dict, task_key: str, rejection_reason: str = "No reason provided") -> bool:
        """
        Rejects a task in Core by calling the `/reject` endpoint.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task to reject.
            rejection_reason (str, optional): Reason for rejecting the task. Defaults to "No reason provided".

        Returns:
            bool: True if task rejection succeeds.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or rejection is unsuccessful.
        """

        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [REJECT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [REJECT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")

        if not task_key:
            logger.error("❌ [REJECT-TASK] task_key is required and cannot be empty.")
            raise ValueError("❌ [REJECT-TASK] task_key is required and cannot be empty.")
        
        try:
            logger.info(f">>> Reject Task: {task_key}")

            url = f"{self.CORE_API}/v1/tasks/{task_key}/reject"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Rejecting Task from {self.AGENT_NAME}",
                    "reason": rejection_reason
                }
            }

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    
                    if response.status != 200:
                        logger.error(f" ❌ [REJECT-TASK] Failed to reject task. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [REJECT-TASK] Failed to reject task. HTTP Status: {response.status} - {response_json}")
                    
                    logger.info(f"<<<<< ✅ Task Rejected!")
                    
                    return True

        except Exception as e:
            logger.error(f"❌ [REJECT-TASK] Error calling Reject Task API: {e}")
            raise RuntimeError(f"❌ [REJECT-TASK] Error calling Reject Task API: {e}")

    #================================================================================================
    # Update Task Usage in Core
    #================================================================================================
    async def update_usage(self, JOB_COOKIE: dict, task_key: str, duration_seconds: int):
        """
        Updates the usage time of a task in Core by calling the `/usage` endpoint.
        Duration is rounded up to the nearest full minute.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task.
            duration_seconds (int): Number of seconds the task has been active.

        Returns:
            bool: True if the usage update is successful.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or the update is rejected.
        """

        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [USAGE] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [USAGE] JOB_COOKIE is required and must be a non-empty dictionary.")

        if not task_key:
            logger.error("❌ [USAGE] task_key is required and cannot be empty.")
            raise ValueError("❌ [USAGE] task_key is required and cannot be empty.")
        
        try:
            duration_minutes = math.ceil(duration_seconds / 60)
            logger.info(f">>> Update Usage for Task: {task_key}, Duration: {duration_seconds}s (~{duration_minutes} min)")

            url = f"{self.CORE_API}/v1/tasks/{task_key}/usage"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {"amount": duration_minutes}

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None

                    if response.status not in [200, 201, 202, 203, 204]:
                        logger.error(f"❌ [USAGE] Failed to update usage. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [USAGE] Failed to update usage. HTTP Status: {response.status} - {response_json}")
                    
                    logger.info("✅ [USAGE] Usage updated successfully!")
                    
                    return True

        except Exception as e:
            logger.error(f"❌ [USAGE] Error calling Update Usage API: {e}")
            raise RuntimeError(f"❌ [USAGE] Error calling Update Usage API: {e}")
