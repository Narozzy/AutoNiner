# Generated by Django 3.0.4 on 2020-04-02 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200402_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doorcountinstance',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='doorcountinstance',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tid', to='home.Task'),
        ),
    ]
