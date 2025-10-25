from django.db import models


class Employee(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    date_joined = models.DateTimeField(auto_now_add=True)


class Restaurant(models.Model):
    name = models.CharField()
    date_joined = models.DateTimeField(auto_now_add=True)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name="menus")
    title = models.CharField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    date_created = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class MenuItem(models.Model):
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
