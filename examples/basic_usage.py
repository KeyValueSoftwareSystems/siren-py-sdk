# examples/basic_usage.py

# This file will demonstrate basic usage of the SirenClient.

# from siren import SirenClient # This will work once the package is installed

# For local development, you might need to adjust sys.path:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from siren.client import SirenClient

if __name__ == "__main__":
    print("Running Siren SDK basic usage example...")
    
    # Replace 'YOUR_API_KEY' with a real or test API key
    api_key = "YOUR_API_KEY"
    if api_key == "YOUR_API_KEY":
        print("Please replace 'YOUR_API_KEY' with an actual API key to test.")
        # exit(1)

    client = SirenClient(api_key=api_key)

    # Example: Send a message (this will be implemented later)
    # try:
    #     response = client.send_message({
    #         "to": "user@example.com",
    #         "template": "ai_task_completed",
    #         "data": {
    #             "task_name": "Data Cleanup",
    #             "result": "Success"
    #         }
    #     })
    #     print(f"Message sent successfully: {response}")
    # except Exception as e:
    #     print(f"Error sending message: {e}")

    print("Basic usage example finished.")
