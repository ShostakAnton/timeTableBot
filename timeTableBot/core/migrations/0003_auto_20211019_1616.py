# Generated by Django 3.2.7 on 2021-10-19 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_group_time_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='time_table',
        ),
        migrations.AddField(
            model_name='timetable',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='time_table', to='core.group'),
        ),
    ]
