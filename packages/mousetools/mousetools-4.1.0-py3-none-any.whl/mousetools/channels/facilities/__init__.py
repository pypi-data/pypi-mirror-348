import logging
import typing
from collections.abc import Generator
from datetime import datetime, time, timedelta
from enum import Enum
from zoneinfo import ZoneInfo

from dateutil.parser import isoparse

from mousetools.api.menu import Menus
from mousetools.channels import CouchbaseChannel
from mousetools.channels.calendar import CalendarChildChannel
from mousetools.channels.enums import (
    CouchbaseChannels,
    DestinationTimezones,
    DLRCouchbaseChannels,
    WDWCouchbaseChannels,
)
from mousetools.channels.facilitystatus import FacilityStatusChildChannel
from mousetools.enums import DestinationShort, EntityType
from mousetools.mixins.couchbase import CouchbaseMixin

logger = logging.getLogger(__name__)


class FacilityChildChannel(CouchbaseMixin):
    """Base class for all Facility Child Channels. Subclasses like Attraction, Restaurant, Entertainment, etc. extend this class.

    Example:

        >>> from mousetools.channels.facilities import AttractionFacilityChild, ThemeParkFacilityChild
        >>> a = AttractionFacilityChild("wdw.facilities.1_0.en_us.attraction.80010177;entityType=Attraction")
        >>> print(a)
        "Attraction: Pirates of the Caribbean (wdw.facilities.1_0.en_us.attraction.80010177;entityType=Attraction)"
        >>> from mousetools.channels.facilities.enums import WaltDisneyWorldParkChannelIds
        >>> d = ThemeParkFacilityChild(WaltDisneyWorldParkChannelIds.MAGIC_KINGDOM, lazy_load=False)
        >>> print(d.coordinates)
        {'latitude': 28.4160036778, 'longitude': -81.5811902834}
    """

    _subclasses: typing.ClassVar[dict[str, type["FacilityChildChannel"]]] = {}

    def __init__(
        self,
        channel_id: str,
        lazy_load: bool = True,
    ):
        """
        Args:
            channel_id (str): Facility Channel ID
            lazy_load (bool, optional): If True, will not pull data until a method or property is called. Defaults to True.
        """
        if isinstance(channel_id, Enum):
            channel_id = channel_id.value

        self.channel_id: str = channel_id
        self.entity_id: str = channel_id.rsplit(".", 1)[-1]

        self._destination_short: DestinationShort = self.channel_id.split(".")[0]
        self._tz: DestinationTimezones = (
            DestinationTimezones.WALT_DISNEY_WORLD
            if self._destination_short == DestinationShort.WALT_DISNEY_WORLD
            else DestinationTimezones.DISNEYLAND_RESORT
        )
        self._refresh_interval: timedelta = timedelta(
            hours=12
        )  # properties are rarely updated, no need to spam the API

        self._cb_data: typing.Optional[dict] = None
        self._cb_data_pull_time: typing.Optional[datetime] = datetime.now(tz=self._tz.value)
        if not lazy_load:
            self.refresh()

        self._today_calendar: typing.Optional[CalendarChildChannel] = None

    def refresh(self) -> None:
        """Pulls initial data if none exists or if it is older than the refresh interval"""
        if self._cb_data is None or datetime.now(tz=self._tz.value) - self.last_update > self._refresh_interval:
            self._cb_data = self.get_channel_data(self.channel_id)
            self._cb_data_pull_time = datetime.now(tz=self._tz.value)

    def pull_today_calendar(self) -> None:
        today = datetime.now(tz=self._tz.value)
        day = today.day
        month = today.month

        calendar_channel_id = f"{WDWCouchbaseChannels.CALENDAR.value if self._destination_short == DestinationShort.WALT_DISNEY_WORLD else DLRCouchbaseChannels.CALENDAR.value}.{day:02}-{month:02}."
        self._today_calendar = CalendarChildChannel(calendar_channel_id)

    @property
    def name(self) -> typing.Optional[str]:
        """
        The name of the entity.

        Returns:
            (typing.Optional[str]): The name of the entity, or None if it was not found.
        """

        self.refresh()
        try:
            return self._cb_data["name"]
        except KeyError:
            logger.debug("No name found for %s", self.channel_id)
            return None

    @property
    def entity_type(self) -> typing.Optional[str]:
        """
        The type of entity this is.

        Returns:
            (typing.Optional[str]): The type of entity this is, or None if it was not found.
        """

        self.refresh()
        try:
            return self._cb_data["type"]
        except KeyError:
            logger.debug("No entity type found for %s", self.channel_id)
            return None

    @property
    def sub_type(self) -> typing.Optional[str]:
        """
        The sub type of entity.

        Returns:
            (typing.Optional[str]): The sub type of entity, or None if it was not found.
        """
        self.refresh()
        try:
            return self._cb_data["subType"]
        except KeyError:
            logger.debug("No sub type found for %s", self.channel_id)
            return None

    @property
    def coordinates(self) -> typing.Optional[dict[str, float]]:
        """
        The coordinates of this entity

        Returns:
            (typing.Optional[dict[str, float]]): A dict with "lat" and "lng" keys containing the coordinates of this entity as floats, or None if no coordinates are found
        """
        self.refresh()
        try:
            return {
                "latitude": float(self._cb_data["latitude"]),
                "longitude": float(self._cb_data["longitude"]),
            }
        except KeyError as e:
            print(e)
            logger.debug("No coordinates found for %s", self.channel_id)
            return None

    @property
    def ancestor_destination_entity_id(self) -> typing.Optional[str]:  # type: ignore
        """
        The id of the ancestor destination of this entity.

        Returns:
            (typing.Optional[str]): The id of the ancestor destination of this entity, or None if it was not found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorDestinationId"]
        except KeyError:
            logger.debug("No ancestor destination id found for %s", self.channel_id)
            return None

    @property
    def ancestor_theme_park_entity_id(self):
        """
        The id of the theme park of this entity.

        Returns:
            (typing.Optional[str]): Theme park id, or None if no such id is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorThemeParkId"]
        except KeyError:
            logger.debug("No ancestor theme park id found for %s", self.channel_id)
            return None

    @property
    def ancestor_water_park_entity_id(self) -> typing.Optional[str]:
        """
        The if of the water park of this entity.

        Returns:
            (typing.Optional[str]): Water park id, or None if no such id is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorWaterParkId"]
        except KeyError:
            logger.debug("No ancestor water park id found for %s", self.channel_id)
            return None

    @property
    def ancestor_resort_entity_id(self) -> typing.Optional[str]:
        """
        The id of the resort of the entity.

        Returns:
            (typing.Optional[str): Resort id, or None if no such id is found.
        """

        self.refresh()
        try:
            return self._cb_data["ancestorResortId"]
        except KeyError:
            logger.debug("No ancestor resort ids found for %s", self.channel_id)
            return None

    @property
    def ancestor_land_entity_id(self) -> typing.Optional[str]:
        """
        The if of the land of this entity.

        Returns:
            (typing.Optional[str]): Land id, or None if no such id is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorLandId"]
        except KeyError:
            logger.debug("No ancestor land id found for %s", self.channel_id)
            return None

    @property
    def ancestor_resort_area_entity_id(self) -> typing.Optional[str]:
        """
        The id of the resort area of this entity.

        Returns:
            (typing.Optional[str]): Resort area id, or None if no such id is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorResortAreaId"]
        except KeyError:
            logger.debug("No ancestor resort area ids found for %s", self.channel_id)
            return None

    @property
    def ancestor_entertainment_venue_entity_id(self) -> typing.Optional[str]:
        """
        The id of entertainment venues of this entity.

        Returns:
            (typing.Optional[str]): Entertainment venue id, or None if no such id is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorEntertainmentVenueId"]
        except KeyError:
            logger.debug("No ancestor entertainment venue ids found for %s", self.channel_id)
            return None

    @property
    def ancestor_restaurant_entity_id(self) -> typing.Optional[str]:
        """
        The id of the restaurant of this entity.

        Returns:
            (typing.Optional[str]): Restaurant id, or None if no such id is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorRestaurantId"]
        except KeyError:
            logger.debug("No ancestor restaurant ids found for %s", self.channel_id)
            return None

    @property
    def ancestor_destination_name(self) -> typing.Optional[str]:
        """
        The name of the destination of this entity.

        Returns:
            (typing.Optional[str]): Destination name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorDestination"]
        except KeyError:
            logger.debug("No ancestor destination name found for %s", self.channel_id)
            return None

    @property
    def ancestor_resort_name(self) -> typing.Optional[str]:
        """
        The name of the resort of this entity.

        Returns:
            (typing.Optional[str]): Resort name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorResort"]
        except KeyError:
            logger.debug("No ancestor resort name found for %s", self.channel_id)
            return None

    @property
    def ancestor_land_name(self) -> typing.Optional[str]:
        """
        The name of the land of this entity.

        Returns:
            (typing.Optional[str]): Land name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorLand"]
        except KeyError:
            logger.debug("No ancestor land name found for %s", self.channel_id)
            return None

    @property
    def ancestor_resort_area_name(self) -> typing.Optional[str]:
        """
        The name of the resort area of this entity.

        Returns:
            (typing.Optional[str]): Resort area name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorResortArea"]
        except KeyError:
            logger.debug("No ancestor resort area name found for %s", self.channel_id)
            return None

    @property
    def ancestor_entertainment_venue_name(self) -> typing.Optional[str]:
        """
        The name of the entertainment venue of this entity.

        Returns:
            (typing.Optional[str]): Entertainment venue name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorEntertainmentVenue"]
        except KeyError:
            logger.debug("No ancestor entertainment venue name found for %s", self.channel_id)
            return None

    @property
    def ancestor_restaurant_name(self) -> typing.Optional[str]:
        """
        The name of the restaurant of this entity.

        Returns:
            (typing.Optional[str]): Restaurant name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorRestaurant"]
        except KeyError:
            logger.debug("No ancestor restaurant name found for %s", self.channel_id)
            return None

    @property
    def ancestor_theme_park_name(self) -> typing.Optional[str]:
        """
        The name of the theme park of this entity.

        Returns:
            (typing.Optional[str]): Theme park name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorThemePark"]
        except KeyError:
            logger.debug("No ancestor theme park name found for %s", self.channel_id)
            return None

    @property
    def ancestor_water_park_name(self) -> typing.Optional[str]:
        """
        The name of the water park of this entity.

        Returns:
            (typing.Optional[str]): Water park name, or None if no such name is found.
        """
        self.refresh()
        try:
            return self._cb_data["ancestorWaterPark"]
        except KeyError:
            logger.debug("No ancestor water park name found for %s", self.channel_id)
            return None

    @property
    def disney_owned(self) -> typing.Optional[bool]:
        """
        Whether the entity is owned by Disney.

        Returns:
            (typing.Optional[bool]): Whether the entity is owned by Disney.
        """
        self.refresh()
        try:
            return self._cb_data["disneyOwned"]
        except KeyError:
            logger.debug("No disney owned found for %s", self.channel_id)
            return None

    @property
    def disney_operated(self) -> typing.Optional[bool]:
        """
        Whether the entity is operated by Disney.

        Returns:
            (typing.Optional[bool]): Whether the entity is operated by Disney.
        """
        self.refresh()
        try:
            return self._cb_data["disneyOperated"]
        except KeyError:
            logger.debug("No disney operated found for %s", self.channel_id)
            return None

    @property
    def admission_required(self) -> typing.Optional[bool]:
        """
        Whether the entity requires admission.

        Returns:
            (typing.Optional[bool]): Whether the entity requires admission.
        """
        self.refresh()
        try:
            return self._cb_data["admissionRequired"]
        except KeyError:
            logger.debug("No admission required found for %s", self.channel_id)
            return None

    @property
    def pre_paid(self) -> typing.Optional[bool]:
        """
        Whether the entity is pre-paid.

        Returns:
            (typing.Optional[bool]): Whether the entity is pre-paid.
        """
        self.refresh()
        try:
            return self._cb_data["prePaid"]
        except KeyError:
            logger.debug("No pre-paid found for %s", self.channel_id)
            return None

    @property
    def timezone(self) -> ZoneInfo:
        """
        The time zone of the entity.

        Returns:
            (ZoneInfo): The time zone of the entity.
        """

        return self._tz.value

    @property
    def related_location_ids(self) -> list[str]:
        """
        The ids of the related locations of this entity.

        Returns:
            (list[str]): The ids of the related locations of this entity.
        """
        # https://api.wdprapps.disney.com/facility-service/entertainments/19322758
        raise NotImplementedError

    @property
    def duration(self) -> typing.Optional[time]:
        """
        The duration of the entity.

        Returns:
            (typing.Optional[time]): The duration of the entity.
        """
        self.refresh()
        try:
            return time.fromisoformat(":".join(self._cb_data["duration"].split(":")[:3]))
        except KeyError:
            logger.debug("No duration found for %s", self.channel_id)
            return None

    @property
    def description(self) -> typing.Optional[str]:
        """The description of the facility.

        Returns:
            (typing.Optional[str]): The description of the entity.
        """
        self.refresh()
        try:
            return self._cb_data["description"]
        except KeyError:
            logger.debug("No description found for %s", self.channel_id)
            return None

    def get_facility_status_channel(self) -> FacilityStatusChildChannel:
        """Get the facility status channel for this entity.

        Returns:
            (FacilityStatusChildChannel): The facility status channel
        """
        channel = (
            WDWCouchbaseChannels.FACILITY_STATUS
            if self._destination_short == DestinationShort.WALT_DISNEY_WORLD
            else DLRCouchbaseChannels.FACILITY_STATUS
        )
        facility_status_channel_id = f"{channel.value}.{self.entity_id}"

        return FacilityStatusChildChannel(facility_status_channel_id)

    @property
    def last_update(self) -> typing.Optional[datetime]:
        """
        The last time the data was updated.

        Returns:
            (typing.Optional[datetime]): The last time the entity's data was updated, or None if no such data exists.
        """
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)

        try:
            tz = (
                DestinationTimezones.WALT_DISNEY_WORLD
                if "wdw" in self.channel_id
                else DestinationTimezones.DISNEYLAND_RESORT
            )
            dt = isoparse(self._cb_data["lastUpdate"])
            dt = dt.replace(tzinfo=tz.value)
            return dt
        except KeyError:
            logger.debug("No last updated found for %s", self.channel_id)
            return self._cb_data_pull_time

    @property
    def sponsor_name(self) -> typing.Optional[str]:
        """The sponsor name of the entity.

        Returns:
            (typing.Optional[str]): The sponsor name of the entity.
        """
        self.refresh()
        try:
            return self._cb_data["sponsorName"]
        except KeyError:
            logger.debug("No sponsor name found for %s", self.channel_id)
            return None

    @property
    def meal_periods(self) -> typing.Optional[list[str]]:
        """
        The meal periods offered by the restaurant.

        Returns:
            (typing.Optional[list[str]]): The meal periods offered by the restaurant.
        """
        self.refresh()
        try:
            return self._cb_data["mealPeriods"]
        except KeyError:
            logger.debug("No meal periods found for %s", self.channel_id)
            return None

    @property
    def menu(self) -> Menus:
        """
        The menu of the restaurant.

        Returns:
            (typing.Optional[Menus]): The menu of the restaurant.
        """
        return Menus(self.channel_id)

    @property
    def detail_image_url(self) -> typing.Optional[str]:
        """The detail image url of the entity.

        Returns:
            (typing.Optional[str]): The detail image url of the entity.
        """
        self.refresh()
        try:
            return self._cb_data["detailImageUrl"]
        except KeyError:
            logger.debug("No detail image url found for %s", self.channel_id)
            return None

    @property
    def list_image_url(self) -> typing.Optional[str]:
        """The list image url of the entity.

        Returns:
            (typing.Optional[str]): The list image url of the entity.
        """
        self.refresh()
        try:
            return self._cb_data["listImageUrl"]
        except KeyError:
            logger.debug("No list image url found for %s", self.channel_id)
            return None

    def get_today_park_hours(self) -> dict:
        self.pull_today_calendar()
        hours = self._today_calendar.get_park_hours(self.entity_id)
        return hours

    def get_today_meal_periods(self) -> dict:
        self.pull_today_calendar()
        meal_periods = self._today_calendar.get_meal_periods(self.entity_id)
        return meal_periods

    def get_today_schedule(self) -> list[dict]:
        self.pull_today_calendar()
        schedule = self._today_calendar.get_facility_schedule(self.entity_id)
        return schedule

    def is_closed_today(self) -> bool:
        self.pull_today_calendar()
        refurb = self._today_calendar.get_refurbishment(self.entity_id)
        closed = self._today_calendar.get_closed(self.entity_id)
        return bool(refurb or closed)

    def __str__(self) -> str:
        return f"{self.entity_type}: {self.name} ({self.channel_id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(channel_id='{self.channel_id}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, FacilityChildChannel):
            return self.channel_id == other.channel_id
        return False

    @classmethod
    def get_subclass(cls, type_name: str) -> type["FacilityChildChannel"]:
        if type_name not in cls._subclasses:
            cls._subclasses[type_name] = type(type_name, (cls,), {"__doc__": f"Class for {type_name} Entities."})
        return cls._subclasses[type_name]


