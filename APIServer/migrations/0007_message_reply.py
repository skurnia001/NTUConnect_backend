# Generated by Django 3.1.1 on 2020-10-15 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APIServer', '0006_votemessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='APIServer.message'),
        ),
    ]
