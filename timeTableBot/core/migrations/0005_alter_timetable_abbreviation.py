# Generated by Django 3.2.7 on 2021-10-19 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20211019_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='abbreviation',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
