from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Student_group(models.Model):
    name = models.CharField(max_length=30)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='groups')
    course = models.IntegerField()
    direction = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class TimeTable(models.Model):
    group = models.ForeignKey(Student_group, on_delete=models.CASCADE, null=True, related_name='time_table')
    full_title = models.CharField(max_length=100, blank=True)
    abbreviation = models.CharField(max_length=100, blank=True)
    begin = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.abbreviation