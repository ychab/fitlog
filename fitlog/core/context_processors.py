from fitlog.training.models import Workout


def extra(request):
    data = {
        'workouts': [],
    }

    if request.user.is_authenticated:
        data['workouts'] = Workout.objects.all().order_by('name')

    return data
