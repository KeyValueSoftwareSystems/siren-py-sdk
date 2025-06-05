"""Workflow management for Siren SDK."""

from typing import Any, Dict, Optional

import requests


class WorkflowsManager:
    """Manages workflow-related operations for the Siren API."""

    def __init__(self, base_url: str, api_key: str):
        """Initializes the WorkflowsManager.

        Args:
            base_url: The general base URL for the Siren API (e.g., 'https://api.trysiren.io').
            api_key: The API key for authentication.
        """
        self.base_url = f"{base_url}/api/v2"
        self.api_key = api_key

    def trigger_workflow(
        self,
        workflow_name: str,
        data: Optional[Dict[str, Any]] = None,
        notify: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Triggers a workflow with the given name and payload.

        Args:
            workflow_name: The name of the workflow to execute.
            data: Common data for all workflow executions.
            notify: Specific data for this workflow execution.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = (
            f"{self.base_url}/workflows/trigger"  # self.base_url now includes /api/v2
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload: Dict[str, Any] = {"workflowName": workflow_name}
        if data is not None:
            payload["data"] = data
        if notify is not None:
            payload["notify"] = notify

        try:
            response = requests.post(
                endpoint, headers=headers, json=payload, timeout=10
            )
            response.raise_for_status()  # Raises HTTPError for 4XX/5XX
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                return http_err.response.json()
            except requests.exceptions.JSONDecodeError:
                # If the error response is not JSON, re-raise the HTTPError
                # with the response text for better debugging.
                new_err = requests.exceptions.HTTPError(
                    f"{http_err}\nResponse text: {http_err.response.text}",
                    response=http_err.response,
                )
                raise new_err from http_err
        except requests.exceptions.RequestException as req_err:
            # For other request errors (e.g., connection issues)
            raise req_err
