# Generated by Django 4.2.4 on 2023-08-20 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_jobresult_error"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobresult",
            name="result",
            field=models.TextField(blank=True, null=True),
        ),
    ]