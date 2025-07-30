import requests
import logging
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Response:
    """
    A class to encapsulate the API response.
    Provides easy access to the response data.
    """
    def __init__(self, data):
        self.data = data
    
    @property
    def txt(self):
        """Easy access to the response text"""
        # First try to get the message field from the API response
        if self.data.get('message') is not None:
            return self.data.get('message')
        # Fallback to txt field for backward compatibility
        return self.data.get('txt')

class Models:
    """
    Handles model-related operations. Instantiated by the CNAI client.
    """
    def __init__(self, client):
        self.client = client
    
    def generate_content(self, model, contents, **kwargs):
        """
        Generates content using the specified model.
        Parameters:
        - model (str): The model name to use
        - contents (str or list): Input content for generation
        - **kwargs: Additional parameters for the API
        
        Returns:
        - Response object containing the API response
        """
        # Prepare the request payload
        data = {
            'model': model,
            'content': contents,
            'temperature': kwargs.get('temperature'),
            'max_tokens': kwargs.get('max_tokens'),
            'tools': kwargs.get('tools'),
            'function_call': kwargs.get('function_call')
        }
        
        # Format the contents based on its type
        if isinstance(contents, str):
            # Convert string to proper OpenAI message format 
            data['contents'] = [{"role": "user", "content": contents}]
        else:
            # Assume it's already properly formatted
            data['contents'] = contents
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        # Log the request for debugging
        logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
        
        # Make the API request
        response = requests.post(
            'https://apis.circuitnotion.com/v1/chat/completions',
            json=data,
            headers={
                'Authorization': f'Bearer {self.client.api_key}',
                'Content-Type': 'application/json'
            },
            timeout=30  # Increased timeout for model inference
        )
        
        # Log the response for debugging
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        try:
            logger.debug(f"Response body: {json.dumps(response.json(), indent=2)}")
        except:
            logger.debug(f"Response text: {response.text}")
        
        # Raise exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()
        
        return Response(response.json())

class CNAI:
    """
    Main client class. Initialize with your API key to access the API.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = Models(self) # Expose model operations
    
    @classmethod
    def Client(cls, api_key):
        """
        Class method to create a new client instance.
        This matches the user's desired usage: CNAI.Client(api_key)
        """
        return cls(api_key)