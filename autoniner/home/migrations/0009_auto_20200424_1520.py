# Generated by Django 3.0.4 on 2020-04-24 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20200402_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('DOOR', 'DOOR'), ('QUESTIONS', 'QUESTIONS')], default='door count', max_length=10),
        ),
        migrations.CreateModel(
            name='QuestionsInstance',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('internal_notes', models.CharField(max_length=1000)),
                ('ip_address', models.CharField(max_length=100)),
                ('entered_by', models.CharField(max_length=100)),
                ('desk_location', models.CharField(max_length=100)),
                ('question', models.CharField(max_length=100)),
                ('question_type', models.CharField(max_length=1000)),
                ('date', models.DecimalField(decimal_places=20, max_digits=100)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskid', to='home.Task')),
            ],
        ),
    ]
