from django.urls import path
from api.views.employee import get_employee

urlpatterns = [
    path("employee/<int:pk>/", get_employee, name="get_employee")
]
