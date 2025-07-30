import requests

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
        - contents (str): Input content for generation
        - **kwargs: Additional parameters for the API
        
        Returns:
        - Response object containing the API response
        """
        # Convert string contents to list if it's not already
        if isinstance(contents, str):
            contents_data = [contents]
        else:
            contents_data = contents
            
        # Prepare the request payload
        data = {
            'model': model,
            'contents': contents,  # Keep original format for API endpoint
            'temperature': kwargs.get('temperature'),
            'max_tokens': kwargs.get('max_tokens'),
            'tools': kwargs.get('tools'),
            'function_call': kwargs.get('function_call')
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
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
