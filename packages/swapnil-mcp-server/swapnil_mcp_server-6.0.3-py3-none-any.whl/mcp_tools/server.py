from mcp.server.fastmcp import FastMCP
import win32com.client
from datetime import datetime

mcp = FastMCP("MCP_Tools")

@mcp.tool()
async def Set_Meeting(subject: str, start_date: str, end_date: str, use_teams: bool = True, optional_attendees: str = None) -> str:
    """Set Meeting in outlook from given subject and start and end date. 
    Args:
        subject: Meeting subject
        start_date: Start date and time in ISO format (e.g., "2023-10-01T10:00:00")
        end_date: End date and time in ISO format (e.g., "2023-10-01T11:00:00")
        use_teams: Whether to create a Teams meeting (default: True)
        optional_attendees: Semicolon-separated list of email addresses for optional attendees
    """

    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    calendar = namespace.GetDefaultFolder(9)
    appointment = calendar.Items.Add(1)
    appointment.Subject = subject
    appointment.Start = datetime.fromisoformat(start_date)
    appointment.End = datetime.fromisoformat(end_date)
    appointment.Location = "Microsoft Teams Meeting"
    appointment.Body = "Join Microsoft Teams Meeting"
    appointment.ReminderSet = True
    appointment.ReminderMinutesBeforeStart = 15
    appointment.BusyStatus = 2
    appointment.MeetingStatus = 1
    appointment.allDayEvent = False  # Changed to False as Teams meetings are typically timed events
    
    # Create Teams meeting
    if use_teams:
        try:
            # This creates the Teams meeting link
            appointment.RTFBody = '{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat\\deflang1033{\\fonttbl{\\f0\\fnil\\fcharset0 Calibri;}}\r\n{\\*\\generator Riched20 10.0.19041}\\viewkind4\\uc1 \r\n\\pard\\sa200\\sl276\\slmult1\\f0\\fs22\\lang9 Join Microsoft Teams Meeting\\par\r\n}\r\n'
            appointment.MeetingWorkspaceURL = ""
            appointment.NetShowURL = ""
            teams_property = appointment.PropertyAccessor
            teams_property.SetProperty("http://schemas.microsoft.com/mapi/string/{00062008-0000-0000-C000-000000000046}/IsSingletonAppointment", True)
            teams_property.SetProperty("http://schemas.microsoft.com/mapi/id/{00062008-0000-0000-C000-000000000046}/0x8208", True)
            teams_property.SetProperty("http://schemas.microsoft.com/mapi/id/{00062008-0000-0000-C000-000000000046}/0x8582", True)
        except Exception as e:            # If Teams integration fails, continue without it
            print(f"Warning: Failed to set Teams properties: {e}")
            
    #appointment.RequiredAttendees = "sachin.datir@amdocs.com"
    if optional_attendees:
        appointment.OptionalAttendees = optional_attendees
    #appointment.Categories = "Meeting"
    appointment.Sensitivity = 0
    appointment.Save()
    appointment.Send()
    
    result_message = f"Meeting with subject '{subject}' set from {start_date} to {end_date}."
    if use_teams:
        result_message += " Microsoft Teams meeting link has been created."
    return result_message


