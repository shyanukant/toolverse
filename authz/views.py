import re
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import  default_token_generator
from django.conf import settings

# Create your views here.
# Signup view
def signup_view(request):
    flag = 0

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.warning(request, "Password is not matching.")
            return redirect(reverse("authz:signup"))

        if len(password) < 8:
            messages.warning(request, "Password must be atleast 8 characters.")
            return redirect(reverse("authz:signup"))
        
        elif not re.search("[a-z]", password):
            flag = -1
        elif not re.search("[A-Z]", password):
            flag = -1
        elif not re.search("[0-9]", password):
            flag = -1
        elif not re.search("[_!@#$%^&*]", password):
            flag = -1
        else:
            pass

        if flag == 0:
            try :
                if User.objects.get(username=email):
                    messages.info(request, "Email already reigster!")
                    return redirect(reverse("authz:signup"))
            except Exception as Identifier:
                pass

            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.is_active = False
            user.save()

            # send account activation or verification email
            email_subject = 'Verify your account'
            current_site = get_current_site(request)
            message = render_to_string('auth/validate.html',
                                       {
                                           'user' : user,
                                           'domain' : current_site,
                                           'uid' : urlsafe_base64_encode(force_bytes(user.pk)), 
                                           'token': default_token_generator.make_token(user)
                                       })

            # email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            # email_message.send()
            messages.success(request, f"{message}")
            return redirect('authz:login')
        else:
            messages.error(request, "Please Enter valid password!!")
            return redirect(reverse("authz:signup"))

    return render(request, 'auth/auth.html',  {'auth': 'signup' , 'head_info' : 'Create and account'})

# Sign in view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('contents:dashboard')
        else:
            messages.error(request, "Invalid Credentails!!")
            return redirect(reverse('authz:login'))

    return render(request, 'auth/auth.html',  {'auth': 'login', 'head_info' : 'Login in to your account'})

# logout view
def logout_view(request):
    logout(request)
    messages.success(request, "logout Successfull!!")
    return render(request, 'auth/auth.html',  {'auth': 'login', 'head_info' : 'Login in to your account'})


class ValidateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(f"Error decoding uidb64: {e}")
            user = None

        # print(uid, user, default_token_generator.check_token(user, token))
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, 'Account Verified Successfully! Login Now')
            return redirect('authz:login')
        return render(request, 'auth/validate-fail.html')
    
class ResetPasswordView(View):
    template_name = 'auth/auth.html'
    def get(self, request):
        return render(request, self.template_name, {'auth': 'reset_pass', 'head_info' : 'Reset Password'})
    
    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            email_subject = "[ Reset your password ]"
            message = render_to_string('auth/request-reset-pass.html', {
                'domain': '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': default_token_generator.make_token(user[0])
            })

            # email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER ,[email])
            # email_message.send()

            messages.info(request, f"{message}")
            return render(request, self.template_name)
        else:
            messages.error(request, "No account exists with this email.")
            return render(request, self.template_name,  {'auth': 'reset_pass', 'head_info' : 'Forgot your password?'})
        
class SetNewPasswordView(View):
    template_name = 'auth/auth.html'
    def get(self, request, uidb64, token):
        context = {
            'uid' : uidb64,
            'token' : token,
            'auth' : 'set_pass',
            'head_info' : 'Set New Password'
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not default_token_generator.check_token(user, token):
                messages.warning(request, 'Password Reset link is Invalid!')
                return redirect('auth:reset_pass')

        except DjangoUnicodeDecodeError as identifier:
            pass
        return render(request, self.template_name, context)
    
    def post(self, request, uidb64, token):
        context = {
            'uid' : uidb64,
            'token' : token,
            'auth' : 'set_pass',
            'head_info' : 'Set New Password'
        }
        flag = 0
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.warning(request, 'Password is Not Matching')
            return render(request, self.template_name, context)
        
        messages.success(request, "New password set successfully! Login in your account")
        return redirect('authz:login')
