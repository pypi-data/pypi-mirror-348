from mcp.server.fastmcp import FastMCP
import win32com.client
from datetime import datetime
from typing import Any, Dict
import requests 
import logging
import os 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = {
    "http": "http://genproxy.corp.amdocs.com:8080", 
    "https": "http://genproxy.corp.amdocs.com:8080",
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mcp_server")

mcp = FastMCP("MCP_Tools")


@mcp.tool()
async def Get_Project_Repositories(project_name: str) -> str:
    """Get project repositories from Azure DevOps.
    
    Args:
        project_name: Name of the Azure DevOps project
        
    Returns:
        List of repositories in the specified project
    """
    try:
        # Validate input
        if not project_name:
            return "Error: Project name is required"
        
        logger.info(f"Fetching repositories for project: {project_name}")
        TFS_PAT = os.getenv("TFS_PAT", "vf6k5xhrhdtba5elqr6f3niswddtuuikabvoubwa2zkujwuq224a")

        os.environ['HTTP_PROXY'] = ''
        os.environ['HTTPS_PROXY'] = ''

        REPOSITORY_URL = f"https://mistfs/misamdocs/{project_name}/_apis/git/repositories"
        repository_response = requests.get(
                REPOSITORY_URL,
                auth=("", TFS_PAT),
                verify=False
        )
        repository_response.raise_for_status()
        repository_data = repository_response.json()
          
        if repository_data and "value" in repository_data:
            repositories = repository_data.get('value', [])
            repositorynames = [repository['name'] for repository in repositories]
            logger.info(f"Successfully fetched repositories for project: {project_name}")
            return repositorynames
        else:
            logger.warning(f"No repositories found for project: {project_name}")
            return "No repositories found or error occurred"
    
    except Exception as e:
        logger.exception(f"Error fetching repositories for {project_name}: {str(e)}")
        return f"Error fetching repositories: {str(e)}"

@mcp.tool()
async def get_weather(city: str) -> Dict[str, Any]:
    """Get weather information for a city.
    
    Args:
        city: Any city name, not limited to Indian cities
        
    Returns:
        Weather data for the requested city
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "9714c902c784730338c95bd3140cc6ed")
    #https://api.openweathermap.org/data/2.5/weather?q=London&appid=bd5e378503939ddaee76f12ad7a97608&units=metric
    units = os.getenv("WEATHER_UNITS", "metric")  # Use metric by default for Celsius
    
    try:
        logger.info(f"Fetching weather data for city: {city}")
        
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&units={units}&appid={api_key}"
        )
        
        response = requests.get(
            url, 
            timeout=30.0, 
            verify=False, 
            proxies=PROXIES
        )
        
        response.raise_for_status()
        
        # Parse and format the weather data
        weather_data = response.json()
        
        # Format the response for better readability
        formatted_data = {
            "location": f"{weather_data.get('name', city)}, {weather_data.get('sys', {}).get('country', 'Unknown')}",
            "temperature": {
                "current": weather_data.get('main', {}).get('temp'),
                "feels_like": weather_data.get('main', {}).get('feels_like'),
                "min": weather_data.get('main', {}).get('temp_min'),
                "max": weather_data.get('main', {}).get('temp_max')
            },
            "humidity": weather_data.get('main', {}).get('humidity'),
            "wind": {
                "speed": weather_data.get('wind', {}).get('speed'),
                "direction": weather_data.get('wind', {}).get('deg')
            },
            "description": weather_data.get('weather', [{}])[0].get('description', 'Unknown'),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Successfully retrieved weather for {city}")
        return formatted_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data for {city}: {str(e)}")
        return {"error": f"Failed to fetch weather data: {str(e)}"}
    except Exception as e:
        logger.exception(f"Unexpected error in get_weather for {city}: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool()
async def Set_Meeting(subject: str, start_date: str, end_date: str) -> str:
    """Set Meeting in outlook from given subject and start and end date. 
    Args:
        subject: Meeting subject
        start_date: Start date and time in ISO format (e.g., "2023-10-01T10:00:00")
        end_date: End date and time in ISO format (e.g., "2023-10-01T11:00:00")
    """

    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    calendar = namespace.GetDefaultFolder(9)
    appointment = calendar.Items.Add(1)
    appointment.Subject = subject
    appointment.Start = datetime.fromisoformat(start_date)
    appointment.End = datetime.fromisoformat(end_date)
    appointment.Location = ""
    appointment.Body = "Meeting Body"
    appointment.ReminderSet = True
    appointment.ReminderMinutesBeforeStart = 15
    appointment.BusyStatus = 3
    appointment.MeetingStatus = 1
    appointment.allDayEvent = True
    appointment.OptionalAttendees = ""
    appointment.Sensitivity = 0
    appointment.Save()
    appointment.Send()
    return f"Meeting with subject '{subject}' set from {start_date} to {end_date}."


