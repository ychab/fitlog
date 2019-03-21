from django.urls import path

from . import views

app_name = 'routines'

urlpatterns = [
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('routines/', views.RoutineListView.as_view(), name='routine_list'),
    path('trainings/', views.TrainingListView.as_view(), name='training_list'),
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
]
