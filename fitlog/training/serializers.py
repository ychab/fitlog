from django.db import transaction

from rest_framework import serializers

from .models import Exercise, Routine, TrainingLog, Workout, WorkoutExercise


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


class WorkoutListSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer()
    workout_exercises = ExerciseWorkoutDetailSerializer(many=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'name', 'routine', 'workout_exercises', 'url')


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


class TrainingLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingLog
        fields = ('id', 'exercise', 'workout', 'date', 'set', 'reps', 'weight')
