from django.utils.translation import get_language, to_locale

import factory
from factory import fuzzy

from fitlog.training.models import (
    Exercise, Routine, Training, Workout, WorkoutExercise,
    TrainingExercise, TrainingExerciseSet)

language = get_language() or 'en-us'
locale = to_locale(language)


class SlugFactory(factory.DjangoModelFactory):

    class Meta:
        abstract = True
        django_get_or_create = ('slug',)

    slug = factory.Faker('slug', locale=locale)
    name = factory.LazyAttribute(lambda o: o.slug)


class RoutineFactory(SlugFactory):

    class Meta:
        model = Routine


class ExerciseFactory(SlugFactory):

    class Meta:
        model = Exercise

    muscle = fuzzy.FuzzyChoice(dict(Exercise.MUSCLES).keys())


class WorkoutFactory(SlugFactory):

    class Meta:
        model = Workout

    routine = factory.SubFactory(RoutineFactory)

    @factory.post_generation
    def exercises(self, create, extracted, **kwargs):
        if create and extracted:
            for exercise in extracted:
                WorkoutExerciseFactory(
                    workout=self,
                    exercise=exercise,
                )


class WorkoutExerciseFactory(factory.DjangoModelFactory):

    class Meta:
        model = WorkoutExercise

    workout = factory.SubFactory(WorkoutFactory)
    exercise = factory.SubFactory(ExerciseFactory)
    order = factory.Sequence(lambda n: n)
    sets = fuzzy.FuzzyInteger(1, 5)
    reps = fuzzy.FuzzyInteger(6, 15)
    rest_period = fuzzy.FuzzyInteger(60, 180)


class TrainingFactory(factory.DjangoModelFactory):

    class Meta:
        model = Training

    workout = factory.SubFactory(WorkoutFactory)


class TrainingExerciseFactory(factory.DjangoModelFactory):

    class Meta:
        model = TrainingExercise

    training = factory.SubFactory(TrainingFactory)
    exercise = factory.SubFactory(ExerciseFactory)


class TrainingExerciseSetFactory(factory.DjangoModelFactory):

    class Meta:
        model = TrainingExerciseSet

    training_exercise = factory.SubFactory(TrainingExerciseFactory)
    order = factory.Sequence(lambda n: n)
    reps = fuzzy.FuzzyInteger(6, 15)
    weight = fuzzy.FuzzyFloat(4, 150, precision=2)
    rest_period = fuzzy.FuzzyInteger(60, 180)
