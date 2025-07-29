import pytest
from unittest.mock import patch, MagicMock
import requests
from rulerunner_sdk import RuleRunnerClient, RuleRunnerAPIError, RuleRunnerConnectionError

# Test data
TEST_API_KEY = "test_api_key_123"
TEST_BASE_URL = "http://test.api.rulerunner.com"
TEST_FROM_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
TEST_TO_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44f"
TEST_AMOUNT = "10.0"

@pytest.fixture
def client():
    return RuleRunnerClient(api_key=TEST_API_KEY, base_url=TEST_BASE_URL)

def test_client_initialization():
    # Test with required api_key
    client = RuleRunnerClient(api_key=TEST_API_KEY)
    assert client.api_key == TEST_API_KEY
    assert client.base_url == "https://api.rulerunner.com"  # default

    # Test with custom base_url
    client = RuleRunnerClient(api_key=TEST_API_KEY, base_url=TEST_BASE_URL)
    assert client.base_url == TEST_BASE_URL

    # Test without api_key
    with pytest.raises(ValueError):
        RuleRunnerClient(api_key="")

@patch('requests.post')
def test_is_compliant_success(mock_post, client):
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
    mock_post.return_value = mock_response

    # Test the method
    result = client.is_compliant(
        from_address=TEST_FROM_ADDRESS,
        to_address=TEST_TO_ADDRESS,
        amount=TEST_AMOUNT
    )

    # Verify the request
    mock_post.assert_called_once_with(
        f"{TEST_BASE_URL}/api/v1/isCompliant",
        json={
            "from_address": TEST_FROM_ADDRESS,
            "to_address": TEST_TO_ADDRESS,
            "amount": TEST_AMOUNT
        },
        headers={"X-API-Key": TEST_API_KEY}
    )

    # Verify the response
    assert result["is_compliant"] is True
    assert result["message"] == "Transaction is compliant"
    assert result["merkle_root"] == "test_root"

@patch('requests.post')
def test_is_compliant_api_error(mock_post, client):
    # Mock API error response
    mock_response = MagicMock()
    mock_response.json.return_value = {"detail": "Invalid API key"}
    mock_response.status_code = 401
    mock_post.return_value = mock_response

    # Test the method
    with pytest.raises(RuleRunnerAPIError) as exc_info:
        client.is_compliant(
            from_address=TEST_FROM_ADDRESS,
            to_address=TEST_TO_ADDRESS,
            amount=TEST_AMOUNT
        )

    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)

@patch('requests.post')
def test_is_compliant_connection_error(mock_post, client):
    # Mock connection error
    mock_post.side_effect = requests.exceptions.ConnectionError()

    # Test the method
    with pytest.raises(RuleRunnerConnectionError):
        client.is_compliant(
            from_address=TEST_FROM_ADDRESS,
            to_address=TEST_TO_ADDRESS,
            amount=TEST_AMOUNT
        )

@patch('requests.get')
def test_health_check_success(mock_get, client):
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
    mock_get.return_value = mock_response

    # Test the method
    result = client.health_check()

    # Verify the request
    mock_get.assert_called_once_with(
        f"{TEST_BASE_URL}/api/v1/health",
        headers={"X-API-Key": TEST_API_KEY}
    )

    # Verify the response
    assert result["status"] == "ok"
    assert result["version"] == "1.0.0"
    assert result["sanctions_addresses_count"] == 1000

def test_verify_proof_locally():
    client = RuleRunnerClient(api_key=TEST_API_KEY)
    
    # Test data
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    proof = [
        {"position": "right", "hash": "hash1"},
        {"position": "left", "hash": "hash2"}
    ]
    root = "final_hash"

    # Mock the sha256 method
    with patch.object(client, '_sha256') as mock_sha256:
        mock_sha256.side_effect = ["hash1", "hash2", "final_hash"]
        
        # Test the method
        result = client.verify_proof_locally(address, proof, root)
        
        # Verify the result
        assert result is True
        assert mock_sha256.call_count == 3  # Called for address and each proof step

def test_verify_proof_locally_invalid():
    client = RuleRunnerClient(api_key=TEST_API_KEY)
    
    # Test data
    address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    proof = [
        {"position": "right", "hash": "hash1"},
        {"position": "left", "hash": "hash2"}
    ]
    root = "different_hash"

    # Mock the sha256 method
    with patch.object(client, '_sha256') as mock_sha256:
        mock_sha256.side_effect = ["hash1", "hash2", "wrong_hash"]
        
        # Test the method
        result = client.verify_proof_locally(address, proof, root)
        
        # Verify the result
        assert result is False 