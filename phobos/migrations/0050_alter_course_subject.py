# Generated by Django 4.2.3 on 2023-12-03 05:10


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0049_remove_question_category_unit_questioncategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.CharField(choices=[('PHYSICS', 'Physics')], default='PHYSICS', max_length=100),
        ),
    ]
