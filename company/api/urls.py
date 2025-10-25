from django.urls import path
from api.views.employee import get_employee, add_employee
from api.views.restaurant import create_restaurant, get_restaurant
from api.views.menu import get_menu, create_menu

urlpatterns = [
    path("employee/<int:pk>/", get_employee, name="get_employee"),
    path("employee/", add_employee, name="add_employee"),
    path("restaurant/<int:pk>/", get_restaurant, name="get_restaurant"),
    path("restaurant/", create_restaurant, name="create_restaurant"),
    path("menu/<int:pk>/", get_menu, name="get_menu"),
    path("menu/", create_menu, name="create_menu"),
]
