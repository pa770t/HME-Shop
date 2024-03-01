# Generated by Django 5.0 on 2024-02-23 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_membership_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='level',
            field=models.CharField(choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum'), ('Diamond', 'Diamond')], default='Bronze', max_length=8),
        ),
    ]