import requests
import time

class Solver:
    def __init__(self, capsolver_api_key: str = None):
        self.capsolver_api_key = capsolver_api_key

    def RecaptchaV2(self, website: str, site_key: str):
        """
        Solve ReCaptcha V2 using CapSolver API.
        
        :param website: Target website URL
        :param site_key: ReCaptcha site key
        :return: CAPTCHA solution token or None if failed
        """
        return self._solve_captcha(website, site_key, "ReCaptchaV2TaskProxyLess")

    def RecaptchaV3(self, website: str, site_key: str, min_score: float = 0.3):
        """
        Solve ReCaptcha V3 using CapSolver API.
        
        :param website: Target website URL
        :param site_key: ReCaptcha site key
        :param min_score: Minimum score (default 0.3)
        :return: CAPTCHA solution token or None if failed
        """
        return self._solve_captcha(website, site_key, "ReCaptchaV3TaskProxyLess", min_score)

    def _solve_captcha(self, website: str, site_key: str, captcha_type: str, min_score: float = None):
        """Internal function to solve CAPTCHA via CapSolver API."""
        if not self.capsolver_api_key:
            print("No API key provided for CapSolver.")
            return None

        # Define the task payload
        task_payload = {
            "type": captcha_type,
            "websiteURL": website,
            "websiteKey": site_key
        }

        # Add minScore for ReCaptcha V3
        if captcha_type == "ReCaptchaV3TaskProxyLess":
            task_payload["minScore"] = min_score

        # Send request to create task (FIXED: clientKey instead of apiKey)
        response = requests.post("https://api.capsolver.com/createTask", json={
            "clientKey": self.capsolver_api_key,  # <-- FIXED HERE
            "task": task_payload
        })

        response_data = response.json()

        task_id = response_data.get("taskId")
        if not task_id:
            return None

        # Poll for results
        retries = 10
        for attempt in range(retries):
            time.sleep(4)
            result = requests.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey": self.capsolver_api_key,  # <-- FIXED HERE
                "taskId": task_id
            })
            
            result_data = result.json()

            status = result_data.get("status")

            if status == "ready":
                captcha_key = result_data.get("solution", {}).get("gRecaptchaResponse")
                return captcha_key
            elif status == "failed":
                return None

        return None

