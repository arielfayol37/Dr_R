# Generated by Django 4.2.2 on 2023-07-19 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0004_course_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='question',
            old_name='unit',
            new_name='sub_topic',
        ),
        migrations.RemoveField(
            model_name='question',
            name='sub_questions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='weight',
        ),
        migrations.AddField(
            model_name='question',
            name='num_points',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='question',
            name='parent_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_questions', to='phobos.question'),
        ),
        migrations.AddField(
            model_name='course',
            name='topics',
            field=models.ManyToManyField(related_name='courses', to='phobos.topic'),
        ),
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='phobos.topic'),
        ),
    ]
