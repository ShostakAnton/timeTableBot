from django.contrib import admin
from core import models


admin.site.register(models.Faculty)


@admin.register(models.Student_group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "faculty",
        "course",
        "direction",
    )
    list_filter = ("course", "faculty", "direction", )


@admin.register(models.TimeTable)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "abbreviation",
        "full_title",
        "begin",
        "end",
    )

    list_filter = ("group__faculty", )