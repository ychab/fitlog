from django.urls import reverse
from django.views.generic import RedirectView


class HomePageRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        if user.is_anonymous:
            return reverse('login')

        return reverse('trainings:workout_list')
