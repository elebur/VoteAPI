import datetime

from django.http import HttpResponseBase, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import MenuSerializer
from base.models import Menu


@api_view(["GET"])
def get_menu_by_id(request: Request, pk: int) -> Response:  # noqa: ARG001
    """Return a menu by its id."""
    m = get_object_or_404(Menu, pk=pk)
    serializer = MenuSerializer(m, many=False)
    return Response(serializer.data)


@csrf_exempt
def process_menu(request: Request) -> Response | HttpResponseBase:
    """Based on the method the function delegates the request to the proper handler.

    GET: return menus results for today.
    POST: create new menu.
    """
    if request.method == "POST":
        return create_menu(request)
    if request.method == "GET":
        today = timezone.now()
        return get_menus_by_date(
            request, year=today.year, month=today.month, day=today.day,
        )

    msg = f"""{{"detail": "Method \\"{request.method}\\" not allowed."}}"""
    return HttpResponseNotAllowed(content=msg, permitted_methods=("GET", "POST"))


@api_view(["GET"])
def get_menus_by_date(request: Request, year: int, month: int, day: int) -> Response:  # noqa: ARG001
    """Return menus for the given date."""
    try:
        date = datetime.date(year=year, month=month, day=day)
    except ValueError:
        err_msg = (f"Invalid date - '{year}-{month}-{day}'. "
                   "Correct format is YYYY-MM-DD")
        return Response({"details": err_msg}, status=status.HTTP_400_BAD_REQUEST)
    menus = Menu.objects.filter(launch_date=date)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_menu(request: Request) -> Response:
    """Create new menu."""
    serializer = MenuSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"menu_id": serializer.data["id"]}  # pyright: ignore[reportArgumentType, reportCallIssue]
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
