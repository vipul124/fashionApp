# Generated by Django 4.1.3 on 2024-10-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_product_variants_alter_variant_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='options',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='video',
            name='hashtags',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
