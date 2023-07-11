import operator
from functools import reduce
from smtplib import SMTPException

import requests
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from .forms import ProfileForm, LoginForm
from .models import Profile
from .utils import generate_random_string

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def index(request):
    request.session['active'] = 'index'
    return render(request, 'landing-page.html', {})


# @login_required
@cache_page(CACHE_TTL)
def listing(request, category_id=None):
    request.session['active'] = 'movies-list'
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    headers = {
        "X-RapidAPI-Key": settings.RAPID_API_KEY,
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    querystring = {"sort": "year.decr", "limit": "12", 'page': request.GET.get('page', 1)}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        data['next'] = data['next'].replace('/titles', reverse('movies-list'))
    except Exception:
        data = {'results': [], 'entries': 0, 'error': True}
    # print(data)
    return render(request, 'listing.html', {'data': data})


@login_required
def movie_detail(request, movie_id):
    return render(request, 'detail.html', {})


@login_required
def categories(request):
    return render(request, 'movie-categories.html', {})


@csrf_exempt
def login_view(request):
    request.session['active'] = 'login'
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    form = LoginForm(request=request)
    if request.POST:
        form = LoginForm(request.POST, request=request)
        remember_me = request.POST.get('remember_me') == 'on'
        request.session.set_expiry(1209600 if remember_me else 1209600)
        if form.is_valid():
            if request.POST.get('next', None):
                next_page = request.POST.get('next')
            else:
                next_page = reverse('index')
            # return JsonResponse({'status': 'success', 'message': 'Login successful. Redirecting ...',
            # 'page': next_page})
            return HttpResponseRedirect(next_page)
        else:
            return JsonResponse({'status': 'error', 'errors': {k: v[0] for k, v in form.errors.items()}})
    return render(request, 'login.html', {'form': form})


def logout(request):
    from django.contrib import auth
    request.session.clear()
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def reset_password(request):
    if request.POST:
        # search for profiles
        post = request.POST.get('email').lower()

        params = [Q(**{'email__iexact': post}), Q(**{'phone__iexact': post})]

        query = reduce(operator.or_, (i for i in params))
        try:
            instance = Profile.objects.get(query)

            from django.conf import settings
            from django.template.loader import render_to_string
            password = generate_random_string(4)
            instance.set_password(password)
            instance.save()
            html_content = render_to_string('email/reset-password.html', {'instance': instance, 'password': password})

            msg = EmailMessage('ALX-Movie-App - Password Reset', html_content, settings.DEFAULT_FROM_EMAIL,
                               [instance.email])
            msg.content_subtype = "html"
            try:
                print("Sending Reset Password Message .....")
                msg.send(fail_silently=True)
                return JsonResponse({
                    'status': 'success', 'message':
                        'Your password was reset and an email has been sent to the email attached to the found profile.'
                })
            except SMTPException as e:
                print(e.__str__())
                return JsonResponse({
                    'status': 'error', 'message':
                        "Sorry, We couldn't send a reset email. You can try again after a few seconds."})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "Sorry, We couldn't find your profile."})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Something went wrong. Please try again later'})
    return render(request, 'reset-password.html', {})


def registration(request):
    form = ProfileForm()
    if request.POST:
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile Saved successfully'})
        else:
            return JsonResponse({'status': 'error', 'errors': {k: v[0] for k, v in form.errors.items()}})
    return render(request, 'register.html', {'form': form})


@login_required
def profile_edit(request, profile_id):
    instance = get_object_or_404(Profile, pk=profile_id)
    form = ProfileForm(instance=instance)
    if request.POST:
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile Saved successfully'})
        else:
            return JsonResponse({'status': 'error', 'errors': {k: v[0] for k, v in form.errors.items()}})
    return render(request, 'profile-form.html', {'form': form, 'instance': instance})
