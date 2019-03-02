from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Exercise, Routine, TrainingLog, Workout, WorkoutExercise


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    ordering = ['name']
    search_fields = ['name']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    ordering = ['name']
    search_fields = ['name']


class WorkoutExercisesInline(admin.TabularInline):
    model = Workout.exercises.through


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'routine', 'exercises_list']
    list_display_links = ['name']
    list_select_related = ['routine']
    inlines = [WorkoutExercisesInline]
    exclude = ('exercises',)
    ordering = ['name']
    search_fields = ['name']

    def exercises_list(self, obj):
        output = '<ul>'
        for exercise in obj.exercises.all():
            output += '<li>{}</li>'.format(exercise)
        output += '</ul>'
        return format_html(output)
    exercises_list.short_description = _('Exercises')


@admin.register(TrainingLog)
class TrainingLogAdmin(admin.ModelAdmin):
    # list_display = [
    #     'id',
    #     'workout_exercise__workout__name',
    #     'workout_exercise__exercise__name',
    #     'date',
    #     'sets',
    #     'reps',
    # ]
    list_display = [
        'id',
        'workout_name',
        'exercise_name',
        'date',
        'sets',
        'reps',
    ]
    list_display_links = ['id']
    list_filter = ['date']
    ordering = ['-date']
    date_hierarchy = 'date'
    search_fields = ['workout_exercice__exercise__name']

    def workout_name(self, obj):
        return str(obj.workout_exercise.workout)
    workout_name.short_description = _('Workout')

    def exercise_name(self, obj):
        return str(obj.workout_exercise.exercise)
    exercise_name.short_description = _('Exercise')