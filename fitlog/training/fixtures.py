"""
We don't use the fixture Django feature because:
 * we can't use the translation support
 * can't dynamically inject data

Thanks to thie website for translations (!) :
https://www.fitnessfriandises.fr/2011/07/lexique-francais-anglais-des-exercices-de-musculation/

"""
import logging

from django.utils.translation import ugettext_lazy as _

from .factories import ExerciseFactory, RoutineFactory, WorkoutFactory, WorkoutExerciseFactory, TrainingFactory, \
    TrainingExerciseFactory, TrainingExerciseSetFactory
from .models import Exercise, Routine, Workout, WorkoutExercise

logger = logging.getLogger('fitlog.generator')


def create_fixtures(limit=50, testing=False):
    create_routines()
    create_exercises()
    create_workouts()
    create_workout_exercises()

    if testing:
        create_training(limit=limit)


def create_routines():
    RoutineFactory(name=_('Half body'), slug='half-body')
    RoutineFactory(name=_('Full body'), slug='full-body')
    RoutineFactory(name=_('Push Pull Legs'), slug='ppl')
    RoutineFactory(name=_('Split 3 days'), slug='split-3d')
    RoutineFactory(name=_('Split 5 days'), slug='split-5d')
    logger.info('Routines created successfully')


def create_exercises():
    # Chest
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Bench press'), slug='bench-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Incline press'), slug='incline-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Decline press'), slug='decline-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Dumbbell bench press'), slug='dumbbell-bench-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Dumbbell incline press'), slug='dumbbell-incline-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Dumbbell decline press'), slug='dumbbell-decline-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Push ups'), slug='push-ups')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Fly'), slug='fly')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Peck deck'), slug='peck-deck')
    ExerciseFactory(muscle=Exercise.MUSCLE_CHEST, name=_('Cable crossover'), slug='cable-crossover')

    # Back
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Deadlift'), slug='deadlift')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Chin up'), slug='chin-up')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Pull up'), slug='pull-up')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Lat pulldown'), slug='lat-pulldown')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Close grip pulldown'), slug='close-grip-pulldown')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Pullover'), slug='pullover')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Cable pullover'), slug='cable-pullover')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Cable row'), slug='cable-row')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Dumbbell row'), slug='dumbbell-row')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('Bent over barbell row'), slug='bent-over-barbell-row')
    ExerciseFactory(muscle=Exercise.MUSCLE_BACK, name=_('T-bar row'), slug='t-bar-row')

    # Shoulders
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Dumbbell press'), slug='dumbbell-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Arnold press'), slug='arnold-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Front raise'), slug='front-raise')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Lateral raise'), slug='lateral-raise')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Cable lateral raise'), slug='cable-lateral-raise')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Bent over raise'), slug='bent-over-raise')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Cable bent over lateral raise'), slug='cable-bent-over-lateral-raise')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Upright row'), slug='upright-row')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Rear deltoid machine'), slug='rear-deltoid-machine')
    ExerciseFactory(muscle=Exercise.MUSCLE_SHOULDERS, name=_('Shrug'), slug='shrug')

    # Biceps
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Dumbbell curl'), slug='dumbbell-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Incline dumbbell curl'), slug='incline-dumbbell-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Concentration curl'), slug='concentration-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Hammer curl'), slug='hammer-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Cable curl'), slug='cable-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Overhead cable curl'), slug='overhead-cable-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Barbell curl'), slug='barbell-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_BICEPS, name=_('Reverse curl'), slug='reverse-curl')

    # Triceps
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Skullcrushers'), slug='skullcrushers')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Triceps pushdown'), slug='triceps-pushdown')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Reverse grip triceps pushdown'), slug='reverse-grip-triceps-pushdown')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Lying triceps extension'), slug='lying-triceps-extension')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Dumbbell triceps extension'), slug='dumbbell-triceps-extension')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('French press'), slug='french-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Kick back'), slug='kick-back')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Dips'), slug='dips')
    ExerciseFactory(muscle=Exercise.MUSCLE_TRICEPS, name=_('Close grip bench press'), slug='close-grip-bench-press')

    # Legs
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Back squat'), slug='back-squat')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Front squat'), slug='front-squat')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Leg press'), slug='leg-press')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Leg extension'), slug='leg-extension')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Leg curl'), slug='leg-curl')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Lunge'), slug='lunge')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Stiff legged deadlift'), slug='stiff-legged-deadlift')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Plié squat'), slug='plie-squat')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Machine adductor'), slug='machine-adductor')
    ExerciseFactory(muscle=Exercise.MUSCLE_LEGS, name=_('Machine abductor'), slug='machine-abductor')

    # Calf
    ExerciseFactory(muscle=Exercise.MUSCLE_CALF, name=_('calf extension'), slug='calf-extension')

    # Glutes
    ExerciseFactory(muscle=Exercise.MUSCLE_GLUTES, name=_('Hip trust'), slug='hip-trust')
    ExerciseFactory(muscle=Exercise.MUSCLE_GLUTES, name=_('Hip extension'), slug='hip-extension')
    ExerciseFactory(muscle=Exercise.MUSCLE_GLUTES, name=_('Lateral leg raise'), slug='lateral-leg-raise')

    # Lower back
    ExerciseFactory(muscle=Exercise.MUSCLE_LOWER_BACK, name=_('Hyperextension'), slug='hyperextension')
    ExerciseFactory(muscle=Exercise.MUSCLE_LOWER_BACK, name=_('Good morning'), slug='good-morning')

    # Abs
    ExerciseFactory(muscle=Exercise.MUSCLE_ABS, name=_('Crunches'), slug='crunches')
    ExerciseFactory(muscle=Exercise.MUSCLE_ABS, name=_('Sit up'), slug='sit-up')
    ExerciseFactory(muscle=Exercise.MUSCLE_ABS, name=_('Hanging knee raise'), slug='hanging-knee-raise')
    ExerciseFactory(muscle=Exercise.MUSCLE_ABS, name=_('Side bend'), slug='side-bend')

    logger.info('Exercises created successfully')


