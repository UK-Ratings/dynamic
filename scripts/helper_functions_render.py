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
import random
from base.models import *
from users.models import *

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

from scripts.helper_functions_stand import stand_get_analysis_record
from scripts.helper_functions import *
from scripts.helper_functions_stand import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


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

def get_color(color_type):

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


        #blue for unsold
        if(color_type =='unsold stand outline color'):
                return '#002F6C'
        if(color_type =='unsold stand fill color'):
                return '#ffffff'
        if(color_type =='unsold stand text color'):
                return '#282761'
#        if(color_type =='unsold stand outline color'):
#                return '#002F6C'
#        if(color_type =='unsold stand fill color'):
#                return '#41B6E6'
#        if(color_type =='unsold stand text color'):
#                return '#282761'
        if(color_type =='sold stand outline color'):
                return '#6610f2'
        if(color_type =='sold stand fill color'):
                return '#8745f2'
        if(color_type =='sold stand text color'):
                return '#000000'

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
#    print(f"get_gradient_color: {value}")
    if(value is None):
           return('#FF0000')
    if value < 0:
        value = 0
    if value > 100:
        value = 100

    if value < 50:
#        1 is 170, 27, 31
#        49 is 255, 173, 173
        red = int(((255-170) * value / 50) + 170)
        green = int(((173-27) * value / 50) + 27)
        blue = int(((173-31) * value / 50) + 31)
    else:
#        50 is 161, 251, 142
#       100 is 25, 135, 84                
        green = int(251 - ((251-135) * ((value-50) / 50)))
        blue = int(142 - ((142-84) * ((value-50) / 50)))
        red = int(161 - ((161-25) * ((value-50) / 50)))
#        red = int(100 * (100 - value) / 50)  # Red decreases as value increases
#        blue = int(64 * (100 - value) / 50)  # Blue decreases as value increases
    if value == 0:
        red = 200
        green = 200
        blue = 200
#    print(f"value: {value}, red: {red}, green: {green}, blue: {blue}")
    out_color = f"#{red:02X}{green:02X}{blue:02X}"
#    print(f"out_color: {out_color}")
    return out_color

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
def new_place_rectangle(fig, sq, x, y, xlen, ylen, image_multiplier, fill_color, edge_color, sq_text, sq_text_color, fl_div, line_width, max_text_size, text_bottom_up, top_section_percent):
        rect = patches.Rectangle((x*fl_div, y*fl_div), xlen*fl_div, ylen*fl_div, linewidth=line_width, edgecolor=edge_color, facecolor=fill_color)
#        rect = patches.Rectangle((x, y), xlen, ylen, linewidth=line_width, edgecolor=edge_color, facecolor=fill_color)
        sq.add_patch(rect)
        if (sq_text is not None) and (len(sq_text) > 0):
                title_str = sq_text[0][0]
                info_set = sq_text[1:]
#                if(text_bottom_up):
#                        info_set = list(reversed(info_set))
                top_section = ylen*top_section_percent
                bottom_section = ylen*(1-top_section_percent)
                padding = 1  # Add some padding around the text

                if(1==1):
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
                        total_bottom_text_height = bottom_text_height * len(info_set)
                        if(qq[1] == 'center'):
                                xxpos = x * fl_div + xlen * fl_div / 2  # Center horizontally
                        else:
                                xxpos = (x+1)*fl_div
                        if(text_bottom_up):
                                if(ylen > 0):
                                        ypos = ((y)*fl_div) + total_bottom_text_height#+ bottom_text_height 
                                else:
                                        ypos = ((y+ylen)*fl_div) + total_bottom_text_height# + bottom_text_height
                        else:
                                if(ylen > 0):
                                        ypos = ((y * fl_div) + (ylen * fl_div) - (padding*fl_div) - (top_section*fl_div))  # Position at the top with padding
                                else:
                                        ypos = ((y * fl_div) - (padding*fl_div) - (top_section*fl_div))  # Position at the top with padding
                        for qq in info_set:
                                sq.text(
                                        xxpos,
                                        ypos,
                                        qq[0],
                                        color=sq_text_color,
                                        ha=qq[1],
                                        va=qq[2],
                                        fontsize=int(bottom_font_size))

                                ypos -= (bottom_text_height)  # Adjust vertical position for the next line#
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
        ax = new_place_rectangle(fig, ax, 0, 0, plt_length*image_multiplier, plt_height*image_multiplier, image_multiplier, '#ffffff', '#ffffff', None, '#000000', 1, 3, 100, True, 0.4)
        return(fig)

