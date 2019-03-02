from django.db import models
from django.utils.timezone import now as tz_now
from django.utils.translation import ugettext_lazy as _


class Routine(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    class Meta:
        db_table = 'routines'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    class Meta:
        db_table = 'exercises'

    def __str__(self):
        return self.name


class Workout(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    routine = models.ForeignKey(Routine, related_name='workouts', on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise, related_name='workouts', through='WorkoutExercise')

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, related_name='workout_exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='workout_exercises', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'workout_exercises'

    def __str__(self):
        return '{} - {}'.format(self.workout.name, self.exercise.name)


class TrainingLog(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name='trainings', on_delete=models.CASCADE)
    # workout = models.ForeignKey(Workout, related_name='training_logs', on_delete=models.CASCADE)
    # exercise = models.ForeignKey(Exercise, related_name='training_logs', on_delete=models.CASCADE)
    date = models.DateTimeField(default=tz_now)
    sets = models.IntegerField()
    reps = models.IntegerField()

    class Meta:
        db_table = 'training_logs'

    def __str__(self):
        return self.name