def create_workouts():
    ppl = Routine.objects.get(slug='ppl')
    full_body = Routine.objects.get(slug='full-body')
    half_body = Routine.objects.get(slug='half-body')
    split_3d = Routine.objects.get(slug='split-3d')
    split_5d = Routine.objects.get(slug='split-5d')

    # PPL
    WorkoutFactory(
        name=_('Push'),
        slug='push',
        routine=ppl,
    )
    WorkoutFactory(
        name=_('Pull'),
        slug='pull',
        routine=ppl,
    )
    WorkoutFactory(
        name=_('Legs'),
        slug='legs',
        routine=ppl,
    )

    # Fullbody
    WorkoutFactory(
        name=_('Full body'),
        slug='full-body',
        routine=full_body,
    )

    # Half body
    WorkoutFactory(
        name=_('Half body top'),
        slug='half-body-top',
        routine=half_body,
    )
    WorkoutFactory(
        name=_('Half body bottom'),
        slug='half-body-bottom',
        routine=half_body,
    )

    # Split on 3 days
    WorkoutFactory(
        name=_('Split 3 days Chest/Biceps/Abs'),
        slug='split-3d-chest-biceps-abs',
        routine=split_3d,
    )
    WorkoutFactory(
        name=_('Split 3 days Legs/Calf'),
        slug='split-3d-legs-calf',
        routine=split_3d,
    )
    WorkoutFactory(
        name=_('Split 3 days Back/Shoulders/Triceps'),
        slug='split-3d-back-shoulders-triceps',
        routine=split_3d,
    )

    # Split on 5 days
    WorkoutFactory(
        name=_('Split 5 days Back'),
        slug='split-5d-back',
        routine=split_5d,
    )
    WorkoutFactory(
        name=_('Split 5 days Shoulders'),
        slug='split-5d-shoulders',
        routine=split_5d,
    )
    WorkoutFactory(
        name=_('Split 5 days Legs'),
        slug='split-5d-legs',
        routine=split_5d,
    )
    WorkoutFactory(
        name=_('Split 5 days Chest'),
        slug='split-5d-chest',
        routine=split_5d,
    )
    WorkoutFactory(
        name=_('Split 5 days Arms'),
        slug='split-5d-arms',
        routine=split_5d,
    )

    logger.info('Workouts created successfully')


