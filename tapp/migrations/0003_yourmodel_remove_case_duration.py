# Generated by Django 4.2.5 on 2023-09-19 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tapp', '0002_alter_case_start_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('view_your_model', 'Can view Your Model')],
            },
        ),
        migrations.RemoveField(
            model_name='case',
            name='duration',
        ),
    ]
