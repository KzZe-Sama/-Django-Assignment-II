# Generated by Django 3.0.7 on 2020-07-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification_code',
            name='user',
            field=models.EmailField(default='Example@gmail.com', max_length=254),
        ),
    ]
