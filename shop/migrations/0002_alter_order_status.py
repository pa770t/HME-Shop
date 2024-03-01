# Generated by Django 5.0 on 2024-02-22 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('refund', 'Refund'), ('cancelled', 'Cancelled')], default='PENDING', max_length=20),
        ),
    ]
