# Generated by Django 4.0.6 on 2022-07-28 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('post', 'Post'), ('news', 'News')], max_length=255),
        ),
    ]
