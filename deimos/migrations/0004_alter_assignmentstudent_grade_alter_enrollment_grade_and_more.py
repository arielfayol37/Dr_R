# Generated by Django 4.2.3 on 2023-08-07 02:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deimos', '0003_rename_note_text_note_content_remove_student_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentstudent',
            name='grade',
            field=models.FloatField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='grade',
            field=models.FloatField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='questionattempt',
            name='is_successful',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='questionattempt',
            name='num_points',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='is_approved',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
