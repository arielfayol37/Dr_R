# Generated by Django 4.2.3 on 2023-07-28 00:41

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0008_assignment_assigned_date_assignment_difficulty_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('topic', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='sub_topics', to='phobos.topic')),
            ],
        ),
    ]
