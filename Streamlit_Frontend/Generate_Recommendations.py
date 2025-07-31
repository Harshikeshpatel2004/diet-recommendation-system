import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockResponse:
    def __init__(self, status_code, error_data):
        self.status_code = status_code
        self._error_data = error_data
    
    def json(self):
        return self._error_data

class Generator:
    def __init__(self, nutrition_input: list, ingredients: list = [], params: dict = {'n_neighbors': 5, 'return_distance': False}):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params
        # You can change this URL to your deployed backend
        self.api_url = 'https://diet-recommendation-system-nub1.onrender.com/predict/'

    def set_request(self, nutrition_input: list, ingredients: list, params: dict):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params

    def generate(self):
        request = {
            'nutrition_input': self.nutrition_input,
            'ingredients': self.ingredients,
            'params': self.params
        }
        
        try:
            logger.info(f"Sending request to {self.api_url}")
            logger.info(f"Request data: {request}")
            
            response = requests.post(
                url=self.api_url,
                data=json.dumps(request), 
                headers={"Content-Type": "application/json"},
                timeout=30  # Add timeout to prevent hanging requests
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            
            # Check if response is successful
            if response.status_code == 200:
                try:
                    # Try to parse JSON response
                    json_response = response.json()
                    logger.info("Successfully parsed JSON response")
                    return response
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    logger.error(f"Response text: {response.text[:500]}...")  # Log first 500 chars
                    
                    # Return a mock response with error information
                    error_response = MockResponse(500, {
                        'output': None,
                        'error': f'Invalid JSON response from server: {str(e)}',
                        'message': 'The server returned an invalid response format'
                    })
                    return error_response
            else:
                logger.error(f"HTTP error {response.status_code}: {response.text}")
                # Try to parse error response as JSON
                try:
                    error_json = response.json()
                    return response
                except json.JSONDecodeError:
                    # Return a mock response with error information
                    error_response = MockResponse(response.status_code, {
                        'output': None,
                        'error': f'HTTP {response.status_code}: {response.text}',
                        'message': f'Server returned error status {response.status_code}'
                    })
                    return error_response
                    
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            error_response = MockResponse(408, {
                'output': None,
                'error': 'Request timed out',
                'message': 'The server took too long to respond'
            })
            return error_response
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            error_response = MockResponse(503, {
                'output': None,
                'error': 'Connection error',
                'message': 'Unable to connect to the server'
            })
            return error_response
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            error_response = MockResponse(500, {
                'output': None,
                'error': f'Unexpected error: {str(e)}',
                'message': 'An unexpected error occurred while making the request'
            })
            return error_response
