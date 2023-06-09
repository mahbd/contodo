# Generated by Django 4.2.2 on 2023-06-15 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeforces', '0002_alter_targetproblems_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfusers',
            name='last_online',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submissions',
            name='status',
            field=models.CharField(choices=[('T', 'Tried'), ('S', 'Solved')], default='T', max_length=1),
        ),
    ]
