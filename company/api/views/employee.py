from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from base.models import Employee
from api.serializers import EmployeeSerializer


@api_view(["GET"])
def get_employee(request: Request, pk: int):
    e = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(e, many=False)
    return Response(serializer.data)