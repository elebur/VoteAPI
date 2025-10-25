from django.db import transaction
from rest_framework import serializers

from base import models


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        # fields = "__all__"
        exclude = ("menu", "restaurant")


class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)

    class Meta:
        model = models.Menu
        fields = "__all__"

    def create(self, validated_data: dict):
        menu_items_data = validated_data.pop("items")
        with transaction.atomic():
            menu = models.Menu.objects.create(**validated_data)
            for item in menu_items_data:
                # Check if a menu item exists for the given restaurant.
                menu_item = models.MenuItem.objects.filter(title=item["title"],
                                                           restaurant=validated_data["restaurant"]
                                                           ).first()
                if menu_item:
                    # If received description differs from the existing one,
                    # then updating the description of the menu item in the DB.
                    if menu_item.description != item["description"]:
                        menu_item.description = item["description"]
                        menu_item.save()
                    menu.items.add(menu_item)
                else:
                    menu.items.create(restaurant=validated_data["restaurant"],
                                      title=item["title"],
                                      description=item["description"])
        return menu
