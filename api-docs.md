# API 1: GET /get

## Purpose

Downloads a specific file owned by the specified user.

## Request Parameters

| Parameter | Required | Description                                   |
|----------|---------|-----------------------------------------------|
| owner    | Yes      | The owner of the file.                        |
| file_name | Yes      | The name of the file to download.             |

## Success Response

The content of the requested file, with the Content-Type header set to the appropriate file type.

## Error Response

- Status code 404: File not found.
- Status code 403: Unauthorized access.
- Other status codes as appropriate.

## Example Usage

```bash
curl --request GET \
  --url {GATEWAY_ENDPOINT}/act5/api/v1/get) \
  --header 'Content-Type: application/json' \
  --data '{
    "owner": "johndoe",
    "file_name": "my_image.jpg"
  }' > downloaded_image.jpg
```

# API 2: GET /view

## Purpose

Lists all files owned by the specified user.

## Request Parameters

| Parameter | Required | Description                                   |
|----------|---------|-----------------------------------------------|
| owner    | Yes      | The owner of the files to list.                |

## Success Response

An array of JSON objects, each containing:

- `owner`: The owner of the file.
- `file_name`: The name of the file.
- `file_size`: The size of the file (in bytes).

## Error Response

- Status code 403: Unauthorized access.
- Other status codes as appropriate.

## Example Usage

```bash
curl --request GET \
  --url {GATEWAY_ENDPOINT}/act5/api/v1/view) \
  --header 'Content-Type: application/json' \
  --data '{
    "owner": "johndoe"
  }'
```

## **API 3: PUT /put**

**Purpose:**

- Uploads a new file owned by the specified user.

**Request Parameters:**

| Parameter | Required | Description |
| --- | --- | --- |
| owner | Yes | The owner of the file to upload. |
| file_name | Yes | The name of the file to upload, including the file extension. |
| file | Yes | Base64-encoded content of the file to upload. |

**Success Response:**

- Status code 200: File uploaded successfully.
- Optional response body containing information about the uploaded file (e.g., ID, size).

**Error Response:**

- Status code 400: Bad request (e.g., invalid parameters, missing data).
- Status code 403: Unauthorized access.
- Status code 413: Payload too large.
- Other status codes as appropriate.

**Example Usage:**

```bash
curl --request PUT \
  --url {GATEWAY_ENDPOINT}/act5/api/v1/put \
  --header 'Content-Type: application/json' \
  --data '{
    "owner": "johndoe",
    "file_name": "my_image.jpg",
    "file": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII="
  }'
```
