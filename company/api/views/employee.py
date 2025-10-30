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

from api.serializers import EmployeeSerializer
from base.models import Employee


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def get_employee(request: Request, pk: int) -> Response:  # noqa: ARG001
    """Return Employee by its 'pk'."""
    e = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(e, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def add_employee(request: Request) -> Response:
    """Add new Employee to the DB."""
    serializer = EmployeeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"employee_id": serializer.data["id"]} # pyright: ignore[reportArgumentType, reportCallIssue]
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)
