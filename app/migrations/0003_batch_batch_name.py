# Generated by Django 4.1.7 on 2023-03-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_client_joined_alter_client_user_id_batch"),
    ]

    operations = [
        migrations.AddField(
            model_name="batch",
            name="batch_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="batch_name"
            ),
        ),
    ]
