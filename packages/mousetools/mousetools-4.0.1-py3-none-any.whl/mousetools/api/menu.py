import typing

from mousetools.auth import auth_obj
from mousetools.mixins.disney import DisneyAPIMixin

# menus -> menu -> menugroups -> menuitems


class MenuItem:
    def __init__(self, raw_item_data: dict, parent_resturant_id: typing.Optional[str] = None):
        self._raw_item_data = raw_item_data
        self._parent_restaurant_id = parent_resturant_id

    def __repr__(self) -> str:
        return f"MenuItem(entity_id={self.entity_id}, parent_resturant_id={self._parent_restaurant_id})"

    @property
    def entity_id(self) -> typing.Optional[str]:
        """
        The entity id of the menu item.

        Returns:
            (typing.Optional[str]): The entity id of the menu item.
        """
        try:
            return self._raw_item_data["id"]
        except KeyError:
            return None

    @property
    def pc_short_name(self) -> typing.Optional[str]:
        """
        The short name of the menu item.

        Returns:
            (typing.Optional[str]): The short name of the menu item.
        """
        try:
            return self._raw_item_data["names"]["PCShort"]
        except KeyError:
            return None

    @property
    def pc_long_name(self) -> typing.Optional[str]:
        """
        The long name of the menu item.

        Returns:
            (typing.Optional[str]): The long name of the menu item.
        """
        try:
            return self._raw_item_data["names"]["PCLong"]
        except KeyError:
            return None

    @property
    def mobile_short_name(self) -> typing.Optional[str]:
        """
        The short name of the menu item.

        Returns:
            (typing.Optional[str]): The short name of the menu item.
        """
        try:
            return self._raw_item_data["names"]["MobileShort"]
        except KeyError:
            return None

    @property
    def mobile_long_name(self) -> typing.Optional[str]:
        """
        The long name of the menu item.

        Returns:
            (typing.Optional[str]): The long name of the menu item.
        """
        try:
            return self._raw_item_data["names"]["MobileLong"]
        except KeyError:
            return None

    @property
    def mickey_check(self) -> typing.Optional[bool]:
        """
        Whether the menu item is mickey check.

        Returns:
            (typing.Optional[bool]): Whether the menu item is mickey check.
        """
        try:
            return self._raw_item_data["mickeyCheck"]
        except KeyError:
            return None

    @property
    def pc_long_description(self) -> typing.Optional[str]:
        """
        The long description of the menu item.

        Returns:
            (typing.Optional[str]): The long description of the menu item.
        """
        try:
            return self._raw_item_data["descriptions"]["PCLong"]["text"]
        except KeyError:
            return None

    @property
    def mobile_short_description(self) -> typing.Optional[str]:
        """
        The short description of the menu item.

        Returns:
            (typing.Optional[str]): The short description of the menu item.
        """
        try:
            return self._raw_item_data["descriptions"]["MobileShort"]["text"]
        except KeyError:
            return None

    @property
    def default_selection(self) -> typing.Optional[bool]:
        """
        Whether the menu item is the default selection.

        Returns:
            (typing.Optional[bool]): Whether the menu item is the default selection.
        """
        try:
            return self._raw_item_data["defaultSelection"]
        except KeyError:
            return None

    @property
    def prices(self) -> typing.Optional[dict]:
        """
        The prices of the menu item.

        Returns:
            (typing.Optional[dict]): The prices of the menu item.
        """
        try:
            return self._raw_item_data["prices"]
        except KeyError:
            return None

    @property
    def per_serving_without_tax(self) -> typing.Optional[float]:
        """
        The per serving without tax of the menu item.

        Returns:
            (typing.Optional[float]): The per serving without tax of the menu item.
        """
        try:
            return self._raw_item_data["prices"]["PerServing"]["withoutTax"]
        except KeyError:
            return None


class MenuGroup:
    def __init__(self, raw_menu_group_data: dict, parent_restaurant_id: typing.Optional[str] = None):
        self._raw_menu_group_data = raw_menu_group_data
        self._parent_restaurant_id = parent_restaurant_id

    def __str__(self) -> str:
        return f"MenuGroup(menu_group_type={self.menu_group_type}, parent_restaurant_id={self._parent_restaurant_id})"

    @property
    def menu_group_type(self) -> typing.Optional[str]:
        """
        The type of the menu group.

        Returns:
            (typing.Optional[str]): The type of the menu group.
        """
        try:
            return self._raw_menu_group_data["menuGroupType"]
        except KeyError:
            return None

    @property
    def multiple_price_types(self) -> typing.Optional[bool]:
        """
        Whether the menu group has multiple price types.

        Returns:
            (typing.Optional[bool]): Whether the menu group has multiple price types.
        """
        try:
            return self._raw_menu_group_data["multiplePriceTypes"]
        except KeyError:
            return None

    @property
    def mickey_check_items(self) -> typing.Optional[bool]:
        """
        Whether the menu group has mickey check items.

        Returns:
            (typing.Optional[bool]): Whether the menu group has mickey check items.
        """
        try:
            return self._raw_menu_group_data["mickeyCheckItems"]
        except KeyError:
            return None

    @property
    def names(self) -> typing.Optional[dict]:
        """
        The names of the menu group.

        Returns:
            (typing.Optional[dict]): The names of the menu group.
        """
        try:
            return self._raw_menu_group_data["names"]
        except KeyError:
            return None

    @property
    def pc_short_name(self) -> typing.Optional[str]:
        """
        The short name of the menu group.

        Returns:
            (typing.Optional[str]): The short name of the menu group.
        """
        try:
            return self._raw_menu_group_data["names"]["PCShort"]
        except KeyError:
            return None

    @property
    def pc_long_name(self) -> typing.Optional[str]:
        """
        The long name of the menu group.

        Returns:
            (typing.Optional[str]): The long name of the menu group.
        """
        try:
            return self._raw_menu_group_data["names"]["PCLong"]
        except KeyError:
            return None

    @property
    def mobile_short_name(self) -> typing.Optional[str]:
        """
        The short name of the menu group.

        Returns:
            (typing.Optional[str]): The short name of the menu group.
        """
        try:
            return self._raw_menu_group_data["names"]["MobileShort"]
        except KeyError:
            return None

    @property
    def mobile_long_name(self) -> typing.Optional[str]:
        """
        The long name of the menu group.

        Returns:
            (typing.Optional[str]): The long name of the menu group.
        """
        try:
            return self._raw_menu_group_data["names"]["MobileLong"]
        except KeyError:
            return None

    @property
    def menu_items(self) -> typing.Optional[list[MenuItem]]:
        """
        The menu items of the menu group.

        Returns:
            (typing.Optional[list[MenuItem]]): The menu items of the menu group.
        """
        try:
            return [MenuItem(i, self._parent_restaurant_id) for i in self._raw_menu_group_data["menuItems"]]
        except KeyError:
            return None


