from datetime import date

from django.db import models
from django.db.models import Avg, Sum
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class SlugModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Routine(SlugModel):

    class Meta:
        db_table = 'routines'


class Exercise(SlugModel):

    MUSCLE_CHEST = 'chest'
    MUSCLE_BACK = 'back'
    MUSCLE_SHOULDERS = 'shoulders'
    MUSCLE_BICEPS = 'biceps'
    MUSCLE_TRICEPS = 'triceps'
    MUSCLE_LOWER_BACK = 'lower_back'
    MUSCLE_GLUTES = 'glutes'
    MUSCLE_LEGS = 'legs'
    MUSCLE_CALF = 'calf'
    MUSCLE_ABS = 'abs'
    MUSCLES = (
        (MUSCLE_CHEST, _('Chest')),
        (MUSCLE_BACK, _('Back')),
        (MUSCLE_SHOULDERS, _('Shoulders')),
        (MUSCLE_BICEPS, _('Biceps')),
        (MUSCLE_TRICEPS, _('Triceps')),
        (MUSCLE_LOWER_BACK, _('Lower back')),
        (MUSCLE_GLUTES, _('Glutes')),
        (MUSCLE_LEGS, _('Legs')),
        (MUSCLE_CALF, _('Calf')),
        (MUSCLE_ABS, _('Abs')),
    )

    muscle = models.CharField(max_length=128, choices=MUSCLES)

    class Meta:
        db_table = 'exercises'


class Workout(SlugModel):
    routine = models.ForeignKey(Routine, related_name='workouts', on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise, related_name='workouts', through='WorkoutExercise')

    class Meta:
        db_table = 'workouts'


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
    # Workout is optional. Sometimes, you may have a freestyle training!
    workout = models.ForeignKey(Workout, null=True, related_name='trainings', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        db_table = 'trainings'

    # Yes, we are doing SQL queries for each of this called methods. This is not
    # the end of time because remember, this is a **personal** app ;-)
    def sets_total(self):
        return TrainingExerciseSet.objects.filter(training_exercise__training=self).count()

    def reps_total(self):
        return round(
            TrainingExerciseSet.objects
                .filter(training_exercise__training=self)
                .aggregate(Sum('reps'))
                .get('reps__sum', None),
            2
        )

    def weights_total(self):
        return round(
            TrainingExerciseSet.objects
                .filter(training_exercise__training=self)
                .aggregate(Sum('weight'))
                .get('weight__sum', None),
            2
        )

    def rest_avg(self):
        return round(
            TrainingExerciseSet.objects
                .filter(training_exercise__training=self)
                .aggregate(Avg('rest_period'))
                .get('rest_period__avg', None),
            2
        )


class TrainingExercise(models.Model):
    training = models.ForeignKey(Training, related_name='training_exercises', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name='training_exercises', on_delete=models.CASCADE)

    class Meta:
        db_table = 'training_exercises'


class TrainingExerciseSet(models.Model):
    training_exercise = models.ForeignKey(TrainingExercise, related_name='training_exercise_sets', on_delete=models.CASCADE)

    order = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    rest_period = models.IntegerField(help_text='In seconds', null=True, blank=True)
    tempo = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        db_table = 'training_exercise_sets'
