# Generated by Django 5.0.2 on 2024-02-18 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project_manager", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name="userprofile",
            old_name="usuario",
            new_name="user",
        ),
        migrations.AddField(
            model_name="card",
            name="company",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="project_manager.company",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="company",
            field=models.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="project_manager.company",
            ),
            preserve_default=False,
        ),
    ]