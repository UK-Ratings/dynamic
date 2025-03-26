#!/usr/bin/env python3

import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

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
        if os.environ.get("RX_STATIC_LOCATION") is not None:
                static_loc = str(os.environ.get("RX_STATIC_LOCATION"))
        else:
                static_loc = None

        return image_length, image_height, image_margin, header_space, footer_space, image_multiplier, static_loc

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

def place_square(ax, x, y, xlen, ylen, image_multiplier, fill_color, edge_color, sq_text, sq_text_color, im_left, im_footer):
    rect = plt.Rectangle(((x+im_left)*image_multiplier, (y+im_footer)*image_multiplier), xlen*image_multiplier, ylen*image_multiplier, edgecolor=edge_color, facecolor=fill_color, linewidth=1.0)
    ax.add_patch(rect)
    if(sq_text is not None):
        if(ylen < 0):
                ax.text((x+im_left)*image_multiplier, (y+im_footer-1)*image_multiplier, sq_text, color=sq_text_color, ha='left', va='top', fontsize=10)
        else:
                ax.text((x+im_left)*image_multiplier, (y+im_footer+ylen-1)*image_multiplier, sq_text, color=sq_text_color, ha='left', va='top', fontsize=10)
    return ax

def new_place_rectangle(sq, x, y, xlen, ylen, image_multiplier, fill_color, edge_color, sq_text, sq_text_color):
        rect = patches.Rectangle((x, y), xlen, ylen, linewidth=2, edgecolor=edge_color, facecolor=fill_color)
        sq.add_patch(rect)
        if sq_text is not None:
                font_size = xlen * image_multiplier / len(sq_text)
                if(ylen < 0):
                        sq.text(x, y+1, sq_text, color=sq_text_color, ha='left', va='top', fontsize=font_size)
                else:
                        sq.text(x, ylen-1, sq_text, color=sq_text_color, ha='left', va='top', fontsize=font_size)
        return sq

def place_isles(ax, image_multiplier, im_left, im_footer):
        isle_color = '#D8D8D8'
        place_square(ax, 10, 310, 1030, -10, image_multiplier, isle_color, isle_color, "Isle Name", 'black', im_left, im_footer)
        place_square(ax, 10, 260, 400, -10, image_multiplier, isle_color, isle_color, "Isle Name", 'black', im_left, im_footer)
        return ax

def place_stands(ax, image_multiplier, im_left, im_footer):
        for x in stand_location.objects.filter(sl_stand__s_rx_event__re_name__iexact='ISC West 2025'):
                place_square(ax, x.sl_x, x.sl_y, x.sl_x_length, x.sl_y_length, image_multiplier, x.sl_stand.s_stand_fill_color, x.sl_stand.s_stand_outline_color, x.sl_stand.s_name, x.sl_stand.s_text_color, im_left, im_footer)
        return ax

def simulate_profit_demand_chart(prices, demands):
    if len(prices) != len(demands):
        raise ValueError("Prices and demands lists must have the same length")

    profits = [price * demand for price, demand in zip(prices, demands)]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(prices, profits, marker='o', linestyle='-', color='b')
    ax.set_title('Profit Demand Chart')
    ax.set_xlabel('Price')
    ax.set_ylabel('Profit')
    return fig, ax

def wwwrender_floorplan():

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        header_set = []
        footer_set = []

        header_set.append("ISC West 2025")
        header_set.append("Las Vegas, NV")

#eventually add to render call
        footer_set.append("ISC West 2025")
        footer_set.append("Las Vegas, NV")

#eventually store with the event
        floor_length = 1060
        floor_height = 720

        header_space, footer_space, left_space, right_space, image_multiplier, static_loc = get_env_values()
        im_wid = left_space+floor_length+right_space
        im_hei = header_space+floor_height+footer_space
        image_length = (im_wid) * image_multiplier / 100.0
        image_height = (im_hei) * image_multiplier / 100.0
        #0,0 in lower left corner

        floor_title = "Floor Plan"

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(image_length, image_height))

        # Set the limits of the plot
        ax.set_xlim(0, im_wid*image_multiplier)
        ax.set_ylim(0, im_hei*image_multiplier)
        ax.set_aspect('equal')
        ax.axis('off')

        ax = place_header(ax, im_wid, floor_height+footer_space+header_space, left_space, image_multiplier, header_set)
        footer_set.append(static_loc + "---> " + cdatetime)
        ax = place_footer(ax, left_space, footer_space, image_multiplier, footer_set)
        place_square(ax, 0, 0, floor_length, floor_height, image_multiplier, '#ffffff', '#000000', "", 'black', left_space, footer_space)

        ax = place_isles(ax, image_multiplier, left_space, footer_space)
        ax = place_stands(ax, image_multiplier, left_space, footer_space)

#        prices = [10, 20, 30, 40, 50]
#        demands = [100, 80, 60, 40, 20]
#        pdc = simulate_profit_demand_chart(10, 6, prices, demands)



#when running entire, this will need to go into calling function.
        erase_files_in_dir(static_loc)

        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_loc, cdatetime)
        pyplot_filename = pyplot_filename + '.png'

