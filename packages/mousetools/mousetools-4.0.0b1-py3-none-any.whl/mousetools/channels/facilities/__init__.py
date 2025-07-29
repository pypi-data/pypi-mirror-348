import logging
import typing
from collections.abc import Generator
from datetime import datetime, time, timedelta
from enum import Enum
from zoneinfo import ZoneInfo

from mousetools.api.menu import Menus
from mousetools.channels import CouchbaseChannel
from mousetools.channels.enums import DestinationShort, DestinationTimezones, DLRCouchbaseChannels, WDWCouchbaseChannels
from mousetools.channels.facilitystatus import FacilityStatusChildChannel
from mousetools.mixins.couchbase import CouchbaseMixin

logger = logging.getLogger(__name__)


class FacilityChildChannel(CouchbaseMixin):
    """Base class for all Facility Child Channels. Subclasses like Attraction, Restaurant, Entertainment, etc. extend this class.

    Example:

        >>> from mousetools.channels.facilities import Attraction, ThemePark
        >>> a = Attraction("wdw.facilities.1_0.en_us.attraction.80010177;entityType=Attraction")
        >>> print(a)
        "Attraction: Pirates of the Caribbean (wdw.facilities.1_0.en_us.attraction.80010177;entityType=Attraction)"
        >>> from mousetools.channels.facilities.enums import WaltDisneyWorldParkChannelIds
        >>> d = ThemePark(WaltDisneyWorldParkChannelIds.MAGIC_KINGDOM, lazy_load=False)
        >>> print(d.coordinates)
        {'latitude': 28.4160036778, 'longitude': -81.5811902834}
    """

    _channel_complete_name: str
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
        self._refresh_interval: timedelta = timedelta(minutes=10)

        self._cb_data: typing.Optional[dict] = None
        if not lazy_load:
            self.refresh()

    def refresh(self) -> None:
        """Pulls initial data if none exists or if it is older than the refresh interval"""
        if self._cb_data is None or datetime.now(tz=self._tz.value) - self.last_update > self._refresh_interval:
            self._cb_data = self.get_channel_data(self.channel_id)

    @property
    def name(self) -> typing.Optional[str]:
        """
        The name of the entity.

        Returns:
            (typing.Optional[str]): The name of the entity, or None if it was not found.
        """

        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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

        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        # TODO check other ancestors to guess dest if not found
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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

        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
        try:
            return self._cb_data["ancestorRestaurantId"]
        except KeyError:
            logger.debug("No ancestor restaurant ids found for %s", self.channel_id)
            return None

    @property
    def disney_owned(self) -> typing.Optional[bool]:
        """
        Whether the entity is owned by Disney.

        Returns:
            (typing.Optional[bool]): Whether the entity is owned by Disney.
        """
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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
            dt = datetime.fromisoformat(self._cb_data["lastUpdate"])
            dt = dt.replace(tzinfo=tz.value)
            return dt
        except KeyError:
            logger.debug("No last updated found for %s", self.channel_id)
            return None

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


Attraction = FacilityChildChannel.get_subclass("Attraction")
Character = FacilityChildChannel.get_subclass("Character")
Destination = FacilityChildChannel.get_subclass("Destination")
DiningEvent = FacilityChildChannel.get_subclass("DiningEvent")
DinnerShow = FacilityChildChannel.get_subclass("DinnerShow")
EntertainmentVenue = FacilityChildChannel.get_subclass("EntertainmentVenue")
Entertainment = FacilityChildChannel.get_subclass("Entertainment")
Event = FacilityChildChannel.get_subclass("Event")
GuestServices = FacilityChildChannel.get_subclass("GuestServices")
Land = FacilityChildChannel.get_subclass("Land")
MerchandiseFacility = FacilityChildChannel.get_subclass("MerchandiseFacility")
ThemePark = FacilityChildChannel.get_subclass("ThemePark")
WaterPark = FacilityChildChannel.get_subclass("WaterPark")
PointOfInterest = FacilityChildChannel.get_subclass("PointOfInterest")
ResortArea = FacilityChildChannel.get_subclass("ResortArea")
Resort = FacilityChildChannel.get_subclass("Resort")


class Restaurant(FacilityChildChannel):
    """Class for Restaurant Entities."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def meal_periods(self) -> typing.Optional[list[str]]:
        """
        The meal periods offered by the restaurant.

        Returns:
            (typing.Optional[list[str]]): The meal periods offered by the restaurant.
        """
        if self._cb_data is None:
            self._cb_data = self.get_channel_data(self.channel_id)
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


class FacilityChannel(CouchbaseChannel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_children_attractions(self) -> Generator[Attraction, None, None]:  # type: ignore
        """Get Attraction Children of a Facility

        Yields:
            Generator[Attraction, None, None]: A generator of Attraction Children
        """
        self.refresh()

        check_for = "entitytype=attraction"
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield Attraction(i["id"])

    def get_children_restaurants(self) -> Generator[Restaurant, None, None]:
        """Get Restaurant Children of a Facility

        Yields:
            Generator[Restaurant, None, None]: A generator of Restaurant Children
        """
        self.refresh()

        check_for = "entitytype=restaurant"
        for i in self._cb_data["results"]:
            if check_for == i["id"].rsplit(";")[-1].lower():
                yield Restaurant(i["id"])
