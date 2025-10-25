from django.urls import path
from api.views.employee import get_employee, add_employee

urlpatterns = [
    path("employee/<int:pk>/", get_employee, name="get_employee"),
    path("employee/", add_employee, name="add_employee"),
]