def zzzcreate_analysis1_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, analysis_sections, analysis_section_height, analysis_set):
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
#        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, image_multiplier, '#ffffff', '#000000', analysis_set, '#000000', fl_div, 1, 50, True)

#        top_pos_x = 1*image_multiplier  # Center horizontally
#        top_pos_y = ((ax_height-(1*image_multiplier)))  # Adjust vertical position
#        ft_size = 18
#        for x in analysis_set:
#                ax.text(top_pos_x, top_pos_y, x, color='black', ha='left', va='top', fontsize=ft_size)
#                top_pos_y = top_pos_y - (6*image_multiplier)  # Adjust spacing between lines
        return(fig)
def zzzcreate_analysis2_subplot(fig, gs, image_margin, header_space, footer_space, image_length, 
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
def zzzcreate_analysis3_subplot(fig, gs, image_margin, header_space, footer_space, image_length, 
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

def floorplan_new_place_stands(rxe, fig, ax, image_multiplier, fl_div, run_id):
        for st in stands.objects.filter(s_rx_event=rxe):
                sl_x = stand_attributes_get_value(st, None, 'Stand x')
                sl_y = stand_attributes_get_value(st, None, 'Stand y')
                sl_x_length = stand_attributes_get_value(st, None, 'Stand x length')
                sl_y_length = stand_attributes_get_value(st, None, 'Stand y length')
                #Available, Sold, New Sell, Reserved, New Stand
                sa_analysis_number, sa_analysis_title, spg = stand_get_analysis_record(st, run_id, None, 'Sq Gradient')
#                print(f"sa_analysis_number: {sa_analysis_number}, sa_analysis_title: {sa_analysis_title}, spg: {spg}")
                if(spg is None):
                        spg = 0
                st_status = stand_attributes_get_value(st, None, 'Stand Status')
                if(st_status == 'Available'):
                        stand_fill_color = get_color('unsold stand fill color')
                        stand_outline_color = get_color('unsold stand outline color')
                        text_color = get_color('unsold stand text color')
                if(st_status == 'Sold'):
                        stand_fill_color = get_gradient_color(spg)
                        stand_outline_color = get_color('sold stand outline color')
                        text_color = get_color('sold stand text color')
                if(st_status == 'New Sell'):
                        stand_fill_color = get_gradient_color(spg)
                        stand_outline_color = get_color('sold stand outline color')
                        text_color = get_color('sold stand text color')
                        circle_fill_color = get_color('sold stand circle fill color')
                        circle_outline_color = get_color('sold stand circle outline color')
                        text_color = get_color('sold stand circle text color')
                        ax = new_place_circle(ax, sl_x, sl_y, sl_x_length, sl_y_length, circle_fill_color, circle_outline_color, fl_div, 40)

                #Base, Price Increase, Price Decrease 
                st_price = stand_attributes_get_value(st, None, 'Stand Price')
                if(st_price == 'Price Increase'):
                        stand_fill_color = get_color('price increase stand fill color')
                        stand_outline_color = get_color('price increase stand outline color')
                        text_color = get_color('price increase stand text color')
                if(st_price == 'Price Decrease'):
                        stand_fill_color = get_color('price decrease stand fill color')
                        stand_outline_color = get_color('price decrease stand outline color')
                        text_color = get_color('price decrease stand text color')

                if(sl_x_length * sl_y_length > 1):
                        new_stand = []
                        if(st_status in ('Sold', 'New Sell')):
                                if(st.s_number is not None and len(st.s_number) > 0):
                                        new_stand.append([str(st.s_number), 'center', 'top'])
                                else:
                                        new_stand.append(['Missing Stand Number', 'center', 'top'])
                                new_stand.append(["Name: " + str(st.s_name), 'left', 'top'])
                                new_stand.append(["Stand Price: "+str(stand_attributes_get_value(st, None, 'Stand Price')), 'left', 'top'])
#                                new_stand.append(["Stand Price Gradient: " + str(stand_attributes_get_value(st, None, 'Stand Price Gradient')), 'left', 'top'])
#                                rsa = stand_analysis.objects.filter(sa_stand=x.sl_stand).order_by('sa_analysis_number')


                                rsa = stand_get_all_analysis_records(st, run_id)
                                for r in rsa:
                                        if(r[1] != 'MC Rules Applied'):
#                                        sa_analysis_number, sa_analysis_title, sa_analysis_value = stand_get_analysis_record(r.sa_stand, run_id, None, r.sa_analysis_title)
#                                        new_stand.append([str(sa_analysis_title)+": "+str(sa_analysis_value), 'left', 'top'])
                                                new_stand.append(["A-"+str(r[1])+": "+str(r[2]), 'left', 'top'])
                        ax = new_place_rectangle(fig, ax, sl_x, sl_y, sl_x_length, sl_y_length, image_multiplier, stand_fill_color, stand_outline_color, new_stand, text_color, fl_div, 1, 50, True, 0.4)
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
        if(len(header_set) == 1):
               header_title_percentage = 1
        else:
               header_title_percentage = 0.5
        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', header_set, '#000000', 1, 3, 300, True, header_title_percentage)
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
        if(len(footer_set) == 1):
               footer_title_percentage = 1
        else:
               footer_title_percentage = 0.6
        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, 
                         image_multiplier, '#ffffff', '#ffffff', footer_set, '#000000', 1, 3, 300, True, footer_title_percentage)
        return(fig)

def create_sold_info_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, 
                             image_multiplier, analysis_sections, analysis_section_height, upper, analysis_set):
 
        potential_plot_height = (image_height - (image_margin*2) - header_space - footer_space)

        ax_upper_x = int((image_length - (int(((image_length)/4))) - image_margin) * image_multiplier)
        ax_height = int((potential_plot_height / 2) * image_multiplier)
        ax_width = int((((image_length)-(image_margin*2))/4) * image_multiplier)

        if(upper):
                ax_upper_y = int((image_margin + header_space) * image_multiplier)
        else:
                ax_upper_y = int((image_margin+header_space+(potential_plot_height/2)) * image_multiplier)
        fl_div = 1.0
 
        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
