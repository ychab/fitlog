from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import (
    Exercise, Routine, Training, TrainingExercise, TrainingExerciseSet, Workout,
)


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
    list_display = ['name', 'routine', 'exercises_suggestions']
    list_display_links = ['name']
    list_select_related = ['routine']
    inlines = [WorkoutExercisesInline]
    exclude = ('exercises',)
    ordering = ['name']
    search_fields = ['name']

    def exercises_suggestions(self, obj):
        output = '<ul>'
        for exercise in obj.exercises.all():
            output += '<li>{}</li>'.format(exercise)
        output += '</ul>'
        return format_html(output)
    exercises_suggestions.short_description = _('Exercises')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'workout',
        'date',
    ]
    list_display_links = ['id']
    list_filter = ['date']
    list_select_related = ['workout']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(TrainingExercise)
class TrainingExerciseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'training',
        'exercise',
    ]
    list_display_links = ['id']
    list_select_related = ['training', 'exercise']


@admin.register(TrainingExerciseSet)
class TrainingExerciseSetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'training_exercise',
        'order',
        'reps',
        'weight',
        'rest_period',
        'tempo',
    ]
    list_display_links = ['id']
    list_select_related = ['training_exercise']
    ordering = ['-training_exercise__training__date']
    search_fields = ['training_exercise__exercise__name']
