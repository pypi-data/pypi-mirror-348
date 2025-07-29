# SWAPNIL MCP Server 🚀

<div align="center">

**A powerful Model Context Protocol (MCP) server implementation for Outlook Calendar integration**

[![License](https://img.shields.io/github/license/erikhoward/azure-fhir-mcp-server)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/modelcontextprotocol/spec)
[![Outlook](https://img.shields.io/badge/Outlook-Calendar_Integration-0078D4.svg)](https://office.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## 📋 Overview

SWAPNIL MCP Server is a robust implementation of the Model Context Protocol that provides seamless integration with Microsoft Outlook Calendar. It enables AI models to create and schedule meetings through a standardized interface.

## 🛠️ Setup & Installation

### Requirements

- Python 3.9 or higher
- Microsoft Outlook (installed on the system)
- Internet connection (proxy support available)

### Quick Start

```bash
# Install the package
pip install swapnil-mcp-server

# Start the server
python -m mcp_tools
```

## 🧰 Available MCP Tools

This server exposes a powerful tool through the Model Context Protocol interface:

### 📅 Outlook Calendar

<details>
<summary><strong>Set_Meeting</strong> - Create and schedule a meeting in Microsoft Outlook</summary>

```python
async def Set_Meeting(subject: str, start_date: str, end_date: str) -> str
```

**Parameters:**
- `subject`: Meeting subject
- `start_date`: Start date and time in ISO format (e.g., "2023-10-01T10:00:00")
- `end_date`: End date and time in ISO format (e.g., "2023-10-01T11:00:00")

**Returns:**
- A confirmation message with meeting details

**Example:**
```python
# Schedule a team meeting
result = await Set_Meeting(
    "Team Weekly Sync", 
    "2023-10-01T10:00:00", 
    "2023-10-01T11:00:00"
)
print(result)  # Meeting with subject 'Team Weekly Sync' set from 2023-10-01T10:00:00 to 2023-10-01T11:00:00.
```
</details>

## 📋 Detailed Usage Guide

### Configuration

No specific environment variables are required to run the server. However, Microsoft Outlook must be installed and configured on the system.

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
    
    # Schedule a meeting
    meeting_result = await client.Set_Meeting(
        "Team Retrospective",
        "2023-10-15T14:00:00",
        "2023-10-15T15:00:00"
    )
    print(meeting_result)
```

## 🔍 Troubleshooting

Common issues and solutions:

- **Connection errors**: Ensure the server is running and accessible
- **Outlook integration issues**: Verify Outlook is installed and properly configured
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
  <a href="https://office.com">Microsoft Outlook</a> •
  <a href="https://fastapi.tiangolo.com/">FastAPI</a>
</p>

<p align="center">
  <strong>Author:</strong> <a href="https://www.linkedin.com/in/dagadeswapnil/">Swapnil Dagade</a> <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn" width="16" height="16">
</p>

</div>
