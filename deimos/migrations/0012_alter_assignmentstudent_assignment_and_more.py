# Generated by Django 4.2.3 on 2023-10-08 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0037_expressionanswer_preface_floatanswer_preface_and_more'),
        ('deimos', '0011_merge_20231008_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentstudent',
            name='assignment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='phobos.assignment'),
        ),
        migrations.AlterField(
            model_name='assignmentstudent',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assignments_intermediate', to='deimos.student'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='phobos.course'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='deimos.student'),
        ),
        migrations.AlterField(
            model_name='questionmodifiedscore',
            name='question_student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='modify_question_score', to='deimos.questionstudent'),
        ),
        migrations.AlterField(
            model_name='questionstudent',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='phobos.question'),
        ),
        migrations.AlterField(
            model_name='questionstudent',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deimos.student'),
        ),
    ]
