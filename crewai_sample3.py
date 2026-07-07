import requests
import json

# --- Configuration ---
TARGET_ENDPOINT = "http://100.71.195.41:20128/v1"

def run_api_interaction():
    """
    Directly interact with the API endpoint without crewai dependency.
    """
    print("--- Starting API Interaction ---")
    
    try:
        # Basic GET request to the endpoint
        print(f"Attempting to connect to: {TARGET_ENDPOINT}")
        response = requests.get(TARGET_ENDPOINT, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {TARGET_ENDPOINT}. Please check if the server is running.")
    except requests.exceptions.Timeout:
        print(f"Request timed out when connecting to {TARGET_ENDPOINT}")
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def make_custom_request(method='GET', data=None):
    """
    Make a custom request to the API endpoint.
    """
    print(f"Sending {method} request to {TARGET_ENDPOINT}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(TARGET_ENDPOINT, timeout=10)
        elif method.upper() == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(TARGET_ENDPOINT, json=data, headers=headers, timeout=10)
        else:
            print(f"Method {method} not supported in this example")
            return None
        
        print(f"Status Code: {response.status_code}")
        return response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    run_api_interaction()
    
    # Example: If you need to send data
    # test_data = {"key": "value"}
    # result = make_custom_request(method='POST', data=test_data)
    # print(f"Custom request result: {result}")