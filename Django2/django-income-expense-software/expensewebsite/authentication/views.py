from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth

from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator


# Create your views here.
class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            response = {'email_error': 'Email is invalid'}
            return JsonResponse(response, status=400)
        elif User.objects.filter(email=email).exists():
            response = {'email_error': 'sorry the email already exists!'}
            return JsonResponse(response, status=409)
        response = {'email_valid': True}
        return JsonResponse(response, status=200)


class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            response = {'username_error': 'username should only contain alphaneumeric characters'}
            return JsonResponse(response, status=400)
        elif User.objects.filter(username=username).exists():
            response = {'username_error': 'sorry the username already exists!'}
            return JsonResponse(response, status=409)
        response = {'username_valid': True}
        return JsonResponse(response, status=200)


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password1 = request.POST['password2']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if password == password1:
                    if len(password) < 6:
                        messages.error(request, "Password too short")
                        return render(request, 'authentication/register.html', context)
                    else:
                        user = User.objects.create_user(username=username, email=email)
                        user.set_password(password)

                        # - path to view of activation
                        # - getting domain we are on
                        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                        # - token
                        token = token_generator.make_token(user)
                        domain = get_current_site(request).domain
                        link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                        # - relative url to verification
                        activate_url = 'http://' + domain + link

                        email_subject = 'Activate your account'
                        email_body = 'Hi ' + user.username + ' Please use this link to activate your account\n' + activate_url
                        email = EmailMessage(
                            email_subject,
                            email_body,
                            'noreply@gmail.com',
                            [email],
                        )
                        email.send(fail_silently=False)
                        user.is_active = False
                        user.save()
                        messages.success(request, 'Account successfully created check activation link on email')
                        return render(request, 'authentication/register.html')

                else:
                    messages.error(request, "Passwords does not match")
                    return render(request, 'authentication/register.html', context)

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if user.is_active:
            messages.success(request, 'Account already activated')
            return redirect('login')
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully')
        return redirect('login')

        # return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' + username + ' you are logged in successfully')
                    return redirect('expenses')
                else:
                    messages.error(request, 'Account not activated please check your email')
            else:
                messages.error(request, 'Username or password is invalid!')
        else:
            messages.error(request, 'Please enter username and password!')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Logout successful')
        return redirect('login')
