# Generated by Django 4.2.2 on 2023-06-15 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CFUsers',
            fields=[
                ('handle', models.CharField(max_length=63, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.URLField(blank=True, max_length=255, null=True)),
                ('last_submission', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetProblems',
            fields=[
                ('problem_name', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=255, primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetSolves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'Not Read'), ('R', 'Read'), ('T', 'Tried'), ('S', 'Solved')], default='N', max_length=3)),
                ('last_change', models.DateTimeField(blank=True, null=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeforces.targetproblems')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeforces.cfusers')),
            ],
        ),
        migrations.AddField(
            model_name='targetproblems',
            name='users',
            field=models.ManyToManyField(through='codeforces.TargetSolves', to='codeforces.cfusers'),
        ),
        migrations.CreateModel(
            name='Submissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_link', models.URLField(max_length=255)),
                ('problem_name', models.CharField(max_length=255)),
                ('contest_id', models.IntegerField()),
                ('problem_id', models.CharField(max_length=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeforces.cfusers')),
            ],
        ),
    ]
