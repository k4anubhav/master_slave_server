# Generated by Django 4.2.4 on 2023-08-19 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_rename_job_id_joblock_job_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobresult",
            name="error",
            field=models.TextField(blank=True, null=True),
        ),
    ]