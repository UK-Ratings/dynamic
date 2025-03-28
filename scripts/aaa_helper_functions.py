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

from base.models import *
from users.models import *

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

from scripts import aaa_reset_and_load


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
    print("dumps_dir: ", dumps_dir)
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
def figure_small_font_size(first_line_font_size):
        if(first_line_font_size > 0):
                sm_font = 5
                line_height = 10
        if(first_line_font_size > 10):
                sm_font = 6
                line_height = 14
        if(first_line_font_size > 30):
                sm_font = 18
                line_height = 40
        if(first_line_font_size > 50):
                sm_font = 24
                line_height = 60
        if(first_line_font_size > 75):
                sm_font = 40
                line_height = 85
        return sm_font, line_height
def new_place_rectangle(sq, x, y, xlen, ylen, image_multiplier, fill_color, edge_color, sq_text, sq_text_color, fl_div, line_width):
#Note: Could get more sophisticated with the text placement and size.
        rect = patches.Rectangle((x*fl_div, y*fl_div), xlen*fl_div, ylen*fl_div, linewidth=line_width, edgecolor=edge_color, facecolor=fill_color)
        sq.add_patch(rect)
        if sq_text is not None:
                if(ylen > 0):
                        # Calculate available space for text
                        padding = 2 * fl_div  # Add some padding around the text
                        available_width = abs((xlen * fl_div) - (2 * padding))
                        available_height = abs((ylen * fl_div) - (2 * padding))
                        # Center the first line and make it larger
                        max_font_size = 100  # Set an upper limit for font size
                        first_line_font_size = min(available_width / len(sq_text[0]), available_height / 2)
                        first_line_font_size = min(first_line_font_size, max_font_size)
                        # Add the first line of text (centered and larger)
                        sq.text(
                        x * fl_div + xlen * fl_div / 2,  # Center horizontally
                        y * fl_div + ylen * fl_div - padding,  # Position at the top with padding
                        sq_text[0],
                        color=sq_text_color,
                        ha='center',
                        va='top',
                        fontsize=int(first_line_font_size)
                        )

                        if(len(sq_text) > 1):   
                                sm_font, line_height = figure_small_font_size(first_line_font_size)
                                ypos = ((y+ylen)*fl_div) - int((available_height*.4))
                                for line in sq_text[1:]:
                                        sq.text(
                                                (x+1)*fl_div,  # Center horizontally
                                                ypos,
                                                line,
                                                color=sq_text_color,
                                                ha='left',
                                                va='top',
                                                fontsize=int(sm_font)
                                        )
                                        ypos -= (line_height)  # Adjust vertical position for the next line#

                else:
                        # Calculate available space for text
                        padding = 2 * fl_div  # Add some padding around the text
                        available_width = abs((xlen * fl_div) - (2 * padding))
                        available_height = abs((ylen * fl_div) - (2 * padding))
                        # Center the first line and make it larger
                        max_font_size = 100  # Set an upper limit for font size
                        first_line_font_size = min(available_width / len(sq_text[0]), available_height / 2)
                        first_line_font_size = min(first_line_font_size, max_font_size)
                        # Add the first line of text (centered and larger)
                        sq.text(
                        x * fl_div + xlen * fl_div / 2,  # Center horizontally
                        y * fl_div - padding,  # Position at the top with padding
                        sq_text[0],
                        color=sq_text_color,
                        ha='center',
                        va='top',
                        fontsize=int(first_line_font_size)
                        )
                        if(len(sq_text) > 1):   
                                sm_font, line_height = figure_small_font_size(first_line_font_size)
                                ypos = (y*fl_div) - int((available_height*.4))
                                for line in sq_text[1:]:
                                        sq.text(
                                                (x+1)*fl_div,  # Center horizontally
                                                ypos,
                                                line,
                                                color=sq_text_color,
                                                ha='left',
                                                va='top',
                                                fontsize=int(sm_font)
                                        )
                                        ypos -= (line_height)  # Adjust vertical position for the next line
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
        ax = new_place_rectangle(ax, 0, 0, plt_length*image_multiplier, plt_height*image_multiplier, image_multiplier, '#ffffff', '#ffffff', None, '#000000', 1, 3)
        return(fig)
def new_place_header(fig, gs, image_margin, header_space, image_length, image_multiplier, header_set):
        ax_upper_x = image_margin * image_multiplier
        ax_upper_y = ax_upper_x
        ax_height = (image_margin+header_space) * image_multiplier
        ax_width = (image_length-(image_margin*2)) * image_multiplier
        ax = fig.add_subplot(gs[ax_upper_y:ax_height, ax_upper_x:ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "new_place_header")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', None, '#000000', 1, 2)
        top_pos_x = (ax_width / 2)  # Center horizontally
        top_pos_y = ((ax_height-(4*image_multiplier)))  # Adjust vertical position
        ft_size = 192
        for x in header_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='center', va='center', fontsize=ft_size)
                ft_size = 128
                top_pos_y = top_pos_y - (7 * image_multiplier)  # Adjust spacing between lines
        return(fig)
def new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set):
        ax_upper_x = image_margin * image_multiplier
        ax_upper_y = (image_height-image_margin-footer_space) * image_multiplier
        ax_height = (image_height-image_margin) * image_multiplier
        ax_width = (image_length-(image_margin*2)) * image_multiplier

        ax = fig.add_subplot(gs[ax_upper_y:ax_height, ax_upper_x:ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "new_place_footer")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', None, '#000000', 1, 2)
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(10*image_multiplier)))  # Adjust vertical position
        ft_size = 96
        for x in footer_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                ft_size = 72
                top_pos_y = top_pos_y - (60*image_multiplier)  # Adjust spacing between lines
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
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000', 1, 2)
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
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000', 1, 2)
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
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000', 1, 2)
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(1*image_multiplier)))  # Adjust vertical position
        ft_size = 18
        for x in analysis_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                top_pos_y = top_pos_y - (4*image_multiplier)  # Adjust spacing between lines
        return(fig)


