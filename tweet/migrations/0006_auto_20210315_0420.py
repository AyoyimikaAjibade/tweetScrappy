# Generated by Django 3.1.7 on 2021-03-15 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0005_auto_20210312_1252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['totalLike']},
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tip',
            field=models.TextField(max_length=140),
        ),
    ]
