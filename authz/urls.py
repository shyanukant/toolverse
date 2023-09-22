from django.urls import path
from .views import signup_view, login_view, logout_view, ValidateAccountView, ResetPasswordView, SetNewPasswordView

app_name = 'authz'
urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('validate/<uidb64>/<token>/', ValidateAccountView.as_view() , name='validate'),
    path('reset-password/', ResetPasswordView.as_view(), name='resetpass'),
    path('set-new-password/<uidb64>/<token>/', SetNewPasswordView.as_view() , name='setpassword'),
]