import pytest
from rulerunner_sdk import RuleRunnerClient, RuleRunnerAPIError
import os
from dotenv import load_dotenv

# Ensure this is your *real* production or staging API URL
REAL_API_URL = "https://api.rulerunner.io"
# Use an environment variable for the real API key for security
load_dotenv()
REAL_API_KEY = os.getenv("RULERUNNER_PROD_API_KEY")

# Test addresses - use ones that make sense for your live data
VALID_FROM_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e" # Example non-sanctioned
VALID_TO_ADDRESS = "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"   # Example non-sanctioned
# KNOWN_SANCTIONED_ADDRESS = "0x..." # Add a known sanctioned address for your API

@pytest.mark.integration
@pytest.fixture(scope="module")
def live_client():
    if not REAL_API_KEY or REAL_API_KEY == "your_actual_api_key_for_testing_prod_or_staging":
        pytest.skip("Real API key not set (RULERUNNER_PROD_API_KEY or hardcoded), skipping integration tests.")
    return RuleRunnerClient(api_key=REAL_API_KEY, api_url=REAL_API_URL)

@pytest.mark.integration
def test_live_health_check(live_client):
    """Test health check against the live API."""
    health = live_client.health_check()
    assert health["status"] == "ok"
    assert "version" in health
    assert health["sanctions_addresses_count"] >= 0
    assert health["merkle_root"] is not None

@pytest.mark.integration
def test_live_is_compliant_non_sanctioned(live_client):
    """Test a compliant transaction against the live API."""
    result = live_client.is_compliant(
        from_address=VALID_FROM_ADDRESS,
        to_address=VALID_TO_ADDRESS,
        amount="1.0"
    )
    assert result["is_compliant"] is True
    assert result["from_address_sanctioned"] is False
    assert result["to_address_sanctioned"] is False
    assert result["merkle_root"] is not None

# @pytest.mark.integration
# def test_live_is_compliant_known_sanctioned(live_client):
#     """Test a transaction with a known sanctioned address against the live API."""
#     if not KNOWN_SANCTIONED_ADDRESS:
#         pytest.skip("KNOWN_SANCTIONED_ADDRESS not set for integration test.")
#     result = live_client.is_compliant(
#         from_address=KNOWN_SANCTIONED_ADDRESS,
#         to_address=VALID_TO_ADDRESS,
#         amount="1.0"
#     )
#     assert result["is_compliant"] is False
#     assert result["from_address_sanctioned"] is True # Assuming sender is the known sanctioned one

@pytest.mark.integration
def test_live_is_compliant_invalid_api_key():
    """Test live API with an invalid key."""
    invalid_key_client = RuleRunnerClient(api_key="invalid_fake_key_123_testing_only", api_url=REAL_API_URL)
    with pytest.raises(RuleRunnerAPIError) as exc_info:
        invalid_key_client.is_compliant(
            from_address=VALID_FROM_ADDRESS,
            to_address=VALID_TO_ADDRESS,
            amount="1.0"
        )
    assert exc_info.value.status_code == 403 