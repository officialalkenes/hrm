# Generated by Django 4.1.5 on 2023-11-04 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_alter_room_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='types',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]