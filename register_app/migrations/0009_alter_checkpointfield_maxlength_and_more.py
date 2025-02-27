# Generated by Django 5.1.5 on 2025-02-15 12:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register_app", "0008_alter_checkpointfield_stepsize"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkpointfield",
            name="maxlength",
            field=models.SmallIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(10),
                    django.core.validators.MaxValueValidator(1500),
                ],
                verbose_name="Max. character count",
            ),
        ),
        migrations.AlterField(
            model_name="checkpointfield",
            name="minlength",
            field=models.SmallIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(500),
                ],
                verbose_name="Min. character count",
            ),
        ),
    ]
