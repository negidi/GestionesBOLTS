# Generated by Django 4.1.3 on 2023-10-16 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_factura_detallefactura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]
