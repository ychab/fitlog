from django.urls import path

from . import views

app_name = 'routines'

urlpatterns = [
    path('routines/', views.RoutineListView.as_view(), name='routine_list'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workouts/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
]
