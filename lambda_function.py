import boto3
import json
import base64
import os

BASE_PATH = '/act5/api/v1'
GET_PATH = f'{BASE_PATH}/get'
PUT_PATH = f'{BASE_PATH}/put'
VIEW_PATH = f'{BASE_PATH}/view'
BUCKET_NAME = os.environ['s3_bucket_name']
s3 = boto3.client('s3')

def _get_object_key(owner, file_name):
    """Constructs the object key for a file based on owner and name."""
    return f"{owner}/{file_name}"

def list_files_for_owner(owner):
    files = []
    prefix = f"{owner}/"  # Assuming folder names are based on owners
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    for obj in response.get('Contents', []):
        files.append(obj['Key'].split('/')[-1])
    
    return files[1:]


def get_file_url(owner, file_name):
    """Generates a presigned URL for downloading a file."""
    files = list_files_for_owner(owner)
    file_key = _get_object_key(owner, file_name)
    
    if file_name not in files:
        return None
    file_key = f'{owner}/{file_name}'
    try:
        file_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': file_key}, ExpiresIn=3600)
        return file_url
    except Exception as e:
        print(f"Error generating URL for {file_key}: {e}")
        return None


def create_folder(folder_path):
    """Creates a folder in the bucket, ignoring errors if it already exists."""
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=folder_path)
    except Exception as e:
        print(f"Error creating folder {folder_path}: {e}")


def upload_file_to_s3(file_content, file_key):
    """Uploads a file to S3 with the specified key."""
    try:
        s3.put_object(Body=file_content, Bucket=BUCKET_NAME, Key=file_key)
    except Exception as e:
        print(f"Error uploading file {file_key}: {e}")


def lambda_handler(event, context):
    """Handles API requests for file operations."""
    try:
        path = event['path']
        body = json.loads(event["body"])

        if path == PUT_PATH:
            return _handle_put_request(body)
        elif path == GET_PATH:
            return _handle_get_request(body)
        elif path == VIEW_PATH:
            return _handle_view_request(body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid path'})
            }
    except Exception as e:
        print(f"Error handling lambda request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }


def _handle_put_request(body):
    """Handles PUT requests for uploading files."""
    try:
        owner = body.get('owner')
        file_name = body.get('file_name')
        file = body.get('file')

        if not all([owner, file_name, file]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        folder_path = _get_object_key(owner, '')
        create_folder(folder_path)

        file_content = base64.b64decode(file)
        file_key = _get_object_key(owner, file_name)
        upload_file_to_s3(file_content, file_key)

        return {
            'statusCode': 200,
            'body': json.dumps({'post': 'OK'})
        }
    except Exception as e:
        print(f"Error handling PUT request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }


def _handle_get_request(body):
    """Handles GET requests for download file URLs."""
    try:
        file_name = body.get('file_name')
        owner = body.get('owner')

        if not all([file_name, owner]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        file_url = get_file_url(owner, file_name)
        if file_url:
            return {
                'statusCode': 200,
                'body': json.dumps({'file_url': file_url})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'File not found'})
            }
    except Exception as e:
        print(f"Error handling GET request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }


def _handle_view_request(body):
    """Handles VIEW requests for listing files for an owner."""
    try:
        owner = body.get('owner')

        if not owner:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing owner field'})
            }

        files = list_files_for_owner(owner)
        return {
            'statusCode': 200,
            'body': json.dumps({'files': files})
        }
    except Exception as e:
        print(f"Error handling VIEW request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
