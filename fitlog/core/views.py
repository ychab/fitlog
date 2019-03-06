from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView

from fitlog.training.models import Exercise, Routine


class HomePageRedirectView(RedirectView):
    permanent = True

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return HttpResponseRedirect(reverse('login'))

        if Routine.objects.count() == 0:
            messages.info(request, _('Please create routines.'))
            return HttpResponseRedirect(reverse('trainings:routine_list'))

        elif Exercise.objects.count() == 0:
            messages.info(request, _('Please create exercises.'))
            return HttpResponseRedirect(reverse('trainings:exercise_list'))

        return HttpResponseRedirect(reverse('trainings:workout_list'))
