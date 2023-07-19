# Generated by Django 4.2.2 on 2023-07-19 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='difficulty_level',
            field=models.CharField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('DIFFICULT', 'Difficult')], default='MEDIUM', max_length=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='number_of_students',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
