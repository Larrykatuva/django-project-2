from django.shortcuts import render
import os
import json
from django.conf import settings
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def index(request):
    exists = models.UserPreference.objects.filter(user=request.user).exists()
    user_preference = None
    if exists:
        user_preference = models.UserPreference.objects.get(user=request.user)

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    data = {'currencies': currency_data, 'user_preferences': user_preference}

    if request.method == 'GET':

        return render(request, "preferences/index.html", data)
    else:
        currency = request.POST['currency']
        if exists:
            user_preference.currency = currency
            user_preference.save()
            messages.success(request, 'Changes updated')
        else:
            models.UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, 'Changes saved')
        return render(request, "preferences/index.html", data)

