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
async def get_SMS_Logs(count : str, status : str) -> str:
    """Get Todays SMS Logs from given count 
    Args:
        count: number of logs to be fetched
        status: status of the logs
    """
    account_sid = os.environ.get("SMS_ACCOUNT_SID")
    auth_token = os.environ.get("SMS_AUTH_TOKEN") 

    client = Client(account_sid, auth_token)
    all_messages = []
    all_messages = client.messages.list(date_sent_after=datetime.today().strftime('%Y-%m-%d'),limit=int(count), status=status)

    #format all_messages
    all_messages = [f"From: {message.from_}, To: {message.to}, Body: {message.body}" for message in all_messages]
    return f"SMS Logs are : {all_messages}"

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


