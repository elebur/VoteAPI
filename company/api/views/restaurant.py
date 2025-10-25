from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from base.models import Restaurant
from api.serializers import RestaurantSerializer


@api_view(["GET"])
def get_restaurant(request: Request, pk: int):
    r = get_object_or_404(Restaurant, pk=pk)
    serializer = RestaurantSerializer(r, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def create_restaurant(request: Request):
    serializer = RestaurantSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"restaurant_id": serializer.data["id"]}
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
