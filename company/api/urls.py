from django.urls import path
from api.views.employee import get_employee, add_employee
from api.views.restaurant import create_restaurant, get_restaurant

urlpatterns = [
    path("employee/<int:pk>/", get_employee, name="get_employee"),
    path("employee/", add_employee, name="add_employee"),
    path("restaurant/<int:pk>/", get_restaurant, name="get_restaurant"),
    path("restaurant/", create_restaurant, name="create_restaurant"),
]
