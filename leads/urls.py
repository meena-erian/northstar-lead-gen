from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [path("",views.landing,name="landing"),path("thanks/",views.thanks,name="thanks"),path("analytics/event/",views.event,name="event"),path("staff/analytics/",views.dashboard,name="dashboard"),path("staff/login/",auth_views.LoginView.as_view(template_name="registration/login.html"),name="login"),path("staff/logout/",auth_views.LogoutView.as_view(),name="logout")]
