"""
Ngrok configuration script to create a permanent tunnel to the Flask application
"""
from pyngrok import ngrok, conf
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_ngrok():
    """Configure ngrok with auth token and create tunnel"""
    # The auth token is already configured through the ngrok CLI or config file
    # We don't need to set it again here
    
    # Get Flask port (default is 5000)
    port = int(os.environ.get('PORT', 5000))
    
    # Create tunnel configuration
    conf.get_default().region = 'us'
    
    # Open a tunnel to the Flask application
    public_url = ngrok.connect(port, "http", options={
        "bind_tls": True,  # Enable HTTPS
    })
    
    print(f"\n* ngrok tunnel active at: {public_url}")
    print(f"* Access your Flask app at: {public_url}")
    print("* For ngrok status and metrics, go to http://127.0.0.1:4040\n")
    
    return public_url

if __name__ == "__main__":
    setup_ngrok() 