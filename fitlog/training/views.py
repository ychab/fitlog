from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views import generic
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from fitlog.training.models import (
    Exercise, Routine, TrainingLog, Workout, WorkoutExercise,
)
from fitlog.training.serializers import (
    ExerciseSerializer, RoutineSerializer, TrainingLogSerializer,
    WorkoutListSerializer, WorkoutSerializer, WorkoutSaveSerializer,
)


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


class RoutineViewSet(ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)


class ExerciseViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)


class WorkoutViewSet(ModelViewSet):
    queryset = Workout.objects.all()
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return WorkoutSaveSerializer
        elif self.action == 'list':
            return WorkoutListSerializer
        return WorkoutSerializer

    def get_queryset(self):
        return (
            Workout.objects.all()
            .select_related('routine')
            .prefetch_related(Prefetch(
                'workout_exercises',
                queryset=WorkoutExercise.objects.all().select_related('exercise').order_by('order', 'exercise__name')
            ))
        )


class TrainingLogViewSet(ModelViewSet):
    queryset = TrainingLog.objects.all()
    serializer_class = TrainingLogSerializer
