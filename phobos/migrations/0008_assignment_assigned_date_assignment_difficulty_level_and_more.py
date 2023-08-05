# Generated by Django 4.2.3 on 2023-07-23 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0007_alter_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='assigned_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='difficulty_level',
            field=models.CharField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('DIFFICULT', 'Difficult')], default='MEDIUM', max_length=10),
        ),
        migrations.AddField(
            model_name='question',
            name='difficulty_level',
            field=models.CharField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('DIFFICULT', 'Difficult')], default='MEDIUM', max_length=10),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(max_length=2000),
        ),
    ]
