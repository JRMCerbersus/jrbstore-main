# jrbstore urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from storeApp import views
from django.contrib.auth import views as auth_views
from storeApp.forms import CustomSetPasswordForm
urlpatterns = [
    path('',views.index, name='inicio'),
    path('admin/', admin.site.urls),
    path('', include('storeApp.urls')),  # Incluir las URLs de storeApp
    path('accounts/',include('django.contrib.auth.urls')),
    #contraseñas
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_combined.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_combined.html'
    ), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_combined.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_combined.html'
    ), name='password_reset_complete'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

