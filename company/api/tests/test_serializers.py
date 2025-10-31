from types import MappingProxyType

from api.serializers import MenuSerializer
from base.models import Menu, MenuItem, Restaurant


class TestMenuSerializerWithDuplicatedItems:
    menu_raw_data = MappingProxyType(
        {
            "restaurant": -1,
            "title": "Menu",
            "notes": "Notes",
            "launch_date": "2025-10-10",
            "items": [],
        }
    )
    items_raw_data = (
        {
            "title": "Bruschetta al Pomodoro",
            "description": "Toasted bread topped with fresh tomatoes, basil, and olive oil.",
        },
        {
            "title": "Risotto ai Funghi Porcini",
            "description": "Creamy risotto with porcini mushrooms and Parmesan cheese.",
        },
        {
            "title": "Spaghetti Carbonara",
            "description": "Classic pasta with egg, pancetta, and Pecorino Romano cheese.",
        },
        {
            "title": "Lasagna alla Bolognese",
            "description": "Layered pasta with Bolognese meat sauce and béchamel cream.",
        },
        {
            "title": "Tiramisu",
            "description": "Traditional Italian dessert made with mascarpone, coffee, and cocoa.",
        },
    )

    def test_no_duplicates_in_db(self, restaurant: Restaurant):
        """
        Check that when same menu items are sent they are not duplicated in the DB.
        """
        data = self.menu_raw_data.copy()
        items = self.items_raw_data[:2]
        data["restaurant"] = restaurant.id
        data["items"] = list(items)

        # Ensure that the DB is empty.
        assert MenuItem.objects.count() == 0
        assert Menu.objects.count() == 0

        ser = MenuSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.create(ser.validated_data)

        # Added two menu items and one menu.
        assert MenuItem.objects.count() == 2
        assert Menu.objects.count() == 1

        # Creating a new menu with the same data except the 'launch_date'
        data["launch_date"] = "2026-1-1"
        data["items"] = list(items)
        ser_duplicate = MenuSerializer(data=data)
        ser_duplicate.is_valid(raise_exception=True)
        ser_duplicate.create(ser_duplicate.validated_data)

        # After the second call with the same items we must
        # get +1 menu and no new menu items.
        assert MenuItem.objects.count() == 2
        assert Menu.objects.count() == 2

    def test_same_item_name_with_different_description(self, restaurant):
        data = self.menu_raw_data.copy()
        items_raw = list(self.items_raw_data[:2])
        items_raw[0]["description"] = "Init description #1"
        items_raw[1]["description"] = "Init description #2"

        data["restaurant"] = restaurant.id
        data["items"] = items_raw

        ser = MenuSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.create(ser.validated_data)

        # Ensure that there are exactly two menu items
        # and they have predefined description.
        assert MenuItem.objects.count() == 2
        item_init_1, item_init_2 = MenuItem.objects.all()
        assert item_init_1.description == "Init description #1"
        assert item_init_2.description == "Init description #2"

        # Updating the descriptions.
        items_raw[0]["description"] = "New description #1"
        items_raw[1]["description"] = "New description #2"
        data["items"] = items_raw

        ser_updated = MenuSerializer(data=data)
        ser_updated.is_valid(raise_exception=True)
        ser_updated.create(ser_updated.validated_data)

        # Ensure that we still have two items and
        # they both have updated descriptions.
        assert MenuItem.objects.count() == 2
        item1, item2 = MenuItem.objects.all()
        assert item1.description == "New description #1"
        assert item2.description == "New description #2"
