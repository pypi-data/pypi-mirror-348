from enum import Enum
from zoneinfo import ZoneInfo


class DestinationShort(str, Enum):
    WALT_DISNEY_WORLD = "wdw"
    DISNEYLAND_RESORT = "dlr"


class CouchbaseChannels(str, Enum):
    FACILITIES = "facilities"
    FACILITY_STATUS = "facilitystatus"
    CALENDAR = "calendar"
    FORECASTED_WAIT_TIME = "forecastedwaittimes"
    TODAY = "today"


def get_complete_channel_id(
    destination_short: DestinationShort, channel: CouchbaseChannels, version: str, is_multi_language: bool
) -> str:
    channel_id = f"{destination_short.value}.{channel.value}.{version}"

    if is_multi_language:
        channel_id += ".en_us"

    return channel_id


class WDWCouchbaseChannels(str, Enum):
    FACILITIES = get_complete_channel_id(DestinationShort.WALT_DISNEY_WORLD, CouchbaseChannels.FACILITIES, "1_0", True)
    """Walt Disney World Facilities Channel"""
    FACILITY_STATUS = get_complete_channel_id(
        DestinationShort.WALT_DISNEY_WORLD, CouchbaseChannels.FACILITY_STATUS, "1_0", False
    )
    """Walt Disney World Facility Status Channel"""
    CALENDAR = get_complete_channel_id(DestinationShort.WALT_DISNEY_WORLD, CouchbaseChannels.CALENDAR, "1_0", False)
    """Walt Disney World Calendar Channel"""
    FORECASTED_WAIT_TIME = get_complete_channel_id(
        DestinationShort.WALT_DISNEY_WORLD, CouchbaseChannels.FORECASTED_WAIT_TIME, "1_0", True
    )
    """Walt Disney World Forecasted Wait Time Channel"""
    TODAY = get_complete_channel_id(DestinationShort.WALT_DISNEY_WORLD, CouchbaseChannels.TODAY, "1_0", False)
    """Walt Disney World Today Channel"""


class DLRCouchbaseChannels(str, Enum):
    FACILITIES = get_complete_channel_id(DestinationShort.DISNEYLAND_RESORT, CouchbaseChannels.FACILITIES, "1_0", True)
    """Disneyland Resort Facilities Channel"""
    FACILITY_STATUS = get_complete_channel_id(
        DestinationShort.DISNEYLAND_RESORT, CouchbaseChannels.FACILITY_STATUS, "1_0", False
    )
    """Disneyland Resort Facility Status Channel"""
    CALENDAR = get_complete_channel_id(DestinationShort.DISNEYLAND_RESORT, CouchbaseChannels.CALENDAR, "1_0", False)
    """Disneyland Resort Calendar Channel"""
    FORECASTED_WAIT_TIME = get_complete_channel_id(
        DestinationShort.DISNEYLAND_RESORT, CouchbaseChannels.FORECASTED_WAIT_TIME, "1_0", True
    )
    """Disneyland Resort Forecasted Wait Time Channel"""
    TODAY = get_complete_channel_id(DestinationShort.DISNEYLAND_RESORT, CouchbaseChannels.TODAY, "1_0", False)
    """Disneyland Resort Today Channel"""


class DestinationTimezones(Enum):
    WALT_DISNEY_WORLD = ZoneInfo("America/New_York")
    """Walt Disney World Timezone"""
    DISNEYLAND_RESORT = ZoneInfo("America/Los_Angeles")
    """Disneyland Resort Timezone"""
