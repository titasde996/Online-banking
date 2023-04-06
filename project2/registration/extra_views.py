from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.http import Http404,HttpResponse
from .forms import *
from .forms import MyForm
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from captcha.helpers import captcha_image_url
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_to_phone
import random
from twilio.rest import Client

# create views here
def base_view(request):
    return render(request,'base.html',{})
def base2_view(request):
    return render(request,'base2.html',{})

def contact_view(request):
    return render(request,'contact.html',{})
def about_view(request):
    return render(request,'about.html',{})
