from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from base import models


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = models.Employee
        fields = ("id", "username", "password",
                  "email", "first_name",
                  "last_name", "user", "date_joined")

    def create(self, validated_data: dict):
        u = User.objects.filter(username=validated_data["username"]).first()

        if u:
            err_msg = f"The username '{validated_data['username']}' is already in use"
            raise ValidationError(detail=err_msg, code=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=validated_data["username"],
                                        password=validated_data["password"],
                                        email=validated_data["email"])
        return models.Employee.objects.create(user=user,
                                              first_name=validated_data["first_name"],
                                              last_name=validated_data["last_name"])


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
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


class DoVoteSerializer(serializers.Serializer):
    like = serializers.BooleanField()
    employee_id = serializers.IntegerField()