AttractionFacilityChild = FacilityChildChannel.get_subclass("AttractionFacilityChild")
AudioTourFacilityChild = FacilityChildChannel.get_subclass("AudioTourFacilityChild")
BuildingFacilityChild = FacilityChildChannel.get_subclass("BuildingFacilityChild")
BusStopFacilityChild = FacilityChildChannel.get_subclass("BusStopFacilityChild")
DestinationFacilityChild = FacilityChildChannel.get_subclass("DestinationFacilityChild")
DiningEventFacilityChild = FacilityChildChannel.get_subclass("DiningEventFacilityChild")
DinnerShowFacilityChild = FacilityChildChannel.get_subclass("DinnerShowFacilityChild")
EntertainmentFacilityChild = FacilityChildChannel.get_subclass("EntertainmentFacilityChild")
EntertainmentVenueFacilityChild = FacilityChildChannel.get_subclass("EntertainmentVenueFacilityChild")
WaterParkFacilityChild = FacilityChildChannel.get_subclass("WaterParkFacilityChild")
GuestServiceFacilityChild = FacilityChildChannel.get_subclass("GuestServiceFacilityChild")
LandFacilityChild = FacilityChildChannel.get_subclass("LandFacilityChild")
MerchandiseFacilityChild = FacilityChildChannel.get_subclass("MerchandiseFacilityChild")
PhotopassFacilityChild = FacilityChildChannel.get_subclass("PhotopassFacilityChild")
PointOfInterestFacilityChild = FacilityChildChannel.get_subclass("PointOfInterestFacilityChild")
RecreationFacilityChild = FacilityChildChannel.get_subclass("RecreationFacilityChild")
RecreationActivityFacilityChild = FacilityChildChannel.get_subclass("RecreationActivityFacilityChild")
ResortFacilityChild = FacilityChildChannel.get_subclass("ResortFacilityChild")
ResortAreaFacilityChild = FacilityChildChannel.get_subclass("ResortAreaFacilityChild")
SpaFacilityChild = FacilityChildChannel.get_subclass("SpaFacilityChild")
ThemeParkFacilityChild = FacilityChildChannel.get_subclass("ThemeParkFacilityChild")
TourFacilityChild = FacilityChildChannel.get_subclass("TourFacilityChild")
TransportationFacilityChild = FacilityChildChannel.get_subclass("TransportationFacilityChild")
WaterParkFacilityChild = FacilityChildChannel.get_subclass("WaterParkFacilityChild")
RestaurantFacilityChild = FacilityChildChannel.get_subclass("RestaurantFacilityChild")


