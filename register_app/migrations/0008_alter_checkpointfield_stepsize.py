# Generated by Django 5.1.5 on 2025-02-06 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register_app", "0007_alter_checkpointfield_checkpoint"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkpointfield",
            name="stepsize",
            field=models.CharField(
                blank=True,
                choices=[
                    ("0.01", "0.01"),
                    ("0.05", "0.05"),
                    ("0.1", "0.1"),
                    ("0.5", "0.5"),
                    ("1", "1"),
                    ("5", "5"),
                    ("10", "10"),
                ],
                max_length=4,
                null=True,
                verbose_name="Mark step size",
            ),
        ),
    ]
