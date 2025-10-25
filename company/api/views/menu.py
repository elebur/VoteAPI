import datetime

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from base.models import Menu
from api.serializers import MenuSerializer


@api_view(["GET"])
def get_menu_by_id(request: Request, pk: int):
    m = get_object_or_404(Menu, pk=pk)
    serializer = MenuSerializer(m, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_menus_by_date(request: Request, year: int, month: int, day: int):
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
def create_menu(request: Request):
    serializer = MenuSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"menu_id": serializer.data["id"]} # type: ignore
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
