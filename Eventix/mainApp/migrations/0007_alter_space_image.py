# Generated by Django 4.2.6 on 2023-11-13 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_alter_eventlikes_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]