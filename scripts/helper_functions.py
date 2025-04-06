#!/usr/bin/env python3

import cv2
import os

from base.models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import get_language
from dotenv import load_dotenv
from base.models import *
from users.models import *



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

def get_env_values():
        if os.environ.get("RX_IMAGE_LENGTH") is not None:
                image_length = int(os.environ.get("RX_IMAGE_LENGTH"))
        else:
                image_length = None
        if os.environ.get("RX_IMAGE_HEIGHT") is not None:
                image_height = int(os.environ.get("RX_IMAGE_HEIGHT"))
        else:
                image_height = None
        if os.environ.get("RX_IMAGE_MARGIN") is not None:
                image_margin = int(os.environ.get("RX_IMAGE_MARGIN"))
        else:
                image_margin = None
        if os.environ.get("RX_FLOORPLAN_HEADER_SPACE") is not None:
                header_space = int(os.environ.get("RX_FLOORPLAN_HEADER_SPACE"))
        else:
                header_space = None
        if os.environ.get("RX_FLOORPLAN_FOOTER_SPACE") is not None:
                footer_space = int(os.environ.get("RX_FLOORPLAN_FOOTER_SPACE"))
        else:
                footer_space = None
        if os.environ.get("RX_FLOORPLAN_IMAGE_MULTIPLIER") is not None:
                image_multiplier = int(os.environ.get("RX_FLOORPLAN_IMAGE_MULTIPLIER"))
        else:
                image_multiplier = None
        if os.environ.get("RX_FLOORPLAN_IMAGE_MULTIPLIER_SMALL") is not None:
                image_multiplier_small = int(os.environ.get("RX_FLOORPLAN_IMAGE_MULTIPLIER_SMALL"))
        else:
                image_multiplier_small = None
        if os.environ.get("RX_STATIC_FLOORPLAN_LOCATION") is not None:
                static_floorplan_loc = str(os.environ.get("RX_STATIC_FLOORPLAN_LOCATION"))
        else:
                static_floorplan_loc = None
        if os.environ.get("RX_STATIC_ANALYSIS_LOCATION") is not None:
                static_analysis_loc = str(os.environ.get("RX_STATIC_ANALYSIS_LOCATION"))
        else:
                static_analysis_loc = None
        return image_length, image_height, image_margin, header_space, footer_space, \
                                image_multiplier, image_multiplier_small, static_floorplan_loc, static_analysis_loc
def erase_files_in_dir(media_directory):

    dumps_dir = os.path.join(settings.BASE_DIR, 'static/'+media_directory)
#    print("dumps_dir: ", dumps_dir)
    os.makedirs(dumps_dir, exist_ok=True)
    for file in os.listdir(dumps_dir):
        file_path = os.path.join(dumps_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
def write_pyplot_to_file(plt, media_directory, cdatetime):
    dumps_dir = os.path.join(settings.BASE_DIR, 'static/'+media_directory)
    os.makedirs(dumps_dir, exist_ok=True)
    plot_filename = cdatetime+".png" #'grid_plot.png'
    plot_path = os.path.join(dumps_dir, plot_filename)
#    print("plot_path: ", plot_path)
#    print("plot_filename: ", plot_filename)
    plt.savefig(plot_path, format='png', bbox_inches='tight')
    return cdatetime, plot_path
def create_mov_from_images(media_directory, output_filename):
    max_width = 1920
    max_height = 1080
    total_video_time_in_seconds = 60
    fps = 30
    total_frames = total_video_time_in_seconds * fps

    output_dir = os.path.join(settings.MEDIA_ROOT, 'movies')
    os.makedirs(output_dir, exist_ok=True)
    movie_filename = os.path.join(output_dir, output_filename)

    dumps_dir = os.path.join(settings.BASE_DIR, 'static/' + media_directory)
    images = [img for img in os.listdir(dumps_dir) if img.endswith(".png")]
    images.sort()  # Sort images by filename
    tot_images = len(images)  # Corrected line to count images

    if not images:
        print("No images found in directory.")
        return

    fps_per_image = int(total_frames / tot_images)

    # Read the first image to get the dimensions
    first_image_path = os.path.join(dumps_dir, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Scale the dimensions if they exceed the maximum allowed size
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
    else:
        new_width, new_height = width, height

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MOV file
    video = cv2.VideoWriter(movie_filename, fourcc, fps, (new_width, new_height))

    for image in images:
        image_path = os.path.join(dumps_dir, image)
        frame = cv2.imread(image_path)

        # Resize the frame if necessary
        if width > max_width or height > max_height:
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

        for _ in range(fps_per_image):
            video.write(frame)

    video.release()
    print(f"Video saved as {movie_filename}")

def log_errors_to_file(filename, errors):
#    for qq in errors:
#        print(qq[0], qq[1])
    logs_dir = os.path.join(settings.BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, filename)

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for error in errors:
            log_file.write(f"{error}\n")


def get_event(event_name):
        try:
                rxe = rx_event.objects.get(re_name=event_name)
        except rx_event.DoesNotExist:
                rxe = None
                record_log_data("aaa_run_process.py", "run_event_year", "Event does not exist: " + event_name)
        return rxe