class Menu:
    def __init__(self, raw_menu_data: dict, parent_restaurant_id: typing.Optional[str] = None):
        self._raw_menu_data = raw_menu_data
        self._parent_restaurant_id = parent_restaurant_id

    def __str__(self):
        return f"Menu(entity_id={self.entity_id}, menu_type={self.menu_type}, parent_restaurant_id={self._parent_restaurant_id})"

    @property
    def entity_id(self) -> typing.Optional[str]:
        """
        The entity id of the menu.

        Returns:
            (typing.Optional[str]): The entity id of the menu.
        """
        try:
            return self._raw_menu_data["id"]
        except KeyError:
            return None

    @property
    def menu_type(self) -> typing.Optional[str]:
        """
        The type of the menu.

        Returns:
            (typing.Optional[str]): The type of the menu.
        """
        try:
            return self._raw_menu_data["menuType"]
        except KeyError:
            return None

    @property
    def localized_menu_type(self) -> typing.Optional[str]:
        """
        The localized type of the menu.

        Returns:
            (typing.Optional[str]): The localized type of the menu.
        """
        try:
            return self._raw_menu_data["localizedMenuType"]
        except KeyError:
            return None

    @property
    def experience_type(self) -> typing.Optional[str]:
        """
        The experience type of the menu.

        Returns:
            (typing.Optional[str]): The experience type of the menu.
        """
        try:
            return self._raw_menu_data["experienceType"]
        except KeyError:
            return None

    @property
    def service_style(self) -> typing.Optional[str]:
        """
        The service style of the menu.

        Returns:
            (typing.Optional[str]): The service style of the menu.
        """
        try:
            return self._raw_menu_data["serviceStyle"]
        except KeyError:
            return None

    @property
    def primary_cuisine_type(self) -> typing.Optional[str]:
        """
        The primary cuisine type of the menu.

        Returns:
            (typing.Optional[str]): The primary cuisine type of the menu.
        """
        try:
            return self._raw_menu_data["primaryCuisineType"]
        except KeyError:
            return None

    @property
    def secondary_cuisine_type(self) -> typing.Optional[str]:
        """
        The secondary cuisine type of the menu.

        Returns:
            (typing.Optional[str]): The secondary cuisine type of the menu.
        """
        try:
            return self._raw_menu_data["secondaryCuisineType"]
        except KeyError:
            return None

    @property
    def menu_groups(self) -> list[MenuGroup]:
        """
        The menu groups of the menu.

        Returns:
            (list[MenuGroup]): The menu items of the menu.
        """
        try:
            return [MenuGroup(i, self._parent_restaurant_id) for i in self._raw_menu_data["menuGroups"]]
        except KeyError:
            return []


class Menus(DisneyAPIMixin):
    """Class for Menu Entities."""

    _menu_service_base = f"{auth_obj._environments['serviceMenuUrl']}/diningMenuSvc/orchestration/menus"

    def __init__(self, restaurant_channel_id: str, lazy_load: bool = True):
        self.entity_id = restaurant_channel_id.rsplit(".", 1)[-1]
        self._menu_service_url = f"{self._menu_service_base}/{self.entity_id}"

        if lazy_load:
            self.disney_data: typing.Optional[dict] = None
        else:
            self.disney_data = self.get_disney_data(self.entity_id)

    def __str__(self):
        return f"Menus(entity_id={self.entity_id})"

    def __repr__(self):
        return f"Menus(restaurant_channel_id={self.entity_id})"

    @property
    def menus(self) -> list[Menu]:
        """
        Returns a list of all the menus associated with this entity.

        Returns:
            (list[Menu]): List of Menu objects that are associated with this entity.
        """
        if self.disney_data is None:
            self.disney_data = self.get_disney_data(self._menu_service_url)
        try:
            return [Menu(i, self.entity_id) for i in self.disney_data["menus"]]
        except KeyError:
            return []
