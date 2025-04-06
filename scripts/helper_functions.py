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
from django.db.models.functions import Cast
from django.db.models import FloatField, Count, Sum, IntegerField
import statistics



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




def group_and_calculate_square_foot_prices(rxe):
#'est_Stand_Area','est_Number_of_Corners','est_Stand_Zone','est_Floor_Plan_Sector','est_Packages_Sold'

        event_sales_transactions_grouped.objects.all().delete()
        transactions = event_sales_transactions.objects.filter(est_event=rxe)
#        print(f"First Transactions count: {transactions.count()}")
        transactions = event_sales_transactions.objects.filter(est_event=rxe
                ).exclude(est_Total_Net_Amount=0
                ).exclude(est_Stand_Area=0
                ).exclude(est_Stand_Area__isnull=True
                ).exclude(est_Stand_Area__exact=''
                ).exclude(est_Stand_Area__icontains=','
                ).exclude(est_Stand_Name_Cleaned__icontains=','
                ).exclude(est_Floor_Plan_Sector__icontains=','
                ).exclude(est_Packages_Sold__icontains=',')
#        print(f"After exclusions Transactions count: {transactions.count()}")

        grouped_data = transactions.values(
                'est_Stand_Area',
                'est_Number_of_Corners',
                'est_Stand_Zone',
                'est_Floor_Plan_Sector',
#                'est_Packages_Sold'
                ).annotate(
                count=Count('id'),
                ).order_by(
                'est_Stand_Area',
                'est_Number_of_Corners',
                'est_Stand_Zone',
                'est_Floor_Plan_Sector',
#                'est_Packages_Sold'
                )
#        print(f"Grouped data count: {grouped_data.count()}")
    
        for qq in grouped_data:
               up, created = event_sales_transactions_grouped.objects.update_or_create(
                          estg_Stand_Area=qq['est_Stand_Area'],
                          estg_Number_of_Corners=qq['est_Number_of_Corners'],
                          estg_Stand_Zone=qq['est_Stand_Zone'],
                          estg_Floor_Plan_Sector=qq['est_Floor_Plan_Sector'],
#                          estg_Packages_Sold=qq['est_Packages_Sold'],
                          defaults={
                                   'estg_count': Cast(qq['count'], IntegerField()),
                                   'estg_min': Cast(0, FloatField()),
                                   'estg_max': Cast(0, FloatField()),
                                   'estg_avg': Cast(0, FloatField()),
                                   'estg_median': Cast(0, FloatField())
                                   }
                          )
        estg = event_sales_transactions_grouped.objects.all().count(),
#        print(f"Grouped data count: {estg}")

        for estg in event_sales_transactions_grouped.objects.all():
                min_sq_price = 0
                max_sq_price = 0
                avg_sq_price = 0
                median_sq_price = 0
                est = event_sales_transactions.objects.filter(
                        est_event=rxe,
                        est_Stand_Area=estg.estg_Stand_Area,
                        est_Number_of_Corners=estg.estg_Number_of_Corners,
                        est_Stand_Zone=estg.estg_Stand_Zone,
                        est_Floor_Plan_Sector=estg.estg_Floor_Plan_Sector,
#                        est_Packages_Sold=estg.estg_Packages_Sold
                        ).annotate(                       
                                est_price =  Cast(0, FloatField()),
                                est_sq_price =  Cast(0, FloatField())
#                        sq_price=(Cast(float('est_Total_Net_Amount') / float('est_Stand_Area')), FloatField())
                        ).exclude(est_Total_Net_Amount=0
                        ).exclude(est_Stand_Area=0
                        ).exclude(est_Stand_Area__isnull=True
                        ).exclude(est_Stand_Area__exact=''
                        ).exclude(est_Stand_Name_Cleaned__icontains=',')
                for ee in est:
                        try:
                                tna = float(ee.est_Total_Net_Amount) 
                        except:
                                tna = 0
                        try:
                                float(ee.est_Stand_Area)
                        except:
                                sqp = 0
                        else:
                                sqp = float(ee.est_Total_Net_Amount) / float(ee.est_Stand_Area)
                        ee.est_prices = tna
                        ee.est_sq_prices = sqp
                        ee.save

#                print(f"estg count: {estg.estg_count} est count: {est.count()}")
#                for qqq in est:
#                       print(f"{qqq.est_Total_Net_Amount} {qqq.est_Stand_Area} estg est: {qqq.est_prices} {qqq.est_sq_prices}")
                min_sq_price = min([qqq.est_sq_prices for qqq in est])
                max_sq_price = max([qqq.est_sq_prices for qqq in est])
                avg_sq_price = statistics.mean([qqq.est_sq_prices for qqq in est])
                median_sq_price = statistics.median([qqq.est_sq_prices for qqq in est])
                try:
                       float(min_sq_price)
                except ValueError:
                       min_sq_price = 0.0
                try:
                       float(max_sq_price)
                except ValueError:
                       max_sq_price = 0.0
                try:
                       float(avg_sq_price)
                except  ValueError:
                       avg_sq_price = 0.0
                try:
                       float(median_sq_price)
                except ValueError:
                       median_sq_price = 0.0
                if(str(min_sq_price) == 'nan'):
                       min_sq_price = 0
                if(str(max_sq_price) == 'nan'):
                       max_sq_price = 0
                if(str(avg_sq_price) == 'nan'):
                       avg_sq_price = 0
                if(str(median_sq_price) == 'nan'):
                       median_sq_price = 0
#                print(f"min_sq_price: {min_sq_price} max_sq_price: {max_sq_price} avg_sq_price: {avg_sq_price} median_sq_price: {median_sq_price}")
                estg.estg_min = min_sq_price
                estg.estg_max = max_sq_price
                estg.estg_avg = avg_sq_price
                estg.estg_median = median_sq_price

                estg.save()

#                print(event_sales_transactions_grouped.objects.all().count())
        estg_recs = []
        for tt in event_sales_transactions_grouped.objects.all().order_by('estg_Stand_Zone', 'estg_Floor_Plan_Sector', 'estg_Stand_Area', 'estg_Number_of_Corners',):
#                estg_recs.append([tt.estg_Stand_Area, tt.estg_Number_of_Corners, tt.estg_Stand_Zone, tt.estg_Floor_Plan_Sector,
#                        tt.estg_Packages_Sold, tt.estg_count, tt.estg_min, tt.estg_max, tt.estg_avg, tt.estg_median])
                estg_recs.append([tt.estg_Stand_Area, tt.estg_Number_of_Corners, tt.estg_Stand_Zone, tt.estg_Floor_Plan_Sector,
                        tt.estg_count, tt.estg_min, tt.estg_max, tt.estg_avg, tt.estg_median])
                estg_recs.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
        log_errors_to_file(str(rxe.re_name).replace(' ','_')+'_actual_price_groupings.csv', estg_recs)

#HERE - Don't need packages_sold, just the other 4 fields
#SEEMS TO BE PRICE INCREASES