from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import RestaurantSerializer
from base.models import Restaurant


@api_view(["GET"])
def get_restaurant(request: Request, pk: int) -> Response:  # noqa: ARG001
    """Return a Restaurant for the given pk."""
    r = get_object_or_404(Restaurant, pk=pk)
    serializer = RestaurantSerializer(r, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def create_restaurant(request: Request) -> Response:
    """Add new Restaurant to the DB."""
    serializer = RestaurantSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"restaurant_id": serializer.data["id"]} # pyright: ignore[reportArgumentType, reportCallIssue]
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
