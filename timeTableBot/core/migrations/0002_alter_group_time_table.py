# Generated by Django 3.2.7 on 2021-10-03 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='time_table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='core.timetable'),
        ),
    ]
