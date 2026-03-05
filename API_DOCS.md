# SMS Service REST API Documentation

The SMS Service provides a simple REST API to queue SMS requests that will be sent via an Android device running our bridge APK.

## Send SMS

Queues an SMS to be sent to a Pakistani phone number.

- **URL:** `/sms/api/send`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Request Body

| Field | Type | Description |
| :--- | :--- | :--- |
| `unique_key` | String | The unique ID displayed in the Android APK. |
| `phone_number` | String | Pakistani mobile number (Formats: `03xx...`, `+923xx...`, `923xx...`). |
| `message` | String | The text content of the SMS. |

**Example Request:**

```json
{
  "unique_key": "3099486",
  "phone_number": "03451234567",
  "message": "Hello from the API!"
}
```

### Response

#### Success (200 OK)

```json
{
  "success": true,
  "message": "SMS request queued successfully!"
}
```

#### Error (400 Bad Request / 500 Internal Server Error)

```json
{
  "success": false,
  "error": "Detailed error message here"
}
```

## Integration Examples

### Python (Requests)

```python
import requests

url = "http://localhost:5000/sms/api/send"
data = {
    "unique_key": "YOUR_DEVICE_KEY",
    "phone_number": "03451234567",
    "message": "Automated SMS test"
}

response = requests.post(url, json=data)
print(response.json())
```

### Curl

```bash
curl -X POST http://localhost:5000/sms/api/send \
-H "Content-Type: application/json" \
-d '{
  "unique_key": "3099486",
  "phone_number": "03451234567",
  "message": "Test Message"
}'
```