class FacilityChannel(CouchbaseChannel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_children_channels(self) -> Generator[FacilityChildChannel, None, None]:
        """Gets a list of children channels for the channel.

        Yields:
            typing.Generator[FacilityChildChannel, None, None]: A generator of FacilityChildChannel
        """
        self.refresh()
        for i in self._cb_data["results"]:
            if CouchbaseChannels.FACILITIES in i["id"]:
                yield FacilityChildChannel(i["id"])

    def get_children_attractions(self) -> Generator[AttractionFacilityChild, None, None]:  # type: ignore
        """Get AttractionFacilityChild Children of a Facility

        Yields:
            Generator[AttractionFacilityChild, None, None]: A generator of AttractionFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.ATTRACTION.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield AttractionFacilityChild(i["id"])

    def get_children_audio_tours(self) -> Generator[AudioTourFacilityChild, None, None]:  # type: ignore
        """Get AudioTourFacilityChild Children of a Facility

        Yields:
            Generator[AudioTourFacilityChild, None, None]: A generator of AudioTourFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.AUDIO_TOUR.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield AudioTourFacilityChild(i["id"])

    def get_children_buildings(self) -> Generator[BuildingFacilityChild, None, None]:  # type: ignore
        """Get BuildingFacilityChild Children of a Facility

        Yields:
            Generator[BuildingFacilityChild, None, None]: A generator of BuildingFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.BUILDING.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield BuildingFacilityChild(i["id"])

    def get_children_bus_stops(self) -> Generator[BusStopFacilityChild, None, None]:  # type: ignore
        """Get BusStopFacilityChild Children of a Facility

        Yields:
            Generator[BusStopFacilityChild, None, None]: A generator of BusStopFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.BUS_STOP.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield BusStopFacilityChild(i["id"])

    def get_children_destinations(self) -> Generator[DestinationFacilityChild, None, None]:  # type: ignore
        """Get DestinationFacilityChild Children of a Facility

        Yields:
            Generator[DestinationFacilityChild, None, None]: A generator of DestinationFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.DESTINATION.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield DestinationFacilityChild(i["id"])

    def get_children_dining_events(self) -> Generator[DiningEventFacilityChild, None, None]:  # type: ignore
        """Get DiningEventFacilityChild Children of a Facility

        Yields:
            Generator[DiningEventFacilityChild, None, None]: A generator of DiningEventFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.DINING_EVENT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield DiningEventFacilityChild(i["id"])

    def get_children_dinner_shows(self) -> Generator[DinnerShowFacilityChild, None, None]:  # type: ignore
        """Get DinnerShowFacilityChild Children of a Facility

        Yields:
            Generator[DinnerShowFacilityChild, None, None]: A generator of DinnerShowFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.DINNER_SHOW.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield DinnerShowFacilityChild(i["id"])

    def get_children_entertainment(self) -> Generator[EntertainmentFacilityChild, None, None]:  # type: ignore
        """Get EntertainmentFacilityChild Children of a Facility

        Yields:
            Generator[EntertainmentFacilityChild, None, None]: A generator of EntertainmentFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.ENTERTAINMENT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield EntertainmentFacilityChild(i["id"])

    def get_children_events(self) -> Generator[WaterParkFacilityChild, None, None]:  # type: ignore
        """Get WaterParkFacilityChild Children of a Facility

        Yields:
            Generator[WaterParkFacilityChild, None, None]: A generator of WaterParkFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.EVENT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield WaterParkFacilityChild(i["id"])

    def get_children_entertainment_venues(self) -> Generator[EntertainmentVenueFacilityChild, None, None]:  # type: ignore
        """Get EntertainmentVenueFacilityChild Children of a Facility

        Yields:
            Generator[EntertainmentVenueFacilityChild, None, None]: A generator of EntertainmentVenueFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.ENTERTAINMENT_VENUE.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield EntertainmentVenueFacilityChild(i["id"])

    def get_children_guest_services(self) -> Generator[GuestServiceFacilityChild, None, None]:  # type: ignore
        """Get GuestServiceFacilityChild Children of a Facility

        Yields:
            Generator[GuestServiceFacilityChild, None, None]: A generator of GuestServiceFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.GUEST_SERVICE.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield GuestServiceFacilityChild(i["id"])

    def get_children_lands(self) -> Generator[LandFacilityChild, None, None]:  # type: ignore
        """Get LandFacilityChild Children of a Facility

        Yields:
            Generator[LandFacilityChild, None, None]: A generator of LandFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.LAND.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield LandFacilityChild(i["id"])

    def get_children_merchandise_facilities(self) -> Generator[MerchandiseFacilityChild, None, None]:  # type: ignore
        """Get MerchandiseFacilityChild Children of a Facility

        Yields:
            Generator[MerchandiseFacilityChild, None, None]: A generator of MerchandiseFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.MERCHANDISE_FACILITY.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield MerchandiseFacilityChild(i["id"])

    def get_children_photopasses(self) -> Generator[PhotopassFacilityChild, None, None]:  # type: ignore
        """Get PhotopassFacilityChild Children of a Facility

        Yields:
            Generator[PhotopassFacilityChild, None, None]: A generator of PhotopassFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.PHOTOPASS.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield PhotopassFacilityChild(i["id"])

    def get_children_point_of_interests(self) -> Generator[PointOfInterestFacilityChild, None, None]:  # type: ignore
        """Get PointOfInterestFacilityChild Children of a Facility

        Yields:
            Generator[PointOfInterestFacilityChild, None, None]: A generator of PointOfInterestFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.POINT_OF_INTEREST.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield PointOfInterestFacilityChild(i["id"])

    def get_children_recreation(self) -> Generator[RecreationFacilityChild, None, None]:  # type: ignore
        """Get RecreationFacilityChild Children of a Facility

        Yields:
            Generator[RecreationFacilityChild, None, None]: A generator of RecreationFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.RECREATION.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield RecreationFacilityChild(i["id"])

    def get_children_recreation_activities(self) -> Generator[RecreationActivityFacilityChild, None, None]:  # type: ignore
        """Get RecreationActivityFacilityChild Children of a Facility

        Yields:
            Generator[RecreationActivityFacilityChild, None, None]: A generator of RecreationActivityFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.RECREATION_ACTIVITY.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield RecreationActivityFacilityChild(i["id"])

    def get_children_resorts(self) -> Generator[ResortFacilityChild, None, None]:  # type: ignore
        """Get ResortFacilityChild Children of a Facility

        Yields:
            Generator[ResortFacilityChild, None, None]: A generator of ResortFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.RESORT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield ResortFacilityChild(i["id"])

    def get_children_resort_areas(self) -> Generator[ResortAreaFacilityChild, None, None]:  # type: ignore
        """Get ResortAreaFacilityChild Children of a Facility

        Yields:
            Generator[ResortAreaFacilityChild, None, None]: A generator of ResortAreaFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.RESORT_AREA.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield ResortAreaFacilityChild(i["id"])

    def get_children_restaurants(self) -> Generator[RestaurantFacilityChild, None, None]:  # type: ignore
        """Get RestaurantFacilityChild Children of a Facility

        Yields:
            Generator[RestaurantFacilityChild, None, None]: A generator of RestaurantFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.RESTAURANT.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield RestaurantFacilityChild(i["id"])

    def get_children_spas(self) -> Generator[SpaFacilityChild, None, None]:  # type: ignore
        """Get SpaFacilityChild Children of a Facility

        Yields:
            Generator[SpaFacilityChild, None, None]: A generator of SpaFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.SPA.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield SpaFacilityChild(i["id"])

    def get_children_theme_parks(self) -> Generator[ThemeParkFacilityChild, None, None]:  # type: ignore
        """Get ThemeParkFacilityChild Children of a Facility

        Yields:
            Generator[ThemeParkFacilityChild, None, None]: A generator of ThemeParkFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.THEME_PARK.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield ThemeParkFacilityChild(i["id"])

    def get_children_tours(self) -> Generator[TourFacilityChild, None, None]:  # type: ignore
        """Get TourFacilityChild Children of a Facility

        Yields:
            Generator[TourFacilityChild, None, None]: A generator of TourFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.TOUR.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield TourFacilityChild(i["id"])

    def get_children_transportation(self) -> Generator[TransportationFacilityChild, None, None]:  # type: ignore
        """Get TransportationFacilityChild Children of a Facility

        Yields:
            Generator[TransportationFacilityChild, None, None]: A generator of TransportationFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.TRANSPORTATION.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield TransportationFacilityChild(i["id"])

    def get_children_water_parks(self) -> Generator[WaterParkFacilityChild, None, None]:  # type: ignore
        """Get WaterParkFacilityChild Children of a Facility

        Yields:
            Generator[WaterParkFacilityChild, None, None]: A generator of WaterParkFacilityChild Children
        """
        self.refresh()

        check_for = f"entitytype={EntityType.WATER_PARK.value}".lower()
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield WaterParkFacilityChild(i["id"])
