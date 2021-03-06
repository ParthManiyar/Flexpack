# Generated by Django 3.1.5 on 2021-03-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth_login_register', '0022_auto_20210305_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_pic.png', null=True, upload_to='profile_pic'),
        ),
    ]
