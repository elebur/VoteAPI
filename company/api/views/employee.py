from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from base.models import Employee
from api.serializers import EmployeeSerializer


@api_view(["GET"])
def get_employee(request: Request, pk: int):
    e = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(e, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def add_employee(request: Request):
    serializer = EmployeeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"employee_id": serializer.data["id"]}
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
