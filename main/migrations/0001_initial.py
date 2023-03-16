# Generated by Django 4.1.7 on 2023-03-16 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('judge', models.CharField(choices=[('Codeforces', 'Codeforces'), ('AtCoder', 'AtCoder'), ('LeetCode', 'LeetCode'), ('Toph', 'Toph')], max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('unique_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PushedContest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pushed_time', models.DateTimeField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]