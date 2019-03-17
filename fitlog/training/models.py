from datetime import date

from django.db import models
from django.db.models import Avg, Sum
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
    """
    To suggest exercises to log per training, we must define a list of exercises
    for a workout.
    """
    workout = models.ForeignKey(Workout, related_name='workout_exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='workout_exercises', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    sets = models.IntegerField()
    reps = models.IntegerField()
    rest_period = models.IntegerField(help_text='In seconds', default=90)

    class Meta:
        db_table = 'workout_exercises'


class Training(models.Model):
    # Instead of having a foreign key on WorkoutExercise which is too much
    # restrictive, we open the model.
    # exercise = models.ForeignKey(Exercise, related_name='trainings', on_delete=models.CASCADE)
    # Workout is optional. Sometimes, you may have a freestyle training!
    workout = models.ForeignKey(Workout, null=True, related_name='trainings', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        db_table = 'trainings'

    # Yes, we are doing SQL queries for each of this called methods. This is not
    # the end of time because remember, this is a **personal** app ;-)
    def sets(self):
        return self.training_sets.count()

    def reps(self):
        return round(self.training_sets.aggregate(Sum('reps')).get('reps__sum', None), 2)

    def weights(self):
        return round(self.training_sets.aggregate(Sum('weight')).get('weight__sum', None), 2)

    def rest_avg(self):
        return round(self.training_sets.aggregate(Avg('rest_period')).get('rest_period__avg', None), 2)


class TrainingSet(models.Model):
    training = models.ForeignKey(Training, related_name='training_sets', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='training_sets', on_delete=models.CASCADE)

    set = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    rest_period = models.IntegerField(help_text='In seconds', null=True, blank=True)
    tempo = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        db_table = 'training_sets'
