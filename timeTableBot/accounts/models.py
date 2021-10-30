from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    group = models.ForeignKey(
        "core.Student_group", on_delete=models.SET_NULL, null=True, blank=True, related_name="user"
    )