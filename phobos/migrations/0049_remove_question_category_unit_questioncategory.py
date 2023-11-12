# Generated by Django 4.2.3 on 2023-11-10 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0048_remove_question_num_points_alter_courseinfo_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('subtopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='phobos.subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='phobos.question')),
                ('subtopic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='phobos.subtopic')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='phobos.topic')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='phobos.unit')),
            ],
        ),
    ]
