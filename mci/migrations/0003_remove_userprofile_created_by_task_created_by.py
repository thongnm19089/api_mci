# Generated by Django 4.2.11 on 2024-04-12 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mci', '0002_alter_userprofile_options_alter_userprofile_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='created_by',
        ),
        migrations.AddField(
            model_name='task',
            name='created_by',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
