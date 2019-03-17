from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from fitlog.core.views import HomePageRedirectView
from fitlog.training.views import (
    ExerciseViewSet, RoutineViewSet, TrainingViewSet, WorkoutViewSet,
)

router = DefaultRouter()
router.register('exercises', ExerciseViewSet, base_name='exercise')
router.register('routines', RoutineViewSet, base_name='routine')
router.register('trainings', TrainingViewSet, base_name='training')
router.register('workouts', WorkoutViewSet, base_name='workout')

api_urls = router.urls
api_urls += [
    path('auth-token', obtain_auth_token, name='obtain_token'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),

    path('training/', include('fitlog.training.urls', namespace='trainings')),

    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomePageRedirectView.as_view(), name='home'),
]

# Serve static files in debug mode, check is done later no worry.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    schema_view = get_swagger_view(title='FitLog API')

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),  # For admin views

        path('explore-auth/', include('rest_framework.urls', namespace='rest_framework')),
        path('explore/', schema_view),
    ]


admin.site.site_title = 'FitLog'
admin.site.site_header = 'FitLog'
