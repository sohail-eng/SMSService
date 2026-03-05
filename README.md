# SMS Service

A premium Flask-based SMS bridging application that connects to an Android device via Firebase.

## Features

- **Premium Web Interface**: Modern, responsive landing page for sending SMS.
- **Android Integration**: Bridges with an Android APK to send messages using local system capabilities.
- **REST API**: Easy-to-integrate API for third-party applications.
- **Pakistani Number Validation**: Built-in support for verifying Pakistani mobile numbers.
- **No Authentication Required**: Quick access for testing and deployment.

## Prerequisites

- Python 3.x
- Firebase account with Realtime Database enabled.
- `google-services.json` placed in the root directory.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SMSService
   ```

2. **Setup virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Firebase Credentials**:
   Place your `google-services.json` file in the root directory.

## Running the Application

### Development Mode
```bash
python3 app.py
```

### Production Mode (PM2 + Gunicorn)
To keep the application running in the background with a production-grade server ([Gunicorn](https://gunicorn.org/)), use PM2:
```bash
pm2 start "gunicorn --bind 0.0.0.0:5000 app:app" --name sms-service --interpreter .venv/bin/python3
```
To check logs: `pm2 logs sms-service`

The application will be available at `http://localhost:5000`.

## API Documentation

See [API_DOCS.md](API_DOCS.md) for detailed information on how to use the REST API.

## Usage

1. Download the APK from the main page.
2. Install it on your Android phone.
3. Open the app to get your **Unique Key**.
4. Use the web form or the REST API to send SMS by providing the unique key, recipient number, and message.
