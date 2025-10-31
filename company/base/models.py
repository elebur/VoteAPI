from typing import TYPE_CHECKING  # noqa: D100

from django.contrib.auth.models import User
from django.db import models

if TYPE_CHECKING:
    from django_stubs_ext.db.models.manager import ManyRelatedManager, RelatedManager


class BaseReprAndStr:
    """A basic class for providing 'str' and 'repr' dunder methods."""

    if TYPE_CHECKING:
        id: int

    @property
    def __name(self) -> str:
        """Dynamically generates 'name' attribute.

        Some classes have 'name' attribute while other have 'title'.
        This property checks for both and returns the existing one.
        """
        name_attr = "title" if hasattr(self, "title") else "name"

        return getattr(self, name_attr)

    def __repr__(self) -> str:
        """Build '__repr__' based on the '__name' attribute.

        Build string like '<ClassName: ObjName (pk=1)'
        """
        return f"<{type(self).__name__}: {self.__name} (pk={self.id})>"

    def __str__(self) -> str:
        """Return the '__name' attribute."""
        return self.__name


class Employee(models.Model):
    """The model represents an employee.

    It has O2O field to Django's User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField()
    last_name = models.CharField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:  # noqa: D105
        return (f"<Employee: first_name='{self.first_name}', "
                "last_name='{self.last_name}, pk={self.pk}>")


class Restaurant(BaseReprAndStr, models.Model):
    """Class represents a restaurant.

    Restaurants are required for creating menus.
    """

    name = models.CharField()
    date_joined = models.DateTimeField(auto_now_add=True)


class Menu(BaseReprAndStr, models.Model):
    """A menu entry.

    Each menu must have a Restaurant it belongs to
    and items that belonging to this menu.
    """

    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name="menus")
    title = models.CharField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    # Date when the menu must be shown.
    launch_date = models.DateField()

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        items: ManyRelatedManager["MenuItem"]
        votes: RelatedManager["Vote"]
        id: int


class MenuItem(BaseReprAndStr, models.Model):
    """An item for a menu.

    Besides the fact that the item must belong to a menu
    it also must belong to a certain restaurant. All items are unique
    in the certain Restaurant.
    The same item can be used in different menus and there would be
    no duplicated items in th DB.
    The uniqueness is determined by the item title.
    If a restaurant send an item that already exists in the DB, but has
    a different description, then the description will be updated.
    """

    menu = models.ManyToManyField(Menu, related_name="items")

    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name="menu_items")
    title = models.CharField()
    description = models.TextField()


class Vote(models.Model):
    """A vote (like/dislike) for menus."""

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

    def __repr__(self) -> str:  # noqa: D105
        return (f"<Vote: Employee={self.employee.id}, "
                "like={self.like}, Menu={self.menu.id}>")

    def __str__(self) -> str:  # noqa: D105
        action = "likes" if self.like else "dislikes"
        return f"{self.employee} {action} '{self.menu}'"
