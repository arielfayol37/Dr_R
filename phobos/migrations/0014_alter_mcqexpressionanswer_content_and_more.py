# Generated by Django 4.2.3 on 2023-08-07 01:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0013_alter_question_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcqexpressionanswer',
            name='content',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='num_points',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)]),
        ),
    ]