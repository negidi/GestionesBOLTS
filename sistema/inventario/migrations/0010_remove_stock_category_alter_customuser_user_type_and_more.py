# Generated by Django 4.1.3 on 2023-10-19 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_remove_doctor_admin_remove_patientfeedback_admin_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='category',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'AdminHOD'), (2, 'Operador')], default=1, max_length=10),
        ),
        migrations.DeleteModel(
            name='PharmacyClerk',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]
