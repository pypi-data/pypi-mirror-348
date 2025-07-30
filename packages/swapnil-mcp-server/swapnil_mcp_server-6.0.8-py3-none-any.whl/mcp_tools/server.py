from mcp.server.fastmcp import FastMCP
import win32com.client
from datetime import datetime

mcp = FastMCP("MCP_Tools")

@mcp.list_tools()
def list_tools():
    """List all tools in the MCP server."""
    return mcp.tools


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
    #appointment.RequiredAttendees = "sachin.datir@amdocs.com"
    appointment.OptionalAttendees = ""
    #appointment.Categories = "Meeting"
    appointment.Sensitivity = 0
    appointment.Save()
    appointment.Send()
    return f"Meeting with subject '{subject}' set from {start_date} to {end_date}."


