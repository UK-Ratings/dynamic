from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from decouple import config
from datetime import datetime, timedelta
import time
import os
from django.db.models import Count, Q, F
from django.http import HttpResponse
from django.conf import settings
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64
import urllib
import cv2

from base.models import *
from users.models import *

from scripts.aaa_helper_functions import * 
from scripts.aaa_reset_and_load import *


def base_home(request):
#    record_page_data("base-view.py", "base_home", request)    
    base_msg = str("Starting base_home")
    if "169.254" not in str(request.META['REMOTE_ADDR']):
        base_msg = base_msg + " REMOTE_ADDR: " + str(request.META['REMOTE_ADDR'])
#            + " HTTP_ACCEPT_LANGUAGE: " + str(request.META['HTTP_ACCEPT_LANGUAGE'])
#            + " HTTP_USER_AGENT: " + str(request.META['HTTP_USER_AGENT']))
#    record_log_data("base-view.py", "base_home", base_msg)
    messages_to_display=[]

    db_settings = settings.DATABASES['default']
    db_server = db_settings['HOST']
    db_name = db_settings['NAME']
    path = "manage.py"
    manage_date = time.ctime(os.path.getmtime(path))
    manage_create_date = "Build: " + str(manage_date) + " DB: " + str(db_server) + " " + str(db_name)


#    if request.user.is_authenticated:
#        return redirect('base-home-gbf')


#    record_message(request, "base-view.py", "base_home", messages_to_display)
    return render(request, 'home.html', {
        'manage_create_date':manage_create_date,
        })




def base_venue(request):
#    record_page_data("base-view.py", "base_home", request)    
    messages_to_display=[]
    messages_to_display.append(('Made it to venue','success'))
    record_message(request, "base-view.py", "base_venue", messages_to_display)

    reset_test_data()
    populate_for_test()

    pyplot_filename = render_floorplan()
    return render(request, 'venue.html', {
        'pyplot_filename': pyplot_filename,
        })


