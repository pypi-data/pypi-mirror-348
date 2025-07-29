# SWAPNIL MCP Server 🚀

<div align="center">

**A powerful Model Context Protocol (MCP) server implementation for integrating communication tools**

[![License](https://img.shields.io/github/license/erikhoward/azure-fhir-mcp-server)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/modelcontextprotocol/spec)
[![Twilio](https://img.shields.io/badge/Twilio-SMS_Enabled-F22F46.svg)](https://www.twilio.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## 📋 Overview

SWAPNIL MCP Server is a robust implementation of the Model Context Protocol that provides seamless integration with communication services. It enables AI models to interact with SMS functionality and activity tracking through a standardized interface.

## 🛠️ Setup & Installation

### Requirements

- Python 3.13 or higher
- Twilio account (for SMS functionality)
- Internet connection (proxy support available)

### Quick Start

```bash
# Install the package
pip install swapnil-mcp-server

# Set up environment variables (recommended)
set SMS_ACCOUNT_SID=your_twilio_sid
set SMS_AUTH_TOKEN=your_twilio_token

# Start the server
python -m mcp_tools
```

## 🧰 Available MCP Tools

This server exposes a set of powerful tools through the Model Context Protocol interface:

### 📊 Activity Tracking

<details>
<summary><strong>get_Activities</strong> - Fetch latest activities for a specific unit</summary>

```python
async def get_Activities(unit: str) -> str
```

**Parameters:**
- `unit`: The name of the unit to retrieve activities for

**Returns:**
- A formatted string containing activity data for the specified unit

**Example:**
```python
# Fetch activities for the "Sales" unit
result = await get_Activities("Sales")
print(result)  # Activities for unit Sales: [...]
```
</details>

### 📱 SMS Management

<details>
<summary><strong>get_SMS_Logs</strong> - Retrieve recent SMS message logs</summary>

```python
async def get_SMS_Logs(limit: str) -> str
```

**Parameters:**
- `limit`: The number of SMS logs to fetch

**Returns:**
- A formatted string containing SMS log data

**Example:**
```python
# Get the 5 most recent SMS logs
logs = await get_SMS_Logs("5")
print(logs)  # Recent SMS logs: [...]
```
</details>

<details>
<summary><strong>send_SMS</strong> - Send a text message to any phone number</summary>

```python
async def send_SMS(to: str, body: str) -> str
```

**Parameters:**
- `to`: The phone number to send the SMS to (format: +1XXXXXXXXXX)
- `body`: The message content to be sent

**Returns:**
- A confirmation message with the message SID

**Example:**
```python
# Send a notification message
result = await send_SMS("+12125551234", "Your package has been delivered!")
print(result)  # Message sent! SID: SM123456789
```
</details>

## 📋 Detailed Usage Guide

### Configuration

Set the following environment variables before starting the server:

| Variable | Description | Required |
|----------|-------------|----------|
| `SMS_ACCOUNT_SID` | Your Twilio account SID | Yes (for SMS) |
| `SMS_AUTH_TOKEN` | Your Twilio authentication token | Yes (for SMS) |
| `HTTP_PROXY` | HTTP proxy URL if needed | No |
| `HTTPS_PROXY` | HTTPS proxy URL if needed | No |

### Running the Server

Start the server with the following command:

```bash
python -m mcp_tools
```

### Integration with MCP Clients

Connect using any MCP-compatible client. Here's a simple Python example:

```python
from mcp.client import Client

async def main():
    # Connect to the SWAPNIL MCP Server
    client = await Client.connect("http://localhost:8000")
    
    # Use the available tools
    activities = await client.get_Activities("Marketing")
    print(activities)
    
    # Send an SMS
    sms_result = await client.send_SMS("+12125551234", "Hello from SWAPNIL MCP!")
    print(sms_result)
```

## 🔍 Troubleshooting

Common issues and solutions:

- **Connection errors**: Ensure the server is running and accessible
- **SMS failures**: Verify your Twilio credentials and phone number format
- **Proxy issues**: Check your network settings and proxy configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for enhancing AI-powered communication**

<p align="center">
  <a href="https://github.com/modelcontextprotocol/spec">MCP Specification</a> •
  <a href="https://www.twilio.com/">Twilio API</a> •
  <a href="https://fastapi.tiangolo.com/">FastAPI</a>
</p>

<p align="center">
  <strong>Author:</strong> <a href="https://www.linkedin.com/in/dagadeswapnil/">Swapnil Dagade</a> <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn" width="16" height="16">
</p>

</div>
