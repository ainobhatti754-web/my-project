"""
Timezone utilities and configuration
"""

from datetime import datetime
import pytz

# Common timezones configuration
TIMEZONES = {
    "UTC": "UTC",
    "EST": "US/Eastern",
    "CST": "US/Central",
    "MST": "US/Mountain",
    "PST": "US/Pacific",
    "GMT": "Europe/London",
    "CET": "Europe/Paris",
    "IST": "Asia/Kolkata",
    "CST_CN": "Asia/Shanghai",
    "JST": "Asia/Tokyo",
    "AEST": "Australia/Sydney",
}

class TimezoneManager:
    """Manages timezone conversions and operations"""
    
    def __init__(self):
        self.timezones = TIMEZONES.copy()
        self.custom_timezones = {}
    
    def get_time_in_timezone(self, tz_name: str) -> datetime:
        """
        Get current time in specified timezone
        
        Args:
            tz_name: Timezone name (key from TIMEZONES dict or pytz timezone name)
        
        Returns:
            datetime object in the specified timezone
        """
        if tz_name in self.timezones:
            tz_name = self.timezones[tz_name]
        elif tz_name in self.custom_timezones:
            tz_name = self.custom_timezones[tz_name]
        
        try:
            tz = pytz.timezone(tz_name)
            return datetime.now(tz)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {tz_name}")
    
    def add_custom_timezone(self, alias: str, tz_name: str):
        """
        Add a custom timezone alias
        
        Args:
            alias: Short name for the timezone
            tz_name: Pytz timezone name
        """
        try:
            pytz.timezone(tz_name)
            self.custom_timezones[alias] = tz_name
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {tz_name}")
    
    def remove_custom_timezone(self, alias: str):
        """Remove a custom timezone alias"""
        if alias in self.custom_timezones:
            del self.custom_timezones[alias]
    
    def get_all_timezones(self) -> dict:
        """Get all available timezones (default + custom)"""
        all_tz = self.timezones.copy()
        all_tz.update(self.custom_timezones)
        return all_tz
    
    def get_time_diff(self, tz1: str, tz2: str) -> int:
        """
        Get time difference in hours between two timezones
        
        Args:
            tz1: First timezone
            tz2: Second timezone
        
        Returns:
            Difference in hours
        """
        time1 = self.get_time_in_timezone(tz1)
        time2 = self.get_time_in_timezone(tz2)
        
        offset1 = time1.utcoffset().total_seconds() / 3600
        offset2 = time2.utcoffset().total_seconds() / 3600
        
        return int(offset2 - offset1)
    
    def list_timezones(self) -> list:
        """List all available timezone aliases"""
        return sorted(list(self.get_all_timezones().keys()))
