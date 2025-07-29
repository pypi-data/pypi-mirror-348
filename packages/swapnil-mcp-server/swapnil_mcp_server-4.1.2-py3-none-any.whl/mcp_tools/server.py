from mcp.server.fastmcp import FastMCP
import httpx
import os 
import requests
from dotenv import load_dotenv 
from twilio.rest import Client
from datetime import datetime

mcp = FastMCP("MCP_Tools")

@mcp.tool()
async def get_Activities(unit : str) -> str:
    """Get Latest Activities for UNIT
    Args:
        unit: Unit Name
    """
    load_dotenv()     
    httpProxy = os.environ.get("HTTP_PROXY", "http://genproxy.corp.amdocs.com:8080")
    httpsProxy = os.environ.get("HTTPS_PROXY", "http://genproxy.corp.amdocs.com:8080")   
    proxies = {
    "http": httpProxy,
    "https": httpsProxy,
    }
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Activities'
    response= requests.get(url,proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        return f"Activities For Unit {unit} are : {data})"
    else:
        return f"No Activities Info. Error: {response.status_code}"
     
@mcp.tool()
async def get_SMS_Logs(count : str, status : str = "delivered") -> str:
    """Get Todays SMS Logs from given count 
    Args:
        count: total number of logs to be fetched
        status: status of the logs (e.g., "delivered", "failed", "sent", "queued")
    """
    load_dotenv()
    account_sid = os.environ.get("SMS_ACCOUNT_SID")
    auth_token = os.environ.get("SMS_AUTH_TOKEN")
    
    if not account_sid or not auth_token:
        return "Error: Missing Twilio credentials. Please set SMS_ACCOUNT_SID and SMS_AUTH_TOKEN environment variables."
    
    try:
        client = Client(account_sid, auth_token)
        
        # Validate count parameter
        try:
            count = int(count)
            if count <= 0:
                return "Error: Count must be a positive integer."
        except ValueError:
            return "Error: Count must be a valid integer."
            
        # Valid status values for Twilio
        valid_statuses = ["queued", "sending", "sent", "delivered", "undelivered", "failed", "received"]
        if status not in valid_statuses:
            return f"Error: Invalid status. Valid values are: {', '.join(valid_statuses)}"
            
        all_messages = client.messages.list(
            date_sent_after=datetime.today().strftime('%Y-%m-%d'),
            limit=count, 
            status=status
        )
        
        if not all_messages:
            return f"No SMS logs found with status '{status}' for today."
            
        # Format all messages
        formatted_messages = [f"From: {message.from_}, To: {message.to}, Body: {message.body}" for message in all_messages]
        return f"SMS Logs are: {formatted_messages}"
        
    except Exception as e:
        return f"Error retrieving SMS logs: {str(e)}"

@mcp.tool()
#send sms to number
async def send_SMS(to : str, body : str) -> str:
    """Send SMS to given number
    Args:
        to: Number to send sms
        body: Message to be sent
    """
    account_sid = os.environ.get("SMS_ACCOUNT_SID")
    auth_token = os.environ.get("SMS_AUTH_TOKEN") 
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_='amdocs',
        to=to
    )
    return f"Message sent with SID: {message.sid}"


