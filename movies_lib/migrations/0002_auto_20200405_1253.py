# Generated by Django 2.2.5 on 2020-04-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_lib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieitem',
            name='author',
            field=models.TextField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='movieitem',
            name='year',
            field=models.TextField(default='null', max_length=4),
        ),
        migrations.AlterField(
            model_name='movieitem',
            name='title',
            field=models.TextField(max_length=50),
        ),
    ]
