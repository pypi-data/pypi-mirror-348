"""
Python client for the RuleRunner API.
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional, Union, List

import requests

# --- Custom Exception classes ---
class RuleRunnerError(Exception):
    """Base exception class for RuleRunner SDK errors."""
    pass

class RuleRunnerAPIError(RuleRunnerError):
    """Raised for API-specific errors (e.g., 4XX, 5XX responses)."""
    def __init__(self, message, status_code=None, detail=None):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail # Store additional detail from API if available

    def __str__(self):
        if self.detail:
            return f"{super().__str__()} (Status: {self.status_code}, Detail: {self.detail})"
        if self.status_code:
            return f"{super().__str__()} (Status: {self.status_code})"
        return super().__str__()

class RuleRunnerConnectionError(RuleRunnerError):
    """Raised for network or connection-related errors."""
    pass

class RuleRunnerProofVerificationError(RuleRunnerError):
    """Raised for errors during local proof verification."""
    pass


class RuleRunnerClient:
    """
    Client for interacting with the RuleRunner API.
    """
    DEFAULT_API_URL = "https://api.rulerunner.io" # Renamed for clarity
    
    def __init__(
        self,
        api_url: Optional[str] = None, # Allow None to use default
        api_key: Optional[str] = None,
        timeout: int = 10,
    ):
        """
        Initialize the RuleRunner client.
        
        Args:
            api_url: Base URL for the RuleRunner API. Defaults to http://localhost:8000.
            api_key: API key for authentication. Can also be set via RULERUNNER_API_KEY env var.
            timeout: Request timeout in seconds.
        """
        self.api_url = (api_url or self.DEFAULT_API_URL).rstrip("/")
        
        effective_api_key = api_key or os.getenv("RULERUNNER_API_KEY")
        if not effective_api_key:
            # Warning instead of error to allow calls to unauthenticated endpoints like /health if API supports it
            print("Warning: RuleRunner API key not provided. Authenticated endpoints will fail.") 
            self.api_key = None
        else:
            self.api_key = effective_api_key
            
        self.timeout = timeout
        
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key

    def _request(self, method: str, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper method to make requests to the API."""
        url = f"{self.api_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=json_data, timeout=self.timeout)
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_detail_json = None
            error_detail_text = str(e)
            if e.response is not None:
                try:
                    error_detail_json = e.response.json()
                    error_detail_text = error_detail_json.get("detail", str(e))
                except requests.exceptions.JSONDecodeError:
                    error_detail_text = e.response.text # Use raw text if not JSON
            raise RuleRunnerAPIError(
                f"API Error for {method} {url}", 
                status_code=e.response.status_code if e.response is not None else None,
                detail=error_detail_json or error_detail_text # Prefer JSON structure, fallback to text
            ) from e
        except requests.exceptions.RequestException as e: # Covers ConnectionError, Timeout, etc.
            raise RuleRunnerConnectionError(f"Connection error for {method} {url}: {e}") from e
        except json.JSONDecodeError as e: # If API returns non-JSON success response (should not happen for this API)
            raise RuleRunnerAPIError(f"Failed to decode JSON response from {method} {url}: {e}") from e
    
    def is_compliant(
        self,
        from_address: str,
        to_address: str,
        amount: Union[str, int, float],
        # token_address: Optional[str] = None, # Not used by current API, can be added later
        # chain_id: int = 1, # Not used by current API
    ) -> Dict[str, Any]:
        """
        Check if a transaction is compliant based on current sanctions lists.
        
        Args:
            from_address: Sender's blockchain address.
            to_address: Recipient's blockchain address.
            amount: Transaction amount (converted to string). 
                    Note: Current API version does not use this for Travel Rule checks yet.
            
        Returns:
            Dict with compliance check results, including:
            - is_compliant (bool): Whether the transaction is considered compliant.
            - message (str): A descriptive message about the compliance status.
            - from_address_sanctioned (bool): True if the sender is sanctioned.
            - to_address_sanctioned (bool): True if the recipient is sanctioned.
            - from_address_proof (Optional[List[Dict]]): Merkle proof for sender if sanctioned.
            - to_address_proof (Optional[List[Dict]]): Merkle proof for recipient if sanctioned.
            - merkle_root (str): The Merkle root used for the check.
            - from_entity_details (Optional[Dict]): Details of the sanctioned entity for sender.
            - to_entity_details (Optional[Dict]): Details of the sanctioned entity for recipient.
            - checked_lists (List[str]): List of sanctions lists checked.
            
        Raises:
            RuleRunnerAPIError: If the API returns an error.
            RuleRunnerConnectionError: If there's a problem connecting to the API.
            ValueError: If required arguments are missing.
        """
        if not from_address or not to_address:
            raise ValueError("from_address and to_address are required for compliance check.")
            
        payload = {
            "from_address": from_address,
            "to_address": to_address,
            "amount": str(amount), 
        }
        
        # Optional fields not used by current /isCompliant endpoint
        # if token_address:
        #     payload["token_address"] = token_address
        # if chain_id != 1: # Assuming 1 is a default that API might ignore if not sent
        #     payload["chain_id"] = chain_id
        
        return self._request("POST", "/api/v1/isCompliant", json_data=payload)
    
    def verify_proof_locally(
        self, 
        address: str, 
        proof: List[Dict[str, str]], 
        root: str
    ) -> bool:
        """
        Verify a Merkle proof locally. This implementation matches core.merkle_custom.
        
        Args:
            address: The address to verify (e.g., from_address or to_address).
            proof: The Merkle proof (e.g., from_address_proof or to_address_proof).
                   Expected format: List of {'data': sibling_hash, 'position': 'left'|'right'}.
            root: The Merkle root the proof was generated against.
            
        Returns:
            bool: True if the proof is valid for the address and root.
        
        Raises:
            RuleRunnerProofVerificationError: If proof structure is invalid or hashing fails.
        """
        if not isinstance(address, str) or not address:
            raise RuleRunnerProofVerificationError("Address must be a non-empty string.")
        if not isinstance(proof, list):
            raise RuleRunnerProofVerificationError("Proof must be a list.")
        if not isinstance(root, str) or not root:
            raise RuleRunnerProofVerificationError("Root must be a non-empty string.")

        try:
            # Normalize address - lowercase without '0x' prefix
            current_hash_address = address
            if current_hash_address.startswith("0x"):
                current_hash_address = current_hash_address[2:]
            current_hash_address = current_hash_address.lower()
            
            # Hash the address
            current_hash = hashlib.sha256(current_hash_address.encode()).hexdigest()
            
            for element in proof:
                if not isinstance(element, dict) or 'data' not in element or 'position' not in element:
                    raise RuleRunnerProofVerificationError("Invalid proof element structure. Expected {'data': str, 'position': str}.")
                
                sibling = element["data"]
                position = element["position"]
                
                if not isinstance(sibling, str) or position not in ["left", "right"]:
                     raise RuleRunnerProofVerificationError("Invalid sibling or position in proof element.")

                if position == "right":
                    combined = current_hash + sibling
                else:  # left
                    combined = sibling + current_hash
                    
                current_hash = hashlib.sha256(combined.encode()).hexdigest()
            
            return current_hash == root
        except TypeError as e: # Catch potential errors if data types are wrong before hashing
            raise RuleRunnerProofVerificationError(f"Type error during proof verification: {e}") from e
        except Exception as e: # Catch any other unexpected errors
            raise RuleRunnerProofVerificationError(f"Unexpected error during proof verification: {e}") from e
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the RuleRunner API.
        
        Returns:
            Dict with API health status, including 'status', 'version', 
            'sanctions_addresses_count', 'merkle_root', 'active_lists'.
        """
        return self._request("GET", "/api/v1/health") # No specific API key check in this version, but headers sent anyway
    
    def reload_sanctions_data(self) -> Dict[str, Any]:
        """
        [Admin] Force a reload of the sanctions data from the source.
        
        Requires an admin-level API key to be configured for the SDK instance and 
        for the corresponding ADMIN_API_KEY_SECRET to be set on the server.
        
        Returns:
            Dict with reload status.
        """
        if not self.api_key: # Or a more specific check if admin keys are different
            raise RuleRunnerError("Admin API key is required for reload_sanctions_data.")
        
        return self._request("POST", "/api/v1/admin/reload-sanctions")


# Example usage
if __name__ == "__main__":
    print("--- RuleRunner SDK Example --- ")
    # For this example to run, ensure your RuleRunner API server is running.
    # And set RULERUNNER_API_KEY environment variable if your API requires it for /isCompliant
    # (If API_KEY_SECRET is not set on server, any key will pass for /isCompliant in dev mode)

    try:
        # Initialize client. It will try to pick up RULERUNNER_API_KEY from env.
        # Pass api_key="your_actual_key" if not using env var or for specific keys.
        client = RuleRunnerClient() 
                                   
        print("\n--- Health Check ---")
        health = client.health_check()
        print(f"API Status: {health.get('status')}")
        print(f"API Version: {health.get('version')}")
        print(f"Sanctioned Addresses Count: {health.get('sanctions_addresses_count')}")
        print(f"Current Merkle Root: {health.get('merkle_root')}")
        print(f"Active Lists: {health.get('active_lists')}")
        
        # Mock addresses for testing - replace with actual addresses for real tests
        compliant_from = "0xabc123CleanSender"
        compliant_to = "0xdef456CleanReceiver"
        # Use addresses known to be sanctioned if your test API instance is preloaded
        # For this example, we'll use placeholders. For real tests against a live dev API,
        # ensure these reflect data known to be in your sanctions list (e.g., MOCK_SANCTIONED_ADDRESS_1 from tests)
        sanctioned_example_address = "0x1111111111111111111111111111111111111111" # Example

        print("\n--- Compliant Transaction Check ---")
        payload_compliant = {
            "from_address": compliant_from,
            "to_address": compliant_to,
            "amount": "1.0",
        }
        result_compliant = client.is_compliant(**payload_compliant)
        print(f"Compliance Result: {result_compliant.get('is_compliant')}")
        print(f"Message: {result_compliant.get('message')}")

        print("\n--- Sanctioned Transaction Check (Sender Sanctioned) ---")
        # This test assumes your API is running with mock data where sanctioned_example_address is sanctioned
        # Or that your local API (if API_KEY_SECRET is unset) will use the fallback "sanctioned" string check.
        # For more robust SDK testing, mock the HTTP responses.
        try:
            payload_sanctioned_sender = {
                "from_address": sanctioned_example_address, 
                "to_address": compliant_to,
                "amount": "100.0",
            }
            result_sanctioned = client.is_compliant(**payload_sanctioned_sender)
            print(f"Compliance Result: {result_sanctioned.get('is_compliant')}")
            print(f"Message: {result_sanctioned.get('message')}")
            print(f"Sender Sanctioned: {result_sanctioned.get('from_address_sanctioned')}")
            print(f"Sender Entity: {result_sanctioned.get('from_entity_details')}")

            if result_sanctioned.get('from_address_sanctioned') and result_sanctioned.get('from_address_proof'):
                print("Verifying proof for sanctioned sender locally...")
                is_proof_valid = client.verify_proof_locally(
                    address=payload_sanctioned_sender["from_address"],
                    proof=result_sanctioned["from_address_proof"],
                    root=result_sanctioned["merkle_root"]
                )
                print(f"Local proof verification for sender: {is_proof_valid}")
            else:
                print("No proof to verify for sender or sender not sanctioned as expected.")

        except RuleRunnerAPIError as api_err:
             print(f"API Error during sanctioned check (sender): {api_err}")


        # Note: The Travel Rule amount check logic is not yet in the /isCompliant API endpoint itself.
        # This example call will currently only check sanctions.
        # print("\n--- Transaction Exceeding Travel Rule (Conceptual) ---")
        # result_travel = client.is_compliant(
        #     from_address=compliant_from,
        #     to_address=compliant_to,
        #     amount="15000.0", # High amount
        # )
        # print(f"Travel Rule Check Result: {result_travel.get('is_compliant')}")
        # print(f"Message: {result_travel.get('message')}")
        
    except RuleRunnerError as e:
        print(f"SDK Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 