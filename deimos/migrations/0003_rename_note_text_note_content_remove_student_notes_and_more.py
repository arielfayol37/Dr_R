# Generated by Django 4.2.3 on 2023-08-07 01:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0014_alter_mcqexpressionanswer_content_and_more'),
        ('deimos', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='note_text',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='student',
            name='notes',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bonuspoint',
            name='resource',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bonuses', to='deimos.resource'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='grade',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='deimos.student'),
        ),
        migrations.AlterField(
            model_name='note',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='deimos.student'),
        ),
        migrations.AlterField(
            model_name='noteimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='deimos/images/notes_images/'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='deimos.student'),
        ),
        migrations.CreateModel(
            name='QuestionStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_points', models.FloatField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phobos.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deimos.student')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('is_successful', models.BooleanField(default=False)),
                ('num_points', models.FloatField(default=0)),
                ('question_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='deimos.questionstudent')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phobos.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments_intermediate', to='deimos.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='assignments',
            field=models.ManyToManyField(through='deimos.AssignmentStudent', to='phobos.assignment'),
        ),
        migrations.AddField(
            model_name='student',
            name='questions',
            field=models.ManyToManyField(through='deimos.QuestionStudent', to='phobos.question'),
        ),
    ]