def create_workout_exercises():

    workout_exercises = {
        'push': {
            # Chest
            'bench-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'dumbbell-incline-press': {
                'sets': 3,
                'reps': 10,
                'rest_period': 120,
            },
            'cable-crossover': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
            # Shoulders
            'dumbbell-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-lateral-raise': {
                'sets': 4,
                'reps': 15,
                'rest_period': 60,
            },
            'bent-over-raise': {
                'sets': 4,
                'reps': 15,
                'rest_period': 60,
            },
            # Triceps
            'skullcrushers': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
            'triceps-pushdown': {
                'sets': 3,
                'reps': 15,
                'rest_period': 60,
            },
        },
        'pull': {
            # Back
            'deadlift': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'lat-pulldown': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-row': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-pullover': {
                'sets': 4,
                'reps': 15,
                'rest_period': 60,
            },
            # Biceps
            'incline-dumbbell-curl': {
                'sets': 3,
                'reps': 10,
                'rest_period': 90,
            },
            'concentration-curl': {
                'sets': 3,
                'reps': 10,
                'rest_period': 60,
            },
        },
        'legs': {
            # Legs
            'back-squat': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-extension': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            'leg-curl': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            # Calf
            'calf-extension': {
                'sets': 3,
                'reps': 15,
                'rest_period': 60,
            },
        },
        ### Full body ###
        'push': {
            # Legs
            'back-squat': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            # Chest
            'dumbbell-bench-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            # Shoulders
            'cable-lateral-raise': {
                'sets': 4,
                'reps': 15,
                'rest_period': 60,
            },
            # Back
            'lat-pulldown': {
                'sets': 4,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-row': {
                'sets': 4,
                'reps': 10,
                'rest_period': 90,
            },
            # Biceps
            'dumbbell-curl': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
            # Triceps
            'close-grip-bench-press': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
        },
        ### Half body ###
        'half-body-top': {
            # Chest
            'dumbbell-bench-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            # Back
            'lat-pulldown': {
                'sets': 4,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-row': {
                'sets': 4,
                'reps': 10,
                'rest_period': 90,
            },
            # Shoulders
            'cable-lateral-raise': {
                'sets': 5,
                'reps': 15,
                'rest_period': 60,
            },
            # Triceps
            'close-grip-bench-press': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
            # Biceps
            'dumbbell-curl': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
        },
        'half-body-bottom': {
            # Legs
            'back-squat': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-extension': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            'leg-curl': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            # Calf
            'calf-extension': {
                'sets': 3,
                'reps': 15,
                'rest_period': 60,
            },
        },
        ### Split 3 days
        'split-3d-chest-biceps-abs': {
            # Chest
            'bench-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'dumbbell-incline-press': {
                'sets': 3,
                'reps': 10,
                'rest_period': 120,
            },
            'cable-crossover': {
                'sets': 3,
                'reps': 12,
                'rest_period': 90,
            },
            # Biceps
            'dumbbell-curl': {
                'sets': 5,
                'reps': 12,
                'rest_period': 90,
            },
            # Abs
            'crunches': {
                'sets': 3,
                'reps': 20,
                'rest_period': 60,
            },
        },
        'split-3d-legs-calf': {
            # Legs
            'back-squat': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-extension': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            'leg-curl': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            # Calf
            'calf-extension': {
                'sets': 3,
                'reps': 15,
                'rest_period': 60,
            },
        },
        'split-3d-back-shoulders-triceps': {
            # Back
            'deadlift': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'lat-pulldown': {
                'sets': 4,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-row': {
                'sets': 4,
                'reps': 10,
                'rest_period': 90,
            },
            # Shoulders
            'cable-lateral-raise': {
                'sets': 5,
                'reps': 15,
                'rest_period': 60,
            },
            # Triceps
            'skullcrushers': {
                'sets': 5,
                'reps': 12,
                'rest_period': 90,
            },
        },
        ### Split 5 days
        'split-5d-back': {
            'deadlift': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'lat-pulldown': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-row': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-pullover': {
                'sets': 4,
                'reps': 15,
                'rest_period': 60,
            },
        },
        'split-5d-shoulders': {
            'dumbbell-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'cable-lateral-raise': {
                'sets': 5,
                'reps': 15,
                'rest_period': 60,
            },
            'bent-over-raise': {
                'sets': 5,
                'reps': 15,
                'rest_period': 60,
            },
            'crunches': {
                'sets': 3,
                'reps': 20,
                'rest_period': 60,
            },
        },
        'split-5d-legs': {
            # Legs
            'back-squat': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'leg-extension': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            'leg-curl': {
                'sets': 4,
                'reps': 12,
                'rest_period': 90,
            },
            # Calf
            'calf-extension': {
                'sets': 3,
                'reps': 15,
                'rest_period': 60,
            },
        },
        'split-5d-chest': {
            'bench-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'dumbbell-incline-press': {
                'sets': 5,
                'reps': 10,
                'rest_period': 120,
            },
            'cable-crossover': {
                'sets': 5,
                'reps': 12,
                'rest_period': 90,
            },
            'crunches': {
                'sets': 3,
                'reps': 20,
                'rest_period': 60,
            },
        },
        'split-5d-arms': {
            # Triceps
            'skullcrushers': {
                'sets': 5,
                'reps': 12,
                'rest_period': 90,
            },
            'triceps-pushdown': {
                'sets': 5,
                'reps': 15,
                'rest_period': 60,
            },
            # Biceps
            'incline-dumbbell-curl': {
                'sets': 5,
                'reps': 10,
                'rest_period': 90,
            },
            'concentration-curl': {
                'sets': 5,
                'reps': 10,
                'rest_period': 60,
            },
        },
    }

    for workout_slug, workout_exercise in workout_exercises.items():
        workout = Workout.objects.get(slug=workout_slug)

        order = 1
        for exercise_slug, exercise_sets in workout_exercise.items():
            exercise = Exercise.objects.get(slug=exercise_slug)

            WorkoutExerciseFactory(
                workout=workout,
                exercise=exercise,
                order=order,
                sets=exercise_sets['sets'],
                reps=exercise_sets['reps'],
                rest_period=exercise_sets['rest_period'],
            )
            order += 1

    logger.info('Workout exercises created successfully')


def create_training(limit=10):
    workouts = [
        'push',
        'pull',
        'legs',
        'full-body',
        'half-body-top',
        'half-body-bottom',
        'split-3d-chest-biceps-abs',
        'split-3d-legs-calf',
        'split-3d-back-shoulders-triceps',
        'split-5d-back',
        'split-5d-shoulders',
        'split-5d-legs',
        'split-5d-chest',
        'split-5d-arms',
    ]

    logger.info('Start trainings generation for...')
    for workout_slug in workouts:
        workout = Workout.objects.get(slug=workout_slug)
        workout_exercises = WorkoutExercise.objects.filter(workout=workout)

        logger.info('... {} ...'.format(workout))
        for i in range(0, limit):
            training = TrainingFactory(workout=workout)
            logger.info('> {} training(s)'.format(i + 1))

            for workout_exercise in  workout_exercises:
                training_exercise = TrainingExerciseFactory(
                    training=training,
                    exercise=workout_exercise.exercise,
                )

                for set in range(1, workout_exercise.sets + 1):
                    TrainingExerciseSetFactory(
                        training_exercise=training_exercise,
                        order=set,
                    )
