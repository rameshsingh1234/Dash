import os
import logging
import pytest
import json
from Resuable.api_requests import make_request
from Resuable.assertion import assert_status_code, assert_response_keys, assert_response_body
from Utilities import CustomLogger
from Utilities.readproperties import ReadConfig

# Get the log directory and CSV file path from the configuration
log_directory = ReadConfig.get_logs_directory()
log_file_path = os.path.join(log_directory, "test.log")

# Set up the logger
logger = CustomLogger.setup_logger('API_TEST', log_file_path, level=logging.DEBUG)

# Get the CSV file path from the configuration
csv_file_path = ReadConfig.get_csv_file_path()

# Read the CSV data
csv_data = ReadConfig.read_csv(csv_file_path)

# Extract test case IDs for custom test names
test_params = [pytest.param(data, id=data['Testcase ID']) for data in csv_data]


# Function to get authorization token
def get_auth_token(auth_url, auth_method, auth_headers, auth_payload):
    logger.info("***********************Authorization Request Made*****************************")
    response = make_request(auth_url, auth_method, auth_headers, auth_payload)
    assert_status_code(response, 200)
    logger.info("***********************Authorization Successful*****************************")

    if 'application/json' in response.headers.get('Content-Type', ''):
        response_data = response.json()
        logger.info("***********************Authorization Response Received*****************************")
        logger.info(f" access_token is {response_data['data']['user']['access_token']}")
        return response_data['data']['user']['access_token']
    else:
        logger.error("Authorization response is not in JSON format")
        return None


# Get authorization details from configuration
auth_url = ReadConfig.get_auth_url()
auth_method = ReadConfig.get_auth_method()
auth_headers = json.loads(ReadConfig.get_auth_headers())
auth_payload = json.loads(ReadConfig.get_auth_payload())

# Get the authorization token
auth_token = get_auth_token(auth_url, auth_method, auth_headers, auth_payload)

# Get the base URL from configuration
base_url = ReadConfig.get_base_url()


@pytest.mark.parametrize("test_data", test_params)
def test_api(test_data):
    endpoint = test_data['endpoint']
    method = test_data['method']
    headers = json.loads(test_data['headers']) if test_data['headers'] else {}
    payload = json.loads(test_data['payload']) if test_data['payload'] else {}
    query_params = json.loads(test_data['params']) if test_data['params'] else {}
    expected_status_code = int(test_data['expected_status_code'])
    expected_keys = test_data['expected_response_keys'].split(',') if test_data['expected_response_keys'] else None
    expected_response = json.loads(test_data['expected_responce_body']) if test_data['expected_responce_body'] else None

    # Construct the full URL
    url = f"{base_url}{endpoint}"

    # Add authorization token to headers
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'

    logger.info("***********************API Test Start*****************************")
    logger.info("***********************API Request Made*****************************")
    response = make_request(url, method, headers, payload, params=query_params)

    if 'application/json' in response.headers.get('Content-Type', ''):
        response_data = response.json()
        logger.info("*********************** Response Received *****************************")
    else:
        response_data = None
        logger.info("*********************** Response is not in JSON format *****************************")
        logger.info(response.text)

    assert_status_code(response, expected_status_code)
    logger.info("*********************** Status Code Asserted *****************************")

    if expected_keys and response_data:
        assert_response_keys(response_data, expected_keys)
        logger.info("***********************Response Keys Asserted*****************************")

    if expected_response and response_data:
        assert_response_body(response, expected_response)
        logger.info("***********************Response Body Asserted*****************************")

    logger.info("***********************API Test Ends*****************************")
