#!/usr/bin/env python3

import cv2
import os
import matplotlib.pyplot as plt


from django.utils.translation import get_language
from base.models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import get_language

from base.models import *
from users.models import *

from scripts.aaa_helper_functions import *


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def record_page_data(python_app, function_name, request):
        if request.user.is_authenticated:
                cuser = request.user
        else:
                cuser = 'AnonymousUser'
        remote_address = request.META['REMOTE_ADDR']
        user_language = request.META['HTTP_ACCEPT_LANGUAGE']
        user_agent = request.META['HTTP_USER_AGENT']
        user_referer = request.META.get('HTTP_REFERER', '')
        user_language = get_language()
        user_device = request.user_agent.device.family
        user_os = request.user_agent.os.family
        user_browser = request.user_agent.browser.family
        log = log_page_data(
                page_current_datetime = timezone.now(),
                page_python_app = python_app[:100],
                page_function_name = function_name[:500],
                page_user = cuser,
                page_user_ip = remote_address[:100],
                page_user_agent = user_agent[:500],
                page_user_referer = user_referer[:500],
                page_user_language = user_language[:100],
                page_user_device = user_device[:100],
                page_user_os = user_os[:100],
                page_user_browser = user_browser[:100]
                )
        log.save()
def record_log_data(python_app, function_name, function_message):
        log = log_progress_data(
                current_datetime=timezone.now(),
                python_app=python_app,
                function_name=function_name,
                function_message=function_message
        )
        log.save()
def record_message(request, python_app, function_name, fcnt_messages):
        for x in fcnt_messages:
                msg = log_messages(
                        current_datetime=timezone.now(),
                        python_app=python_app,
                        user_name=request.user.username,
                        function_name=function_name,
                        function_message=x[0] + ' ' + x[1]
                )
                msg.save()
                #'silent' will not be displayed
                if x[1] == 'success':
                        messages.success(request, x[0])
                elif x[1] == 'info':
                        messages.info(request, x[0])
                elif x[1] == 'warning':
                        messages.warning(request, x[0])
                elif x[1] == 'error':
                        messages.error(request, x[0])
def record_error_data(python_app, function_name, given_error_level, given_error_message):
        if(given_error_level.lower() in ('info', 'warning', 'error')):
                e_level = given_error_level.title()
                e_message = given_error_message
        else:
                e_level = 'Error'
                e_message = 'Invalid error level: ' + given_error_level
        log = log_error_data(
                current_datetime=timezone.now(),
                python_app=python_app,
                function_name=function_name,
                error_level=e_level,
                error_message=e_message
        )
        log.save()

def erase_files_in_dir(media_directory):

    dumps_dir = os.path.join(settings.BASE_DIR, 'static/'+media_directory)
    print("dumps_dir: ", dumps_dir)
    os.makedirs(dumps_dir, exist_ok=True)
    for file in os.listdir(dumps_dir):
        file_path = os.path.join(dumps_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def write_pyplot_to_file(plt, media_directory):
    cdatetime = str(timezone.now()).replace(" ", "").replace(":", "").replace("+", "")
    dumps_dir = os.path.join(settings.BASE_DIR, 'static/'+media_directory)
    os.makedirs(dumps_dir, exist_ok=True)
    plot_filename = cdatetime+".png" #'grid_plot.png'
    plot_path = os.path.join(dumps_dir, plot_filename)
    print("plot_path: ", plot_path)
    print("plot_filename: ", plot_filename)
    plt.savefig(plot_path, format='png', bbox_inches='tight')
    return cdatetime, plot_path

def create_mov_from_images(media_directory, output_filename):
    output_dir = os.path.join(settings.MEDIA_ROOT, 'movies')
    os.makedirs(output_dir, exist_ok=True)
    movie_filename = os.path.join(output_dir, output_filename)

    dumps_dir = os.path.join(settings.MEDIA_ROOT, media_directory)
    images = [img for img in os.listdir(dumps_dir) if img.endswith(".png")]
    images.sort()  # Sort images by filename

    if not images:
        print("No images found in directory.")
        return

    # Read the first image to get the dimensions
    first_image_path = os.path.join(dumps_dir, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MOV file
    video = cv2.VideoWriter(movie_filename, fourcc, 1, (width, height))

    for image in images:
        image_path = os.path.join(dumps_dir, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()
    print(f"Video saved as {movie_filename}")


def place_square(ax, x, y, xlen, ylen, image_multiplier, fill_color, edge_color, sq_text, sq_text_color):
    rect = plt.Rectangle((x*image_multiplier, y*image_multiplier), xlen*image_multiplier, ylen*image_multiplier, edgecolor=edge_color, facecolor=fill_color, linewidth=1.0)
    ax.add_patch(rect)
    if(sq_text is not None):
        ax.text(x*image_multiplier, (y-1)*image_multiplier, sq_text, color=sq_text_color, ha='left', va='top', fontsize=10)
    return ax

def place_isles(ax, image_multiplier):
        isle_color = 'black'
        place_square(ax, 10, 130, 800, -10, image_multiplier, isle_color, isle_color, "Isle Name", 'white')
        place_square(ax, 10, 80, 800, -10, image_multiplier, isle_color, isle_color, "Isle Name", 'white')
        return ax

def place_stands(ax, image_multiplier):

        for x in stand_location.objects.filter(sl_stand__s_rx_event__re_name__iexact='ISC West 2025'):
                place_square(ax, x.sl_x, x.sl_y, x.sl_x_length, x.sl_y_length, image_multiplier, x.sl_stand.s_stand_fill_color, x.sl_stand.s_stand_outline_color, x.sl_stand.s_name, x.sl_stand.s_text_color)

        return ax


def render_floorplan():

        floor_length = 1060
        floor_height = 600
        image_multiplier = 8.0
        image_length = floor_length * image_multiplier / 100.0
        image_height = floor_height * image_multiplier / 100.0
        #0,0 in lower left corner

        floor_title = "Floor Plan"


        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(image_length, image_height))

        # Set the limits of the plot
        ax.set_xlim(0, floor_length*image_multiplier)
        ax.set_ylim(0, floor_height*image_multiplier)
        ax.set_title(floor_title, fontsize=15, pad=20)
        ax.text(0.5, 1.05, floor_title, transform=ax.transAxes, ha='center', va='center', fontsize=96)

        ax = place_isles(ax, image_multiplier)
        ax = place_stands(ax, image_multiplier)


#        rect = plt.Rectangle((10, 15), 2, 2, edgecolor='black', facecolor='red', linewidth=0.5)
#        ax.add_patch(rect)
#        ax.text(11, 16, 'Text', color='blue', ha='center', va='center', fontsize=3)

#        ax = place_square(ax, 20, 20, 3, 2, image_multiplier, 'red', 'pink', 'new square', 'blue') 

        ax.set_aspect('equal')
        ax.axis('off')


        pyplot_file = ""
        erase_files_in_dir('floorplans')
        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, 'floorplans')
        print("pyplot_path: ", pyplot_path)
        pyplot_filename = pyplot_filename + '.png'

#    create_mov_from_images('images', 'output.mp4')
        return pyplot_filename
