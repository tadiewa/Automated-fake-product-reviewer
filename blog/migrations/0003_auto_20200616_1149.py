# Generated by Django 2.2 on 2020-06-16 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(blank=True, default='none', max_length=50, null=True),
        ),
    ]
