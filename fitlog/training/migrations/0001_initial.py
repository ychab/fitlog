# Generated by Django 2.1.7 on 2019-03-27 21:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'db_table': 'exercises',
            },
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'db_table': 'routines',
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'db_table': 'trainings',
            },
        ),
        migrations.CreateModel(
            name='TrainingExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_exercises', to='training.Exercise')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_exercises', to='training.Training')),
            ],
            options={
                'db_table': 'training_exercises',
            },
        ),
        migrations.CreateModel(
            name='TrainingExerciseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('weight', models.FloatField()),
                ('rest_period', models.IntegerField(blank=True, help_text='In seconds', null=True)),
                ('tempo', models.CharField(blank=True, max_length=7, null=True)),
                ('training_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_exercise_sets', to='training.TrainingExercise')),
            ],
            options={
                'db_table': 'training_exercise_sets',
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'db_table': 'workouts',
            },
        ),
        migrations.CreateModel(
            name='WorkoutExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('sets', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('rest_period', models.IntegerField(default=90, help_text='In seconds')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_exercises', to='training.Exercise')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_exercises', to='training.Workout')),
            ],
            options={
                'db_table': 'workout_exercises',
            },
        ),
        migrations.AddField(
            model_name='workout',
            name='exercises',
            field=models.ManyToManyField(related_name='workouts', through='training.WorkoutExercise', to='training.Exercise'),
        ),
        migrations.AddField(
            model_name='workout',
            name='routine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='training.Routine'),
        ),
        migrations.AddField(
            model_name='training',
            name='workout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='training.Workout'),
        ),
    ]
