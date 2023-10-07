# Generated by Django 4.2.4 on 2023-10-06 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deimos', '0009_assignmentstudent_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionModifiedScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_modified', models.BooleanField(default=False)),
                ('score', models.FloatField(blank=True, default=0, null=True)),
                ('question_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modify_question_score', to='deimos.questionstudent')),
            ],
        ),
    ]