#    create_mov_from_images('images', 'output.mp4')
        return pyplot_filename


def yyyrender_floorplan():
    st_timezone = timezone.now()
    cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
    header_set = []
    footer_set = []

    header_set.append("ISC West 2025")
    header_set.append("Las Vegas, NV")

    footer_set.append("ISC West 2025")
    footer_set.append("Las Vegas, NV")

    floor_length = 1060
    floor_height = 720

    header_space, footer_space, left_space, right_space, image_multiplier, static_loc = get_env_values()
    im_wid = left_space + floor_length + right_space
    im_hei = header_space + floor_height + footer_space
    image_length = (im_wid) * image_multiplier / 100.0
    image_height = (im_hei) * image_multiplier / 100.0

    print(im_wid, im_hei, image_length, image_height)

    floor_title = "Floor Plan"

    prices = [10, 20, 30, 40, 50]
    demands = [100, 80, 60, 40, 20]

    # Create a figure and axis
    fig = plt.figure(figsize=(image_length, image_height))
    gs = gridspec.GridSpec(im_wid, im_hei, figure=fig)
    ax = fig.add_subplot(gs[0:left_space+floor_length, 0:header_space+floor_height])

    # Set the limits of the plot
    ax.set_xlim(0, im_wid * image_multiplier)
    ax.set_ylim(0, im_hei * image_multiplier)
    ax.set_aspect('equal')
    ax.axis('off')

    ax = place_header(ax, im_wid, floor_height + footer_space + header_space, left_space, image_multiplier, header_set)
    footer_set.append(static_loc + "---> " + cdatetime)
    ax = place_footer(ax, left_space, footer_space, image_multiplier, footer_set)
    place_square(ax, 0, 0, floor_length, floor_height, image_multiplier, '#ffffff', '#000000', "", 'black', left_space, footer_space)

    ax = place_isles(ax, image_multiplier, left_space, footer_space)
    ax = place_stands(ax, image_multiplier, left_space, footer_space)

    # Create an inset axis for the profit demand chart at position (700, 700)
    inset_ax = fig.add_subplot(gs[left_space+floor_length+10:im_wid-10, 10:200])

#    inset_ax = fig.add_axes([700 / (im_wid * image_multiplier), 700 / (im_hei * image_multiplier), 0.3, 0.3])
    profit_demand_chart, profit_demand_ax = simulate_profit_demand_chart(prices, demands)
    for line in profit_demand_ax.get_lines():
        inset_ax.plot(line.get_xdata(), line.get_ydata(), marker='o', linestyle='-', color='b')
    inset_ax.set_title('Profit Demand Chart')
    inset_ax.set_xlabel('Price')
    inset_ax.set_ylabel('Profit')

    # Remove the original figure created by simulate_profit_demand_chart
    plt.close(profit_demand_chart)

    erase_files_in_dir(static_loc)

    pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_loc, cdatetime)
    pyplot_filename = pyplot_filename + '.png'

    return pyplot_filename

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


def simple_render_floorplan():

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        header_set = []
        footer_set = []

        header_set.append("ISC West 2025")
        header_set.append("Las Vegas, NV")

#eventually add to render call
        footer_set.append("ISC West 2025")
        footer_set.append("Las Vegas, NV")

#eventually store with the event
        floor_length = 1060
        floor_height = 720

        header_margin, footer_margin, left_margin, right_margin, image_multiplier, static_loc = get_env_values()

        section_one_length = left_margin+floor_length
        section_two_length = right_margin
        total_image_length = left_margin+floor_length+right_margin
        total_image_height = header_margin+floor_height+footer_margin

        image_length = int(total_image_length * image_multiplier / 100)
        image_height = int(total_image_height * image_multiplier / 100)
        image_header_height = int(header_margin * image_multiplier / 100)
        section_one_image_length = int((left_margin+floor_length) * image_multiplier / 100)
        section_two_image_length = int((right_margin) * image_multiplier / 100)

 
        print("image_length: ", image_length)
        print("image_height: ", image_height)
        print("image_header_height: ", image_header_height)
        print("section_one_image_length: ", section_one_image_length)
        print("section_two_image_length: ", section_two_image_length)

        data1 = np.random.rand(6, 35)
        data2 = np.random.rand(2, 39)
        data3 = np.random.rand(2, 120)

        fig = plt.figure(figsize =([12, 8]))    #x, y
        gs = gridspec.GridSpec(8, 12, figure = fig)     #y, x
        gs.update(wspace = 0, hspace = 0)
        ax1 = plt.subplot(gs[0:4, 0:4])         #y, x
        ax1.set_ylabel('ylabel', labelpad = 0, fontsize = 12)
        ax2 = plt.subplot(gs[4:8, 4:8])
        ax2.set_ylabel('blah', labelpad = 0, fontsize = 12)
        ax3 = plt.subplot(gs[0:4, 8:12])
        ax3.set_ylabel('blah2', labelpad = 0, fontsize = 12)

#when running entire, this will need to go into calling function.
        erase_files_in_dir(static_loc)

        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_loc, cdatetime)
        pyplot_filename = pyplot_filename + '.png'

