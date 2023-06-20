# Generated by Django 4.1.7 on 2023-05-17 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='tas',
        ),
        migrations.AddField(
            model_name='section',
            name='ta',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 3}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]