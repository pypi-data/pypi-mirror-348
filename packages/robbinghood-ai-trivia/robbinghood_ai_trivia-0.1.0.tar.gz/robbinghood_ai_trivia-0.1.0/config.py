import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import vision
from google.oauth2 import service_account

class Config:
    """Configuration class for application settings and API credentials"""
    
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # Get API keys from environment variables
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        
        # Validate all credentials before proceeding
        self._validate_credentials()
        
        # Initialize the Google Vision client
        self.vision_client = self._init_vision_client()
    
    def _validate_credentials(self):
        """Validate that required credentials are set and valid"""
        # Check Perplexity API key
        if not self.perplexity_api_key:
            self._raise_credential_error(
                "PERPLEXITY_API_KEY", 
                "Sign up at https://www.perplexity.ai/ to get your API key"
            )
        
        # Check OpenAI API key
        if not self.openai_api_key:
            self._raise_credential_error(
                "OPENAI_API_KEY", 
                "Sign up at https://platform.openai.com/ to get your API key"
            )
        
        # Check Google credentials path
        if not self.google_credentials_path:
            self._raise_credential_error(
                "GOOGLE_CREDENTIALS_PATH", 
                "Set up Google Cloud Vision at https://console.cloud.google.com/ and download your credentials JSON file"
            )
        
        # Verify Google credentials file exists
        creds_path = Path(self.google_credentials_path)
        if not creds_path.exists():
            raise ValueError(
                f"Google credentials file not found at: {self.google_credentials_path}\n"
                f"Please check the path specified in your GOOGLE_CREDENTIALS_PATH environment variable."
            )
    
    def _raise_credential_error(self, env_var_name, help_text):
        """Raise a detailed error message for missing credentials"""
        raise ValueError(
            f"\nError: {env_var_name} environment variable is not set.\n\n"
            f"How to fix this issue:\n"
            f"1. {help_text}\n"
            f"2. Set the environment variable using one of these methods:\n\n"
            f"   Option A: Create a .env file in the project directory with the following line:\n"
            f"   {env_var_name}=your_api_key_here\n\n"
            f"   Option B: Set the environment variable in your terminal session:\n"
            f"   export {env_var_name}=your_api_key_here    (Linux/macOS)\n"
            f"   set {env_var_name}=your_api_key_here       (Windows Command Prompt)\n"
            f"   $env:{env_var_name}=\"your_api_key_here\"  (Windows PowerShell)\n"
        )
    
    def _init_vision_client(self):
        """Initialize and return a Google Vision client"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.google_credentials_path
            )
            return vision.ImageAnnotatorClient(credentials=credentials)
        except Exception as e:
            print(f"Error initializing Google Vision client: {e}")
            print("Please check that your Google Cloud credentials are valid and have access to the Vision API.")
            sys.exit(1)
