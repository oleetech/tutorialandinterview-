# Generated by Django 5.1.2 on 2024-11-23 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0005_alter_tutorial_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='level',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Basic', max_length=20),
        ),
    ]
