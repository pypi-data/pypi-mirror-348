import pytest
from unittest.mock import patch, MagicMock
import requests
from rulerunner_sdk import RuleRunnerClient, RuleRunnerAPIError, RuleRunnerConnectionError
import hashlib # Import for tests

# Test data
TEST_API_KEY = "test_api_key_123"
TEST_BASE_URL = "http://test.api.rulerunner.com"
TEST_FROM_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
TEST_TO_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44f"
TEST_AMOUNT = "10.0"

@pytest.fixture
def client():
    return RuleRunnerClient(api_key=TEST_API_KEY, api_url=TEST_BASE_URL)

def test_client_initialization():
    # Test with required api_key
    client = RuleRunnerClient(api_key=TEST_API_KEY)
    assert client.api_key == TEST_API_KEY
    assert client.api_url == "https://api.rulerunner.io"  # Corrected default

    # Test with custom base_url
    client = RuleRunnerClient(api_key=TEST_API_KEY, api_url=TEST_BASE_URL)
    assert client.api_url == TEST_BASE_URL

    # Test with API key not provided (should print warning, not raise ValueError based on current client)
    # client_no_key = RuleRunnerClient(api_url=TEST_BASE_URL)
    # assert client_no_key.api_key is None 
    # # Check stdout for warning if possible, or just ensure no error

@patch('rulerunner_sdk.client.requests.request')
def test_is_compliant_success(mock_request, client):
    # Mock successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "is_compliant": True,
        "message": "Transaction is compliant",
        "from_address_sanctioned": False,
        "to_address_sanctioned": False,
        "from_address_proof": None,
        "to_address_proof": None,
        "merkle_root": "test_root",
        "from_entity_details": None,
        "to_entity_details": None,
        "checked_lists": ["OFAC_LLM"]
    }
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # Test the method
    result = client.is_compliant(
        from_address=TEST_FROM_ADDRESS,
        to_address=TEST_TO_ADDRESS,
        amount=TEST_AMOUNT
    )

    # Verify the request
    mock_request.assert_called_once_with(
        "POST", # Method first
        f"{TEST_BASE_URL}/api/v1/isCompliant",
        json={
            "from_address": TEST_FROM_ADDRESS,
            "to_address": TEST_TO_ADDRESS,
            "amount": TEST_AMOUNT
        },
        headers={"X-API-Key": TEST_API_KEY, "Content-Type": "application/json", "Accept": "application/json"},
        timeout=10
    )

    # Verify the response
    assert result["is_compliant"] is True
    assert result["message"] == "Transaction is compliant"
    assert result["merkle_root"] == "test_root"

@patch('rulerunner_sdk.client.requests.request')
def test_is_compliant_api_error(mock_request, client):
    # Mock API error response
    mock_response = MagicMock()
    mock_response.json.return_value = {"detail": "Invalid API key"}
    mock_response.status_code = 401
    # Simulate HTTPError being raised by response.raise_for_status()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
    mock_request.return_value = mock_response

    # Test the method
    with pytest.raises(RuleRunnerAPIError) as exc_info:
        client.is_compliant(
            from_address=TEST_FROM_ADDRESS,
            to_address=TEST_TO_ADDRESS,
            amount=TEST_AMOUNT
        )

    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)

@patch('rulerunner_sdk.client.requests.request')
def test_is_compliant_connection_error(mock_request, client):
    # Mock connection error
    mock_request.side_effect = requests.exceptions.ConnectionError()

    # Test the method
    with pytest.raises(RuleRunnerConnectionError):
        client.is_compliant(
            from_address=TEST_FROM_ADDRESS,
            to_address=TEST_TO_ADDRESS,
            amount=TEST_AMOUNT
        )

@patch('rulerunner_sdk.client.requests.request')
def test_health_check_success(mock_request, client):
    # Mock successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "ok",
        "version": "1.0.0",
        "sanctions_addresses_count": 1000,
        "merkle_root": "test_root",
        "active_lists": ["OFAC_LLM"]
    }
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # Test the method
    result = client.health_check()

    # Verify the request
    mock_request.assert_called_once_with(
        "GET", # Method first
        f"{TEST_BASE_URL}/api/v1/health",
        headers={"X-API-Key": TEST_API_KEY, "Content-Type": "application/json", "Accept": "application/json"},
        json=None,
        timeout=10
    )

    # Verify the response
    assert result["status"] == "ok"
    assert result["version"] == "1.0.0"
    assert result["sanctions_addresses_count"] == 1000

def test_verify_proof_locally():
    client = RuleRunnerClient(api_key=TEST_API_KEY)
    
    # Test data for a simple valid proof
    address = "0xa"
    # hash("a")
    leaf_hash = hashlib.sha256("a".encode()).hexdigest()
    
    sibling_hash = hashlib.sha256("s1".encode()).hexdigest()
    
    # root = hash(leaf_hash + sibling_hash) (right sibling)
    root = hashlib.sha256((leaf_hash + sibling_hash).encode()).hexdigest()
    
    proof = [
        {"position": "right", "data": sibling_hash} # Corrected 'hash' to 'data' to match client.py
    ]

    result = client.verify_proof_locally(address, proof, root)
    assert result is True

def test_verify_proof_locally_invalid():
    client = RuleRunnerClient(api_key=TEST_API_KEY)
    
    # Test data for an invalid proof
    address = "0xa"
    leaf_hash = hashlib.sha256("a".encode()).hexdigest()
    sibling_hash = hashlib.sha256("s1".encode()).hexdigest()
    
    # Correct root would be hash(leaf_hash + sibling_hash)
    # Use a different root to make it invalid
    invalid_root = hashlib.sha256("not_the_root".encode()).hexdigest()
    
    proof = [
        {"position": "right", "data": sibling_hash} # Corrected 'hash' to 'data'
    ]
        
    result = client.verify_proof_locally(address, proof, invalid_root)
    assert result is False 