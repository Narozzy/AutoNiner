# Generated by Django 3.0.4 on 2020-03-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Task Name'),
        ),
    ]
