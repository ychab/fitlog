from django.db import transaction

from rest_framework import serializers

from .models import (
    Exercise, Routine, Training, TrainingExercise, TrainingExerciseSet, Workout,
    WorkoutExercise,
)


class RoutineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Routine
        fields = ('id', 'name')


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ('id', 'name')


class ExerciseWorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = ('id', 'exercise', 'order', 'sets', 'reps', 'rest_period')


class ExerciseWorkoutDetailSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = ('id', 'exercise', 'order', 'sets', 'reps', 'rest_period')


class WorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ('id', 'name', 'routine', 'workout_exercises')



class WorkoutDetailSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer()
    workout_exercises = ExerciseWorkoutDetailSerializer(many=True)

    class Meta:
        model = Workout
        fields = ('id', 'name', 'routine', 'workout_exercises')


class WorkoutSaveSerializer(serializers.ModelSerializer):
    workout_exercises = ExerciseWorkoutSerializer(many=True)

    class Meta:
        model = Workout
        fields = ('id', 'name', 'routine', 'workout_exercises')

    def create_workout_exercises(self, instance, workout_exercises_data):
        for workout_exercise_data in workout_exercises_data:
            workout_exercise_data['workout'] = instance
            WorkoutExercise.objects.create(**workout_exercise_data)

    def create(self, validated_data):
        workout_exercises_data = validated_data.pop('workout_exercises')
        workout = super().create(validated_data)
        self.create_workout_exercises(workout, workout_exercises_data)
        return workout

    def update(self, instance, validated_data):
        workout_exercises_data = validated_data.pop('workout_exercises')
        instance = super().update(instance, validated_data)

        with transaction.atomic():
            # More simple to remove all and re-add all because we need to add new
            # exercise, remove old, update exercise with new sets and reps, etc.
            WorkoutExercise.objects.filter(workout=instance).delete()
            self.create_workout_exercises(instance, workout_exercises_data)

        return instance


class TrainingExerciseSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingExerciseSet
        fields = ('id', 'order', 'reps', 'weight', 'rest_period', 'tempo')


class TrainingExerciseSerializer(serializers.ModelSerializer):
    training_exercise_sets = TrainingExerciseSetSerializer(many=True)

    class Meta:
        model = TrainingExercise
        fields = ('id', 'exercise', 'training_exercise_sets')


# class TrainingExerciseDetailSerializer(serializers.ModelSerializer):
#     exercise = ExerciseSerializer()
#     training_exercise_sets = TrainingExerciseSetSerializer(many=True)
#
#     class Meta:
#         model = TrainingExercise
#         fields = ('id', 'exercise', 'training_exercise_sets')


class TrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = ('id', 'workout', 'date')


class TrainingListSerializer(serializers.ModelSerializer):
    training_exercises = TrainingExerciseSerializer(many=True)

    class Meta:
        model = Training
        fields = (
            'id', 'date', 'workout', 'training_exercises',
            'sets_total', 'reps_total', 'weights_total', 'rest_avg',
        )


class TrainingSaveSerializer(serializers.ModelSerializer):
    training_exercises = TrainingExerciseSerializer(many=True)

    class Meta:
        model = Training
        fields = ('id', 'date', 'workout', 'training_exercises')

    def create_training_exercises(self, instance, training_exercises_data):

        for training_exercise_data in training_exercises_data:
            sets_data = training_exercise_data.pop('training_exercise_sets')

            training_exercise_data['training'] = instance
            training_exercise = TrainingExercise.objects.create(**training_exercise_data)

            for set_data in sets_data:
                set_data['training_exercise'] = training_exercise
                TrainingExerciseSet.objects.create(**set_data)

    def create(self, validated_data):
        training_exercises_data = validated_data.pop('training_exercises')
        training = super().create(validated_data)
        self.create_training_exercises(training, training_exercises_data)
        return training

    def update(self, instance, validated_data):
        training_exercises_data = validated_data.pop('training_exercises')
        instance = super().update(instance, validated_data)

        with transaction.atomic():
            TrainingExercise.objects.filter(training=instance).delete()
            # Cascade delete is also trigger with queryset.delete() method??
            TrainingExerciseSet.objects.filter(training_exercise__training=instance).delete()
            self.create_training_exercises(instance, training_exercises_data)

        return instance
