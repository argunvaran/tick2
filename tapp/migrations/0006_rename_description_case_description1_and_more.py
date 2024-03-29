# Generated by Django 4.2.5 on 2023-09-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tapp', '0005_case_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='description',
            new_name='description1',
        ),
        migrations.AddField(
            model_name='case',
            name='description2',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='case',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('pending', 'Pending'), ('closed', 'Closed')], default='open', max_length=20),
        ),
    ]
