from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views import generic

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import (
    Exercise, Routine, Training, Workout, WorkoutExercise,
    TrainingSet)
from .serializers import (
    ExerciseSerializer, RoutineSerializer, TrainingListSerializer,
    TrainingSaveSerializer, TrainingSerializer,
    WorkoutDetailSerializer, WorkoutSerializer, WorkoutSaveSerializer,
)


class RoutineListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'training/routine_list.html'


class ExerciseListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'training/exercise_list.html'


class WorkoutListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'training/workout_list.html'


class TrainingListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'training/training_list.html'


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
        elif self.action in ['list', 'retrieve']:
            return WorkoutDetailSerializer
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


class TrainingViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ['workout']
    ordering_fields = ('date', 'training_sets__exercice__name', 'training_sets__set')
    ordering = ('-date',)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return TrainingSaveSerializer
        elif self.action == 'list':
            return TrainingListSerializer
        return TrainingSerializer

    def get_queryset(self):
        return (
            Training.objects.all()
            .select_related('workout')
            .prefetch_related(Prefetch(
                'training_sets',
                queryset=TrainingSet.objects.all().select_related('exercise').order_by('exercise__name', 'set')
            ))
        )
