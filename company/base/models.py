from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models

if TYPE_CHECKING:
    from django_stubs_ext.db.models.manager import ManyRelatedManager, RelatedManager


class BaseReprAndStr:
    @property
    def __name(self):
        """
        Some classes have 'name' attribute while other have 'title'.
        This property checks for both and returns the existing one.
        """
        if hasattr(self, "title"):
            name_attr = "title"
        else:
            name_attr = "name"

        return getattr(self, name_attr)

    def __repr__(self):
        """
        Build string like '<ClassName: ObjName (pk=1)'
        """
        return f"<{type(self).__name__}: {self.__name} (pk={self.id})>"  # type: ignore

    def __str__(self):
        return self.__name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField()
    last_name = models.CharField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Employee: first_name='{self.first_name}', last_name='{self.last_name}, pk={self.pk}>"


class Restaurant(BaseReprAndStr, models.Model):
    name = models.CharField()
    date_joined = models.DateTimeField(auto_now_add=True)


class Menu(BaseReprAndStr, models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name="menus")
    title = models.CharField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # Date when the menu must be shown.
    launch_date = models.DateField()

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        items: ManyRelatedManager["MenuItem"]
        votes: RelatedManager["Vote"]
        id: int


class MenuItem(BaseReprAndStr, models.Model):
    menu = models.ManyToManyField(Menu, related_name="items")

    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name="menu_items")
    title = models.CharField()
    description = models.TextField()


class Vote(models.Model):
    menu = models.ForeignKey(Menu,
                             related_name="votes",
                             on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,
                                 related_name="votes",
                                 on_delete=models.CASCADE)
    like = models.BooleanField()
    voted_at = models.DateTimeField(auto_now_add=True)

    if TYPE_CHECKING:
        id: int

    def __repr__(self):
        return f"<Vote: Employee={self.employee.id}, like={self.like}, Menu={self.menu.id}>"  # type: ignore

    def __str__(self):
        action = "likes" if self.like else "dislikes"
        return f"{self.employee} {action} '{self.menu}'"
