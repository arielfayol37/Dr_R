# Generated by Django 4.2.3 on 2023-08-27 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0023_mcqimageanswer_label_questionimage_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionimage',
            old_name='name',
            new_name='label',
        ),
    ]
