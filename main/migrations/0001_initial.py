# Generated by Django 2.2.2 on 2019-08-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=300, null=True)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('period', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
