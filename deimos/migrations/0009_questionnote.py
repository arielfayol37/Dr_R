# Generated by Django 4.2.4 on 2023-09-01 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deimos', '0008_questionstudent_instances_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_note', to='deimos.questionstudent')),
            ],
        ),
    ]