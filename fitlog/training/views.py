from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from fitlog.training.models import Exercise, Routine, Workout


class RoutineListView(LoginRequiredMixin, generic.ListView):
    model = Routine
    queryset = Routine.objects.all()


class ExerciseListView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    queryset = Exercise.objects.all()


class WorkoutListView(LoginRequiredMixin, generic.ListView):
    model = Workout
    queryset = Workout.objects.all()


class WorkoutDetailView(LoginRequiredMixin, generic.DetailView):
    model = Workout