#    create_mov_from_images('images', 'output.mp4')
        return pyplot_filename

def new_place_header(fig, gs, image_margin, header_space, image_length, image_multiplier, header_set):
        ax_upper_x = image_margin * image_multiplier
        ax_upper_y = ax_upper_x
        ax_height = (image_margin+header_space) * image_multiplier
        ax_width = (image_length-(image_margin*2)) * image_multiplier
        ax = fig.add_subplot(gs[ax_upper_y:ax_height, ax_upper_x:ax_width])  # Use the entire grid for the main plot
        print_ax_size(fig, gs, ax, "new_place_header")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000')
        top_pos_x = (ax_width / 2)  # Center horizontally
        top_pos_y = ((ax_height-(4*image_multiplier)))  # Adjust vertical position
        ft_size = 32
        for x in header_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='center', va='center', fontsize=ft_size)
                ft_size = 24
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
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000')
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(10*image_multiplier)))  # Adjust vertical position
        ft_size = 18
        for x in footer_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                ft_size = 14
                top_pos_y = top_pos_y - (60*image_multiplier)  # Adjust spacing between lines
        return(fig)
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
        ax = new_place_rectangle(ax, 0, 0, plt_length*image_multiplier, plt_height*image_multiplier, image_multiplier, '#ffffff', '#ffffff', test_text, '#000000')
        return(fig)
def create_floorplan_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier):
        ax_upper_x = image_margin * image_multiplier
        ax_upper_y = ((image_margin*2) + header_space) * image_multiplier
        ax_height = (image_height - (image_margin*2) - header_space - footer_space) * image_multiplier
        ax_width = int(((image_length)-(image_margin*2))/4)*3 * image_multiplier
#        print(ax_upper_x, ax_upper_y, ax_height, ax_width)
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_height, ax_upper_x:ax_width])  # Use the entire grid for the main plot
        print_ax_size(fig, gs, ax, "create_floorplan_subplot")

        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#000000', test_text, '#000000')
        return(fig)
def create_analysis1_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, analysis_sections, analysis_section_height, analysis_set):
        ax_upper_x = (image_length - (int(((image_length)/4)))) * image_multiplier
        ax_upper_y = (((image_margin*2) + header_space) * image_multiplier)
        ax_height = int(((image_height - (image_margin*2) - header_space - footer_space) / analysis_sections) * analysis_section_height) * image_multiplier
        ax_width = int(((image_length)-(image_margin*2))/4) * image_multiplier
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
        print_ax_size(fig, gs, ax, "create_analysis1_subplot")

#        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        test_text = None
        ax = new_place_rectangle(ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000')
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
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000')
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
                         image_multiplier, '#ffffff', '#ffffff', test_text, '#000000')
        top_pos_x = 1*image_multiplier  # Center horizontally
        top_pos_y = ((ax_height-(1*image_multiplier)))  # Adjust vertical position
        ft_size = 18
        for x in analysis_set:
                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
                top_pos_y = top_pos_y - (4*image_multiplier)  # Adjust spacing between lines
        return(fig)




def render_floorplan():

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        header_set = []
        footer_set = []
        analysis_set_1 = []

        header_set.append("ISC West 2025")
        header_set.append("Las Vegas, NV")
        header_set.append("Blah, Blah, Blah")

#eventually add to render call
        footer_set.append("ISC West 2025")
        footer_set.append("Las Vegas, NV")
        footer_set.append("Blah, Blah, Blah")

        analysis_set_1.append("Analysis 1")
        analysis_set_1.append("Analysis 2")
        analysis_set_1.append("Analysis 3")
        analysis_set_1.append("Analysis 4")
        analysis_set_1.append("Analysis 5")

#eventually store with the event
        floor_length = 1060
        floor_height = 720

        image_length, image_height, image_margin, header_space, footer_space, image_multiplier, static_loc = get_env_values()
        plt_length = int((image_length*image_multiplier)/100.0)
        plt_height = int((image_height*image_multiplier)/100.0)

        fig = plt.figure(figsize=(plt_length, plt_height))    #x, y
        gs = gridspec.GridSpec(plt_height*100, plt_length*100, figure = fig)  # rows, columns
#        print_ax_size(fig, gs, None, "render_floorplan...")
        gs.update(wspace=0, hspace=0)  # Remove any margin between subplots

        fig = create_outer_square(fig, gs, plt_length, plt_height, image_multiplier) 
        fig = new_place_header(fig, gs, image_margin, header_space, image_length, image_multiplier, header_set)
        fig = new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set)
        fig = create_floorplan_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier)
        fig = create_analysis1_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, analysis_set_1)
        fig = create_analysis2_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, 1, analysis_set_1)
        fig = create_analysis3_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 4, 1, analysis_set_1)
#when running entire, this will need to go into calling function.
        erase_files_in_dir(static_loc)

        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_loc, cdatetime)
        pyplot_filename = pyplot_filename + '.png'

#    create_mov_from_images('images', 'output.mp4')
        return pyplot_filename
