# Generated by Django 5.0 on 2024-02-23 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('refund', 'Refund'), ('cancelled', 'Cancelled')], default='paid', max_length=20),
        ),
    ]