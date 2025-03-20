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



def zzzbase_venue(request):
#    record_page_data("base-view.py", "base_home", request)    
    messages_to_display=[]
    messages_to_display.append(('Made it to venue','warning'))
    record_message(request, "base-view.py", "base_venue", messages_to_display)

    floor_length = 60
    floor_width = 30

# Create a grid using Matplotlib
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], marker='o')
    ax.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'venue.html', {
        'data': uri,
        })



def yyybase_venue(request):
#    record_page_data("base-view.py", "base_home", request)    
    messages_to_display=[]
    messages_to_display.append(('Made it to venue','success'))
    record_message(request, "base-view.py", "base_venue", messages_to_display)

    floor_length = 6
    floor_height = 3

    # Create a grid using Matplotlib with a white background and outlined squares
    z = [[1 for _ in range(floor_length)] for _ in range(floor_height)]

    fig, ax = plt.subplots()
    ax.imshow(z, cmap='gray', interpolation='none', vmin=1, vmax=1)

    # Set the overall grid background to white
    fig.patch.set_facecolor('white')

    # Add lines between each row and column to outline each square
    for i in range(floor_height+1):
        ax.axhline(i-0.5, color='black', linewidth=0.1)
    for j in range(floor_length+1):
        ax.axvline(j-0.5, color='black', linewidth=0.1)

    # Remove x and y axis descriptions
    ax.set_xticks([])
    ax.set_yticks([])

    pyplot_file = ""
    erase_files_in_dir('images')

    for i in range(10):
        pyplot_file = write_pyplot_to_file(plt, 'images')

    create_mov_from_images('images', 'output.mp4')

    return render(request, 'venue.html', {
        'pyplot_file': pyplot_file,
        })


def base_venue(request):
#    record_page_data("base-view.py", "base_home", request)    
    messages_to_display=[]
    messages_to_display.append(('Made it to venue','success'))
    record_message(request, "base-view.py", "base_venue", messages_to_display)

    floor_length = 60
    floor_height = 30

    # Create a grid using Matplotlib with a white background and outlined squares
    z = [[1 for _ in range(floor_length)] for _ in range(floor_height)]

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], marker='o')
    ax.grid(True)


#    fig, ax = plt.subplots()
#    ax.imshow(z, cmap='gray', interpolation='none', vmin=1, vmax=1)
#    fig.patch.set_facecolor('red')

#    # Add lines between each row and column to outline each square
#    for i in range(floor_height+1):
#        ax.axhline(i-0.5, color='blue', linewidth=1)
#    for j in range(floor_length+1):
#        ax.axvline(j-0.5, color='green', linewidth=1)


    # Remove x and y axis descriptions
    ax.set_xticks([])
    ax.set_yticks([])

    pyplot_file = ""
    erase_files_in_dir('images')
    pyplot_filename, pyplot_path = write_pyplot_to_file(plt, 'images')
    print("pyplot_path: ", pyplot_path)

#    create_mov_from_images('images', 'output.mp4')

    return render(request, 'venue.html', {
        'pyplot_path': pyplot_path,
        })


