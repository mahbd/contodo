# Generated by Django 4.2.2 on 2023-06-16 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0004_submissions_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submissions',
            options={'ordering': ['-created_at']},
        ),
    ]