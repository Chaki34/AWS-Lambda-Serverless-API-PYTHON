# CloudAPI – API Testing Guide

Replace `YOUR_API_INVOKE_URL` with the Invoke URL shown by API Gateway after deployment.

| Method | URL | Expected result |
|---|---|---|
| GET | `YOUR_API_INVOKE_URL/` | API information and endpoint list |
| GET | `YOUR_API_INVOKE_URL/hello` | Welcome message |
| GET | `YOUR_API_INVOKE_URL/status` | `health: healthy` and UTC timestamp |
| POST | `YOUR_API_INVOKE_URL/greet` | Personalized greeting |

## Postman: POST /greet

1. Select **POST**.
2. Enter `YOUR_API_INVOKE_URL/greet`.
3. Select **Body → raw → JSON**.
4. Send:

```json
{
  "name": "Debmalya"
}
```

Expected response (the message and service fields should match):

```json
{
  "status": "success",
  "message": "Hello, Debmalya!",
  "service": "AWS Lambda",
  "architecture": "Serverless"
}
```

## Negative test

Send `{}` to `POST /greet`. Expected HTTP status: `400`, with a validation message.

Send malformed JSON such as `{not-json`. Expected HTTP status: `400`.

Request a route that does not exist. Expected HTTP status: `404`.

Record the actual HTTP status and response in your submission screenshots.
