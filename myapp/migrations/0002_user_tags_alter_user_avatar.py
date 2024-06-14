# Generated by Django 4.2.7 on 2024-05-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tags",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.CharField(default="media/default.png", max_length=100),
        ),
    ]