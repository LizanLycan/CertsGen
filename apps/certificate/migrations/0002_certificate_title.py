# Generated by Django 2.2.6 on 2020-01-30 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='title',
            field=models.CharField(max_length=150, null=True),
        ),
    ]