# Generated by Django 5.1.2 on 2024-11-22 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='created_at',
            new_name='submitted_at',
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='mcq_answer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='example_code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Basic', max_length=20),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MCQ', 'Multiple Choice Question'), ('CODE', 'Code-based Question'), ('TEXT', 'Text-based Question')], default='TEXT', max_length=10),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
