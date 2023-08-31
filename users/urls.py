from . import views
from django.urls import path
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',views.sign_up,name='sign_up'),
    path('profile/',views.profile,name='profile'),
    path('login/',authViews.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',authViews.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)