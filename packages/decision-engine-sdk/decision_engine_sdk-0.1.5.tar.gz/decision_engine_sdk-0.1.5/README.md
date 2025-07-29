# Decision Engine SDK

This is a Python SDK for interacting with the Decision Engine REST APIs.

## Installation

```bash
pip install requests
```

## Usage

```python
import decision_engine_sdk

# Initialize the SDK
sdk = decision_engine_sdk.DecisionEngineSDK(base_url="http://localhost:8000")  # Replace with your base URL

# Decide Gateway API
payload = {"user_id": "user123", "transaction_amount": 100}
try:
    result = sdk.decide_gateway(payload)
    print(result)
except Exception as e:
    print(e)

# Update Gateway Score API
payload = {"gateway_id": "gateway1", "score": 0.8}
try:
    result = sdk.update_gateway_score(payload)
    print(result)
except Exception as e:
    print(e)
