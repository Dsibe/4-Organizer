# Generated by Django 2.2.13 on 2021-03-27 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_img_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img_path',
            field=models.CharField(blank=True, default="{% static 'placeholder.png' %}", max_length=200),
        ),
    ]