def floorplan_new_place_isles(ax, image_multiplier, fl_div):
        isle_color = '#D8D8D8'
        ax = new_place_rectangle(ax, 10, 310, 1030, -10, image_multiplier, isle_color, isle_color, None, 'black', fl_div, 0)
        ax = new_place_rectangle(ax, 10, 260, 400, -10, image_multiplier, isle_color, isle_color, None, 'black', fl_div, 0)
        return ax
def floorplan_new_place_stands(ax, image_multiplier, fl_div):
        for x in stand_location.objects.filter(sl_stand__s_rx_event__re_name__iexact='ISC West 2025'):
                ax = new_place_rectangle(ax, x.sl_x, x.sl_y, x.sl_x_length, x.sl_y_length, image_multiplier, x.sl_stand.s_stand_fill_color, x.sl_stand.s_stand_outline_color, [x.sl_stand.s_name,'Price:$14000', 'Target:$20000'], x.sl_stand.s_text_color, fl_div, 1)
        return ax




def floorplan_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floorplan_length, floorplan_height):
        potential_plot_height = (image_height - (image_margin*2) - header_space - footer_space) * image_multiplier
        potential_plot_length = (image_length - (image_margin*2)) * image_multiplier
        height_div = (potential_plot_height / floorplan_height)
        length_div = (potential_plot_length / floorplan_length)
        fl_div = min(height_div, length_div)
#        print(f"floorplan_length: {floorplan_length}, floorplan_height: {floorplan_height}")
#        print(f"potential_plot_length: {potential_plot_length}, potential_plot_height: {potential_plot_height}")
#        print(f"height_div: {height_div}, length_div: {length_div}")
#        print(f"fl_div: {fl_div}")

        ax_height = int(floorplan_height * fl_div)
        ax_width = int(floorplan_length * fl_div)
        ax_upper_x = int(((image_length*image_multiplier) - ax_width) / 2)
        ax_upper_y = int(((image_height*image_multiplier) - ax_height) / 2)
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_floorplan_subplot")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#000000', None, '#000000', 1, 3)

        ax = floorplan_new_place_isles(ax, image_multiplier, fl_div)
        ax = floorplan_new_place_stands(ax, image_multiplier, fl_div)
        return(fig)


def render_floorplan(rxe, header_set, footer_set, message_set):
        record_log_data("aaa_helper_functions.py", "run_event_year", "starting: event name: " + str(rxe.re_name))

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        footer_set.append(cdatetime + '.png')
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
        fig = new_place_header(fig, gs, image_margin, header_space, image_length, image_multiplier, header_set)
        fig = new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set)
        fig = floorplan_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floor_length, floor_height)
#        fig = create_analysis1_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, analysis_set_1)
#        fig = create_analysis2_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, 1, analysis_set_1)
#        fig = create_analysis3_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 4, 1, analysis_set_1)

        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_floorplan_loc, cdatetime)
        pyplot_filename = pyplot_filename + '.png'

        record_log_data("aaa_helper_functions.py", "run_event_year", "completed: event name: " + str(rxe.re_name))
        return pyplot_filename



def run_event_year():
        record_log_data("aaa_helper_functions.py", "run_event_year", "starting...")

        aaa_reset_and_load.run()

        rxe = rx_event.objects.get(re_name='ISC West 2025')
        print(rxe.re_name, rxe)
        print(event_sales_transactions.objects.filter(est_event=rxe).order_by('est_Order_Created_Date').count())
#when running entire, this will need to go into calling function.
        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, static_floorplan_loc, static_analysis_loc = get_env_values()
        erase_files_in_dir(static_floorplan_loc)

#def create_stand(eve, stand_name, stand_number, x, y, x_length, y_length):##

#        st, created = stands.objects.update_or_create(s_id=get_next_stand_id(), defaults={
#                's_rx_event': eve[0], 's_name': stand_name, 's_number': stand_number,
#                's_stand_fill_color':'#99B3CF', 's_stand_outline_color':'black', 's_text_color':'#000000'})
#        sl = stand_location.objects.update_or_create(sl_stand=st, defaults={
#                                'sl_x':x, 'sl_y':y, 'sl_x_length':x_length, 'sl_y_length':y_length})

        for x in event_sales_transactions.objects.filter(est_event=rxe).order_by('est_Order_Created_Date'):
                found_stand = False
                for fs in stands.objects.filter(s_rx_event=rxe, s_number=x.est_Stand_Name_Cleaned):
                        print(x.est_Order_Created_Date,fs.s_number, fs.s_name, fs.s_rx_event.re_name)
                        fs.s_stand_fill_color = '#e31f26'
                        fs.s_stand_outline_color = '#aa1b1f'
                        fs.save()
                        found_stand = True
                if found_stand == True:        
                        header_set = []
                        footer_set = []
                        message_set = []
                        header_set.append("ISC West 2025")
                        header_set.append("Las Vegas, NV")
                        header_set.append(str(x.est_Order_Created_Date))

                #eventually add to render call
                        footer_set.append("ISC West 2025")
                        footer_set.append("Las Vegas, NV")
                        footer_set.append("Blah, Blah, Blah")
                        render_floorplan(rxe, header_set, footer_set, message_set)

#    create_mov_from_images('images', 'output.mp4')
        record_log_data("aaa_helper_functions.py", "run_event_year", "completed...")


