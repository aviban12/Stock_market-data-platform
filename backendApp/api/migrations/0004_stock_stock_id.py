# Generated by Django 4.2.3 on 2023-07-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_stock_created_at_stock_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='stock_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
