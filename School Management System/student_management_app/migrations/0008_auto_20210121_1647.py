# Generated by Django 3.1.5 on 2021-01-21 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0007_merge_20210121_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classes',
            old_name='course_name',
            new_name='class_name',
        ),
    ]
