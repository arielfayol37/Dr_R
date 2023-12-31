# Generated by Django 4.2.1 on 2023-07-14 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('deimos', '0001_initial'),
        ('phobos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(through='deimos.Enrollment', to='phobos.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='notes',
            field=models.ManyToManyField(through='deimos.Note', to='phobos.question'),
        ),
        migrations.AddField(
            model_name='resource',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phobos.question'),
        ),
        migrations.AddField(
            model_name='resource',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deimos.student'),
        ),
        migrations.AddField(
            model_name='noteimage',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='deimos.note'),
        ),
        migrations.AddField(
            model_name='note',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phobos.question'),
        ),
        migrations.AddField(
            model_name='note',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deimos.student'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phobos.course'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deimos.student'),
        ),
        migrations.AddField(
            model_name='bonuspoint',
            name='resource',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deimos.resource'),
        ),
        migrations.AddField(
            model_name='bonuspoint',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deimos.student'),
        ),
    ]