#        print_ax_size(fig, gs, ax, "create_analysis1_subplot")

#        # Set the limits of the plot
        ax.set_xlim(0, ax_width)
        ax.set_ylim(0, ax_height)
        ax.axis('off')
        ax = new_place_rectangle(fig, ax, 0, 0, ax_width, ax_height, image_multiplier, '#ffffff', '#000000', analysis_set, '#000000', fl_div, 1, 200, False, 0.2)
        return(fig)

def floorplan_subplot(rxe, fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floorplan_length, floorplan_height, run_id):
    potential_plot_height = (image_height - (image_margin*4) - header_space - footer_space) * image_multiplier
    potential_plot_length = (image_length - (image_margin*2)) * image_multiplier
    height_div = (potential_plot_height / floorplan_height)
    length_div = (potential_plot_length / floorplan_length)
    fl_div = min(height_div, length_div)

    # Calculate bounding box for all squares
    all_stands = stands.objects.filter(s_rx_event=rxe)
    min_x = min(stand_attributes_get_value(st, None, 'Stand x') for st in all_stands)
    min_y = min(stand_attributes_get_value(st, None, 'Stand y') for st in all_stands)
    max_x = max(stand_attributes_get_value(st, None, 'Stand x') + stand_attributes_get_value(st, None, 'Stand x length') for st in all_stands)
    max_y = max(stand_attributes_get_value(st, None, 'Stand y') + stand_attributes_get_value(st, None, 'Stand y length') for st in all_stands)
