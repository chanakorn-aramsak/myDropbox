import base64
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_GATEWAY = os.getenv("API_GATEWAY") + '/act5/api/v1'


def get_file_content_base64(file_path):
    """Reads a file and returns its base64 encoded content."""
    try:
        with open(file_path, 'rb') as file:
            file_content_binary = file.read()
            return base64.b64encode(file_content_binary).decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def make_api_request(method, endpoint, data=None):
    """Makes an API request and returns the response status code and content."""
    url = f"{API_GATEWAY}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None, None

def view_files(owner="p"):
    """Views files for a specific owner."""
    if not owner:
        print("Owner's name cannot be empty.")
        return

    data = {'owner': owner}
    status_code, files = make_api_request('GET', 'view', data)
    print(files,type(files))
    if status_code == 200 and files:
        for file in files['files']:
            print(file)
    else:
        print("No files found for this owner.")

def upload_file(file_name):
    """Uploads a file to the API."""
    file_path = f"./{file_name}"
    file_content = get_file_content_base64(file_path)

    if not file_content:
        return

    data = {
        'owner': "p",  
        'file_name': file_name,
        'file': file_content
    }

    status_code, _ = make_api_request('PUT', 'put', data)
    if status_code == 200:
        print("File uploaded successfully.")

def download_file(file_name, owner):
    """Downloads a file from the API."""
    data = {'owner': owner, 'file_name': file_name}
    response = make_api_request('GET', 'get', data)

    if not response:
        return
    json_data = response[1]

    # Access the 'file_url' key in the JSON data
    file_url = json_data.get('file_url')
    if file_url:
        print("Downloading file...")
        response = requests.get(file_url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("File not found.")



def main():
    """Handles user interaction in the command-line interface."""
    print("Welcome to myDropbox Application")
    print("============================================")
    print("Available commands:")
    print("  - newuser username password password: Create a new user")
    print("  - login username password: Login to your account")
    print("  - put filename: Upload a file")
    print("  - get filename username: Download a file")
    print("  - view: List your files")
    print("  - quit: Exit the program")
    print("============================================")

    while True:
        command = input(">> ")
        split_command = command.split(" ")

        if command == "quit":
            print("============================================")
            break
        elif (split_command[0] == "put" and len(split_command) == 2):
            upload_file(split_command[1])
        elif (split_command[0] == "get" and len(split_command) == 3):
            print(split_command[1], split_command[2])
            download_file(split_command[1], split_command[2])
        elif (split_command[0] == "view"):
            view_files()
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
