from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from todo_app import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name= 'home'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('add-item', views.add_item, name='add-item'),
    path('delete-item/<int:id>', views.delete_item, name='delete-item'),
    path('edit-item/<int:id>', views.update_item, name='edit-item'),
    path('signup', views.signup_user, name='signup'),
    path('validate/username', csrf_exempt(views.UsernameValidation.as_view()), name='validate-username'),
    path('validate/email', csrf_exempt(views.EmailValidation.as_view()), name='validate-email'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout')
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )