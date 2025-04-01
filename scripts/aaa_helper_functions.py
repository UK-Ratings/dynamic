#!/usr/bin/env python3

import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd

from base.models import *
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import get_language
from dotenv import load_dotenv
from math import sqrt

from base.models import *
from users.models import *

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

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

def get_polygon_side_lengths(polygon_str, multiplier):
    """
    Calculate the side lengths of a polygon in feet from its coordinates.
    
    Args:
        polygon_str (str): A string representation of the polygon, e.g.,
                           "POLYGON 3 ((55.924326171875 57.80728515625, 67.924326171875 57.80728515625, ...))"
        multiplier (float): A multiplier to convert the lengths to feet.
    
    Returns:
        list: A list of side lengths in feet, rounded to the nearest integer.
    """
    # Extract the coordinates from the polygon string
    coordinates_str = polygon_str.split("((")[1].split("))")[0]
    coordinates = [
        tuple(map(float, coord.split()))
        for coord in coordinates_str.split(", ")
    ]

    # Calculate the side lengths
    side_lengths = []
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        length = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        side_lengths.append(round(length * multiplier))
    max_length = max(side_lengths)
    min_length = min(side_lengths)

    return max_length, min_length, side_lengths
def get_nearest_position_to_origin(polygon_str, multiplier):
    """
    Find the nearest position to (0, 0) from the given polygon.

    Args:
        polygon_str (str): A string representation of the polygon, e.g.,
                           "POLYGON 3 ((55.924326171875 57.80728515625, 67.924326171875 57.80728515625, ...))"

    Returns:
        tuple: The nearest position (x, y) to (0, 0).
    """
    # Extract the coordinates from the polygon string
    coordinates_str = polygon_str.split("((")[1].split("))")[0]
    coordinates = [
        tuple(map(float, coord.split()))
        for coord in coordinates_str.split(", ")
    ]

    # Find the nearest position to (0, 0)
    nearest_position = min(coordinates, key=lambda coord: sqrt(coord[0]**2 + coord[1]**2))
    xpos = round(multiplier*nearest_position[0])
    ypos = round(multiplier*nearest_position[1])
    return xpos, ypos


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
        if os.environ.get("RX_STATIC_FLOORPLAN_LOCATION") is not None:
                static_floorplan_loc = str(os.environ.get("RX_STATIC_FLOORPLAN_LOCATION"))
        else:
                static_floorplan_loc = None
        if os.environ.get("RX_STATIC_ANALYSIS_LOCATION") is not None:
                static_analysis_loc = str(os.environ.get("RX_STATIC_ANALYSIS_LOCATION"))
        else:
                static_analysis_loc = None
        return image_length, image_height, image_margin, header_space, footer_space, \
                                image_multiplier, static_floorplan_loc, static_analysis_loc
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


#--gbr-red : #e31f26;
#--gbr-dark-red : #aa1b1f;
#--gbr-light-red : #F7ADAD;
#--gbr-cor-red : #C10016;

#--gbr-green : #198754;
#--gbr-light-green: #A1FB8E;

#--gbr-middle-gray : #939393;
#--gbr-cor-middle-gray : #808080;
#--gbr-dark-gray : #212121;
#--gbr-site-background : #ebebeb;
#--gbr-light-gray : #f0f0f0;

#--bs-blue : #0d6efd;
#--bs-indigo : #6610f2;
#--bs-purple : #6f42c1;
#--bs-pink : #d63384;
#--bs-red : #dc3545;
#--bs-orange : #fd7e14;
#--bs-yellow : #ffc107;
#--bs-green : #198754;
#--bs-teal : #20c997;
#--bs-cyan : #0dcaf0;


def get_color(color_type):
        #blue for unsold
        if(color_type =='unsold stand outline color'):
                return '#002F6C'
        if(color_type =='unsold stand fill color'):
                return '#41B6E6'
        if(color_type =='unsold stand text color'):
                return '#282761'
        if(color_type =='sold stand outline color'):
                return '#6610f2'
        if(color_type =='sold stand fill color'):
                return '#8745f2'
        if(color_type =='sold stand text color'):
                return '#ffffff'

        if(color_type =='price increase stand outline color'):
                return '#198754'
        if(color_type =='price increase stand fill color'):
                return '#A1FB8E'
        if(color_type =='price increase stand text color'):
                return '#000000'

        if(color_type =='price decrease stand outline color'):
                return '#aa1b1f'
        if(color_type =='price decrease stand fill color'):
                return '#e31f26'
        if(color_type =='price decrease stand text color'):
                return '#ffffff'

        if(color_type =='sold stand circle outline color'):
                return '#aa1b1f'
        if(color_type =='sold stand circle fill color'):
                return 'none'
        if(color_type =='sold stand circle text color'):
                return '#ffffff'

        if(color_type =='main aisle'):
                return '#808080'
#default to black
        return '#000000'


def get_gradient_color(value):
    """
    Returns a gradient color between red (#FF0000) and green (#00FF00) based on a value between 0 and 100.

    Args:
        value (int): A number between 0 and 100.

    Returns:
        str: A hexadecimal color string in the format #RRGGBB.
    """
    if value < 0 or value > 100:
        raise ValueError("Value must be between 0 and 100")

    red = int(255 * (100 - value) / 100)
    green = int(255 * value / 100)
    blue = 0  # No blue component in the gradient
    return f"#{red:02X}{green:02X}{blue:02X}"


def print_ax_size(fig, gs, ax, from_def):
        print(f"{from_def}... ")
        print(f"   fig: length {fig.get_size_inches()[0]} inches, height {fig.get_size_inches()[1]} inches")
        print(f"   girdspec: columns {gs.ncols}, rows {gs.nrows}")
        if(ax is not None):
                bbox = ax.get_position()
                width = bbox.width * fig.get_size_inches()[0]
                height = bbox.height * fig.get_size_inches()[1]
                print(f"   ax: width {bbox.width}, height {bbox.height}")
                print(f"   ax: width {width} inches, height {height} inches")
        else:
                print(f"   ax: None")
def calculate_max_font_size(fig, sq, text, available_width, available_height, fl_div, max_font_size):
    """
    Calculate the maximum font size so that the text fits within the available width and height.
    """
    renderer = fig.canvas.get_renderer()
#    print(f"available_width: {available_width}, available_height: {available_height}, max_font_size: {max_font_size}")

    for font_size in range(max_font_size, 0, -1):  # Start from max_font_size and decrease
        text_obj = sq.text(500, 500, text, fontsize=font_size, ha='center', va='center', visible=True)
        bbox = text_obj.get_window_extent(renderer=renderer)
        text_width = bbox.width
        text_height = bbox.height
        text_obj.remove()  # Remove the temporary text object
#        print(f"text_obj: {text_obj} font_size: {font_size}, text_width: {text_width}, text_height: {text_height}, available_width: {available_width}, available_height: {available_height}")
        if text_width <= available_width and text_height <= available_height:
            return font_size, text_width, text_height  # Return the font size that fits
    return 1, 1, 1  # Return a minimum font size if no size fits


def new_place_circle(sq, x, y, xlen, ylen, fill_color, edge_color, fl_div, line_width):
    radius = (xlen) * fl_div  # Adjust as needed for your use case
    xcir = x + xlen/2
    if(ylen > 0):
            ycir = y + xlen/2
    else:
            ycir = y - xlen/2
    # Create the circle
    circle = patches.Circle(((xcir) * fl_div, (ycir) * fl_div), radius, linewidth=line_width, edgecolor=edge_color, facecolor=fill_color)
    sq.add_patch(circle)

    return sq

def new_place_rectangle(fig, sq, x, y, xlen, ylen, image_multiplier, fill_color, edge_color, sq_text, sq_text_color, fl_div, line_width, max_text_size):
        rect = patches.Rectangle((x*fl_div, y*fl_div), xlen*fl_div, ylen*fl_div, linewidth=line_width, edgecolor=edge_color, facecolor=fill_color)
        sq.add_patch(rect)
        if sq_text is not None:
                title_str = sq_text[0][0]
                info_set = sq_text[1:]
                top_section = ylen*.4
                bottom_section = ylen*.6
                padding = 1  # Add some padding around the text

                available_width = abs(xlen - (xlen*.25)) * fl_div #int(abs((xlen * fl_div) - ((xlen/5) * (padding*fl_div))))
                available_height = abs(top_section - (top_section * .25)) * fl_div
                title_font_size, text_width, text_height = calculate_max_font_size(fig, sq, title_str, available_width, available_height, fl_div, max_text_size)
                top_line = sq_text[0]
                if(top_line[1] == 'center'):
                        xxpos = x * fl_div + xlen * fl_div / 2  # Center horizontally
                else:
                        xxpos = (x+1)*fl_div
                if(ylen > 0):
                        yypos = ((y * fl_div) + (ylen * fl_div) - (padding*fl_div))  # Position at the top with padding
                else:
                        yypos = ((y * fl_div) - (padding*fl_div))  # Position at the top with padding
                sq.text(
                        xxpos,  
                        yypos,
                        top_line[0],
                        color=sq_text_color,
                        ha=top_line[1],
                        va=top_line[2],
                        fontsize=int(title_font_size)
                        )
                if(len(info_set) > 0):
#                if(1==0):
                        available_height = abs(bottom_section - (bottom_section * .25)) * fl_div
                        line_height = abs((available_height)) / len(info_set)
                        bottom_font_size = max_text_size
                        bottom_text_height = 100000
                        for qq in info_set:
                                bfs, text_width, text_height = calculate_max_font_size(fig, sq, qq[0], available_width, line_height, fl_div, bottom_font_size)
                                if(bfs <= bottom_font_size):
                                        bottom_font_size = bfs
                                        bottom_text_height = text_height + text_height*.15
                        if(qq[1] == 'center'):
                                xxpos = x * fl_div + xlen * fl_div / 2  # Center horizontally
                        else:
                                xxpos = (x+1)*fl_div
                        if(ylen > 0):
                                ypos = ((y)*fl_div) + bottom_text_height 
                        else:
                                ypos = ((y+ylen)*fl_div) + bottom_text_height
                        for qq in reversed(info_set):
                                sq.text(
                                        xxpos,  # Center horizontally
                                        ypos,
                                        qq[0],
                                        color=sq_text_color,
                                        ha=qq[1],
                                        va=qq[2],
                                        fontsize=int(bottom_font_size))

                                ypos += (bottom_text_height)  # Adjust vertical position for the next line#
        return sq
def create_outer_square(fig, gs, plt_length, plt_height, image_multiplier):
        ax = fig.add_subplot(gs[:, :])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_outer_square")
        # Set the limits of the plot
        ax.set_xlim(0, plt_length*image_multiplier)
        ax.set_ylim(0, plt_height*image_multiplier)
#        ax.set_aspect('equal')
        ax.axis('off')
        # Add a rectangle around the entire plot
        test_text = None
        ax = new_place_rectangle(fig, ax, 0, 0, plt_length*image_multiplier, plt_height*image_multiplier, image_multiplier, '#ffffff', '#ffffff', None, '#000000', 1, 3, 100)
        return(fig)

def create_analysis1_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, analysis_sections, analysis_section_height, analysis_set):
        ax_upper_x = (image_length - (int(((image_length)/4)))) * image_multiplier
        ax_upper_y = (((image_margin*2) + header_space) * image_multiplier)
        ax_height = int(((image_height - (image_margin*2) - header_space - footer_space) / analysis_sections) * analysis_section_height) * image_multiplier
        ax_width = int(((image_length)-(image_margin*2))/4) * image_multiplier
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_analysis1_subplot")

#        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000', 1, 2, 100)
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(1*image_multiplier)))  # Adjust vertical position
        ft_size = 18
        for x in analysis_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                top_pos_y = top_pos_y - (6*image_multiplier)  # Adjust spacing between lines
        return(fig)
def create_analysis2_subplot(fig, gs, image_margin, header_space, footer_space, image_length, 
                             image_height, image_multiplier, analysis_sections, analysis_section_start, analysis_section_height, analysis_set):
        ax_upper_x = (image_length - (int(((image_length)/4)))) * image_multiplier
        ax_upper_y = ax_height = int(((image_height - (image_margin*2) - header_space - footer_space) / analysis_sections) * analysis_section_start) * image_multiplier
        ax_height = int(((image_height - (image_margin*2) - header_space - footer_space) / analysis_sections)*analysis_section_height) * image_multiplier
        ax_width = int(((image_length)-(image_margin*2))/4) * image_multiplier
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_analysis2_subplot")

#        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000', 1, 2, 100)
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(1*image_multiplier)))  # Adjust vertical position
        ft_size = 18
        for x in analysis_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                top_pos_y = top_pos_y - (4*image_multiplier)  # Adjust spacing between lines
        return(fig)
def create_analysis3_subplot(fig, gs, image_margin, header_space, footer_space, image_length, 
                             image_height, image_multiplier, analysis_sections, analysis_section_start, analysis_section_height, analysis_set):
        ax_upper_x = (image_length - (int(((image_length)/4)))) * image_multiplier
        ax_upper_y = ax_height = int(((image_height - (image_margin*2) - header_space - footer_space) / analysis_sections) * analysis_section_start) * image_multiplier
        ax_height = int(((image_height - (image_margin*2) - header_space - footer_space) / analysis_sections)*analysis_section_height) * image_multiplier
        ax_width = int(((image_length)-(image_margin*2))/4) * image_multiplier
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_analysis3_subplot")

#        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000', 1, 2, 100)
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(1*image_multiplier)))  # Adjust vertical position
        ft_size = 18
        for x in analysis_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                top_pos_y = top_pos_y - (4*image_multiplier)  # Adjust spacing between lines
        return(fig)


def zzzfloorplan_new_place_isles(fig, ax, image_multiplier, fl_div):
        isle_color = get_color('main aisle')
        ax = new_place_rectangle(fig, ax, 10, 310, 1030, -10, image_multiplier, isle_color, isle_color, None, 'black', fl_div, 0, 50)
        ax = new_place_rectangle(fig, ax, 10, 260, 400, -10, image_multiplier, isle_color, isle_color, None, 'black', fl_div, 0, 50)
        return ax
def floorplan_new_place_stands(fig, ax, image_multiplier, fl_div):
        for x in stand_location.objects.filter(sl_stand__s_rx_event__re_name__iexact='ISC West 2025'):
                #Available, Sold, New Sell, Reserved, New Stand
                if(x.sl_stand.s_stand_status == 'Available'):
                        stand_fill_color = get_color('unsold stand fill color')
                        stand_outline_color = get_color('unsold stand outline color')
                        text_color = get_color('unsold stand text color')
                if(x.sl_stand.s_stand_status == 'Sold'):
                        stand_fill_color = get_color('sold stand fill color')
                        stand_outline_color = get_color('sold stand outline color')
                        text_color = get_color('sold stand text color')
                if(x.sl_stand.s_stand_status == 'New Sell'):
                        stand_fill_color = get_color('sold stand fill color')
                        stand_outline_color = get_color('sold stand outline color')
                        text_color = get_color('sold stand text color')
                        circle_fill_color = get_color('sold stand circle fill color')
                        circle_outline_color = get_color('sold stand circle outline color')
                        text_color = get_color('sold stand circle text color')
                        ax = new_place_circle(ax, x.sl_x, x.sl_y, x.sl_x_length, x.sl_y_length, circle_fill_color, circle_outline_color, fl_div, 40)

                #Base, Price Increase, Price Decrease 
                if(x.sl_stand.s_stand_price == 'Price Increase'):
                        stand_fill_color = get_color('price increase stand fill color')
                        stand_outline_color = get_color('price increase stand outline color')
                        text_color = get_color('price increase stand text color')
                if(x.sl_stand.s_stand_price == 'Price Decrease'):
                        stand_fill_color = get_color('price decrease stand fill color')
                        stand_outline_color = get_color('price decrease stand outline color')
                        text_color = get_color('price decrease stand text color')

                if(x.sl_x_length * x.sl_y_length > 1):
                        new_stand = []
                        if(x.sl_stand.s_name is not None and len(x.sl_stand.s_name) > 0):
                                new_stand.append([str(x.sl_stand.s_name), 'center', 'top'])
                        else:
                                new_stand.append(['No Name Given', 'center', 'top'])
                        new_stand.append(['Price: $20000', 'left', 'top'])
                        new_stand.append(['Target: $30000', 'left', 'top'])

                        ax = new_place_rectangle(fig, ax, x.sl_x, x.sl_y, x.sl_x_length, x.sl_y_length, image_multiplier, stand_fill_color, stand_outline_color, new_stand, text_color, fl_div, 1, 50)
        return ax

def new_place_header(fig, gs, image_margin, header_space, image_length, image_height, image_multiplier, header_set, footer_space):
        ax_height = int(header_space * image_multiplier) 
        ax_width = int((image_length-(image_margin*2)) * image_multiplier)
        ax_upper_x = image_margin * image_multiplier
        ax_upper_y = (image_margin) * image_multiplier

        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_floorplan_subplot")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', header_set, '#000000', 1, 3, 300)
        return(fig)
def new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set):
        ax_height = int(footer_space * image_multiplier) 
        ax_width = int((image_length-(image_margin*2)) * image_multiplier)
        ax_upper_x = image_margin * image_multiplier
        ax_upper_y = (image_height - image_margin-footer_space) * image_multiplier

        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_floorplan_subplot")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', footer_set, '#000000', 1, 3, 300)
        return(fig)

def floorplan_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floorplan_length, floorplan_height):
        potential_plot_height = (image_height - (image_margin*2) - header_space - footer_space) * image_multiplier
        potential_plot_length = (image_length - (image_margin*2)) * image_multiplier
        height_div = (potential_plot_height / floorplan_height)
        length_div = (potential_plot_length / floorplan_length)
        fl_div = min(height_div, length_div)

        ax_height = int(floorplan_height * fl_div)
        ax_width = int(floorplan_length * fl_div)
        ax_upper_x = int(((image_length*image_multiplier) - ax_width) / 2)
        ax_upper_y = int((image_margin + header_space) * image_multiplier)


        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_floorplan_subplot")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#000000', None, '#000000', 1, 3, 100)

        ax = floorplan_new_place_stands(fig, ax, image_multiplier, fl_div)
        return(fig)


def render_floorplan(rxe, header_set, footer_set, message_set):
        record_log_data("aaa_helper_functions.py", "run_event_year", "starting: event name: " + str(rxe.re_name))

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        footer_set.append([cdatetime + '.png', 'left', 'top'])
        floor_length = rxe.re_floor_length
        floor_height = rxe.re_floor_height

        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, static_floorplan_loc, static_analysis_loc = get_env_values()
        plt_length = int((image_length*image_multiplier)/100.0)
        plt_height = int((image_height*image_multiplier)/100.0)


        fig = plt.figure(figsize=(plt_length, plt_height))    #x, y
        gs = gridspec.GridSpec(plt_height*100, plt_length*100, figure = fig)  # rows, columns
#        print_ax_size(fig, gs, None, "render_floorplan...")
        gs.update(wspace=0, hspace=0)  # Remove any margin between subplots

        fig = create_outer_square(fig, gs, plt_length, plt_height, image_multiplier) 
        fig = new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set)
        fig = new_place_header(fig, gs, image_margin, header_space, image_length, image_height, image_multiplier, header_set, footer_space)
        fig = floorplan_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floor_length, floor_height)


#        fig = create_analysis1_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, analysis_set_1)
#        fig = create_analysis2_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, 1, analysis_set_1)
#        fig = create_analysis3_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 4, 1, analysis_set_1)

        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_floorplan_loc, cdatetime)
        pyplot_filename = pyplot_filename + '.png'

        record_log_data("aaa_helper_functions.py", "run_event_year", "completed: event name: " + str(rxe.re_name))
        return pyplot_filename

