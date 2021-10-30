from django.contrib import admin
from accounts import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "group",
    )
    list_filter = ("group__faculty",)