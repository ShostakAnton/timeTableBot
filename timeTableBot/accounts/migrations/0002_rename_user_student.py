# Generated by Django 3.2.7 on 2021-10-19 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_timetable_abbreviation'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Student',
        ),
    ]