#    print(f"min_x: {min_x}, min_y: {min_y}, max_x: {max_x}, max_y: {max_y}")

    ax_width = int((max_x - min_x) * fl_div)
    ax_height = int((max_y - min_y) * fl_div)
    ax_upper_x = int(((image_length * image_multiplier) - ax_width) / 2)
    ax_upper_y = int(((image_margin*2) + (header_space)) * image_multiplier)

    ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])

    # Set the limits of the plot to zoom in on the bounding box
    ax.set_xlim(min_x * fl_div, max_x * fl_div)
    ax.set_ylim(min_y * fl_div, max_y * fl_div)
    ax.axis('off')

    ax = new_place_rectangle(fig, ax, int(min_x * fl_div), int(min_y * fl_div), int((max_x - min_x) * fl_div), int((max_y - min_y) * fl_div), 
                         image_multiplier, '#ffffff', '#ffffff', None, '#000000', 1, 3, 100, True, 0.4)

    ax = floorplan_new_place_stands(rxe, fig, ax, image_multiplier, fl_div, run_id)
    return(fig)

def render_floorplan(rxe, header_set, footer_set, message_set, analysis_set_top, analysis_set_bottom, image_multiplier, floorplan_type, run_id):
        record_log_data("aaa_helper_functions.py", "run_event_year", "starting: event name: " + str(rxe.re_name))

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        footer_set.append([cdatetime + '.png', 'left', 'top'])
        floor_length = rxe.re_floor_length 
        floor_height = rxe.re_floor_height

        image_length, image_height, image_margin, header_space, footer_space, im_multi, im_multi_sm, static_floorplan_loc, static_analysis_loc = get_env_values()
        plt_length = int((image_length*image_multiplier)/100.0)
        plt_height = int((image_height*image_multiplier)/100.0)

        fig = plt.figure(figsize=(plt_length, plt_height))    #x, y
        gs = gridspec.GridSpec(plt_height*100, plt_length*100, figure = fig)  # rows, columns
#        print_ax_size(fig, gs, None, "render_floorplan...")
        gs.update(wspace=0, hspace=0)  # Remove any margin between subplots

        fig = create_outer_square(fig, gs, plt_length, plt_height, image_multiplier) 
        fig = new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set)
        fig = new_place_header(fig, gs, image_margin, header_space, image_length, image_height, image_multiplier, header_set, footer_space)

        if(floorplan_type in ('Initial', 'Final') or (len(analysis_set_top) == 0 and len(analysis_set_bottom) == 0)):
                fig = floorplan_subplot(rxe, fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floor_length, floor_height, run_id)
        else:
                fig = floorplan_subplot(rxe, fig, gs, image_margin, header_space, footer_space, image_length*.70, image_height, image_multiplier, floor_length, floor_height, run_id)
                upper = True
                fig = create_sold_info_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 4, 2, upper, analysis_set_top)
                upper = False
                fig = create_sold_info_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, upper, analysis_set_bottom)
#        fig = create_analysis2_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 3, 1, analysis_set_1)
#        fig = create_analysis3_subplot(fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, 5, 4, 1, analysis_set_1)

        pyplot_filename, pyplot_path = write_pyplot_to_file(plt, static_floorplan_loc, cdatetime)
        plt.close(fig)

        record_log_data("aaa_helper_functions.py", "run_event_year", "completed: event name: " + str(rxe.re_name))
        return pyplot_filename


