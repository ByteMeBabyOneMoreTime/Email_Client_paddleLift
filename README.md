# GetSetDeployed Email API

## Overview

GetSetDeployed Email API provides an enterprise-grade email delivery infrastructure with a developer-first API. Built for modern applications, it ensures reliable and secure email sending capabilities.

## Features

- **API Endpoints**: Simple POST endpoint for email sending with comprehensive response handling.
- **Multi-Language Support**: Support for Python, JavaScript, cURL, and more programming languages.
- **Security**: HTTPS encryption, rate limiting, and secure SMTP credential handling.
- **Reliable Delivery**: High deliverability rates with real-time tracking and reporting.
- **Custom SMTP**: Configure your own SMTP server for complete infrastructure control.
- **Smart Error Handling**: Comprehensive error reporting with actionable solutions.

## Getting Started

### Prerequisites

- Docker installed on your machine.
- `.env` file configured with necessary environment variables.

### Installation

1. Navigate to the `website` folder:
    ```sh
    cd website
    ```

2. Build the Docker image:
    ```sh
    docker build -t getsetdeployed.email .
    ```

3. Run the Docker container:
    ```sh
    docker run -p 8000:8000 --env-file .env getsetdeployed.email
    ```

## API Documentation

### Endpoint

- **POST** `https://email.getsetdeployed.com/send`

### Request Body

```json
{
    "id": "string",
    "subject": "string",
    "body": "string (HTML supported)",
    "recipient_list": ["email1@example.com", "email2@example.com"],
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "use_tls": true,
    "use_ssl": false,
    "email_host_user": "your-email@example.com",
    "email_host_password": "your-password"
}
```

## Example Usage

### cURL Example

```sh
curl -X POST https://email.getsetdeployed.com/send \
  -H "Content-Type: application/json" \
  -d '{
    "id": "your-email-id",
    "subject": "Test Email",
    "body": "<p>Hello, World!</p>",
    "recipient_list": ["recipient@example.com"],
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "use_tls": true,
    "use_ssl": false,
    "email_host_user": "your-email@example.com",
    "email_host_password": "your-password"
}'
```

### React Example

```javascript
import axios from "axios";

const sendEmail = async () => {
  try {
    const response = await axios.post("https://email.getsetdeployed.com/send", {
      id: "your-email-id",
      subject: "Test Email",
      body: "<p>Hello, World!</p>",
      recipient_list: ["recipient@example.com"],
      smtp_host: "smtp.example.com",
      smtp_port: 587,
      use_tls: true,
      use_ssl: false,
      email_host_user: "your-email@example.com",
      email_host_password: "your-password",
    });
    console.log("Email sent successfully:", response.data);
  } catch (error) {
    console.error("Error sending email:", error);
  }
};

sendEmail();
```

### Python Example

```python
import requests

url = "https://email.getsetdeployed.com/send"

payload = {
    "id": "your-email-id",
    "subject": "Test Email",
    "body": "<p>Hello, World!</p>",
    "recipient_list": ["recipient@example.com"],
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "use_tls": True,
    "use_ssl": False,
    "email_host_user": "your-email@example.com",
    "email_host_password": "your-password"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Email sent successfully:", response.json())
else:
    print("Error sending email:", response.status_code, response.text)
```

## Contact

Have questions? We'd love to hear from you.

- **Email**: snehasish@getsetdeployed.com
- **Phone**: +91 9875609901
- **Location**: 123 Developer Street, Tech City, 12345

## License

© 2024 GetSetDeployed. All rights reserved.
