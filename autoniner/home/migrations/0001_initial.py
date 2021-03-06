# Generated by Django 3.0.4 on 2020-03-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('title', models.CharField(max_length=50, verbose_name='Task Title')),
                ('description', models.CharField(blank=True, max_length=50, verbose_name='Task Description')),
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'tasks',
                'ordering': ['date_created'],
                'get_latest_by': ['date_created'],
            },
        ),
    ]
