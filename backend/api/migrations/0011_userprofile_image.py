# Generated by Django 5.0.6 on 2024-05-17 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_tanmirtpost_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(null=True, upload_to='profile_images'),
        ),
    ]