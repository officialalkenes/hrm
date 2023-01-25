# Generated by Django 4.1.3 on 2023-01-25 20:11

import apps.hotel.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('preferred_entry_time', models.TimeField()),
                ('default_exit_time', models.TimeField()),
                ('status', models.CharField(max_length=255)),
                ('has_checked_out', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='event: bridal shower', max_length=100, verbose_name='Event')),
                ('slug', models.SlugField(blank=True, max_length=300)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('capacity', models.PositiveIntegerField(verbose_name='Maximum People per room')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('capacity', models.PositiveIntegerField(verbose_name='Maximum People per room')),
                ('beds', models.PositiveIntegerField(verbose_name='Number of Beds')),
                ('image', models.ImageField(upload_to=apps.hotel.models.room_image_path)),
                ('description', models.TextField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('image_repr', models.ImageField(upload_to=apps.hotel.models.room_type_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='RoomServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hotel.booking')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hotel.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_image', to='hotel.room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hotel.roomtype'),
        ),
        migrations.CreateModel(
            name='EventBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('preferred_entry_time', models.TimeField()),
                ('default_exit_time', models.TimeField()),
                ('status', models.CharField(max_length=255)),
                ('has_checked_out', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hotel.event')),
            ],
        ),
        migrations.CreateModel(
            name='BookingRefund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('guest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room'),
        ),
    ]
