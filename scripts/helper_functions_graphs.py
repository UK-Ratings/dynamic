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
from scripts.helper_functions_render import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def plot_event_sales_by_run(rxe, ax):
    # Fetch data from event_sales_by_run
    sales_data = event_sales_by_run.objects.filter(esbr_stand__s_rx_event=rxe)

    # Prepare data for plotting
    data = pd.DataFrame(
        {
            'date': [sale.esbr_sold_date for sale in sales_data],
            'revenue': [sale.esbr_revenue_amount for sale in sales_data],
            'run_id': [sale.esbr_run_id for sale in sales_data]
        }
    )

    # Group data by run_id and date, summing revenue
    grouped_data = data.groupby(['run_id', 'date']).sum().reset_index()

    # Calculate cumulative revenue for each run_id
    grouped_data['cumulative_revenue'] = grouped_data.groupby('run_id')['revenue'].cumsum()

    # Plot each run_id as a separate line on the provided axis
    for run_id, group in grouped_data.groupby('run_id'):
        ax.plot(group['date'], group['cumulative_revenue'], label=f'Run ID {run_id}')

    # Add labels, legend, and title
    ax.set_xlabel('Date', fontsize=128)
    ax.set_ylabel('Cumulative Revenue ($M)', fontsize=128)
    ax.set_title('Event Sales by Run (Cumulative)', fontsize=128)
    ax.legend(fontsize=30)
    ax.grid(True)
#    ax.set_position([0.1, 0.1, 0.8, 0.8])  # Center the plot within ax
    ax.set_position([0.25, 0.2, 0.55, 0.55])  # Center the plot within ax
    ax.tick_params(axis='x', labelsize=72)
    ax.tick_params(axis='y', labelsize=72)
    return ax
def render_revenue_graph_subplot(rxe, fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floorplan_length, floorplan_height):
        ax_upper_x = int(image_margin * image_multiplier)
        ax_upper_y = int((image_margin*2 + header_space) * image_multiplier)
        ax_height = int((header_space+footer_space+(image_margin*4)) * image_multiplier) 
        ax_width = int((image_length-(image_margin*2)) * image_multiplier)

        ax = fig.add_subplot(gs[ax_upper_y:ax_upper_y+ax_height, ax_upper_x:ax_upper_x+ax_width])  # Use the entire grid for the main plot
        plot_event_sales_by_run(rxe, ax)
        return ax
def render_revenue_graph(rxe, header_set, footer_set, image_multiplier):
        record_log_data("aaa_helper_functions_graphs.py", "render_revenue_graph", "starting: event name: " + str(rxe.re_name))

        st_timezone = timezone.now()
        cdatetime = str(st_timezone).replace(" ", "").replace(":", "").replace("+", "")
        footer_set.append([cdatetime + '.png', 'left', 'top'])
        floor_length = rxe.re_floor_length 
        floor_height = rxe.re_floor_height

        image_length, image_height, image_margin, header_space, footer_space, im_multi, im_multi_sm = get_env_values()
        plt_length = int((image_length*image_multiplier)/100.0)
        plt_height = int((image_height*image_multiplier)/100.0)

        fig = plt.figure(figsize=(plt_length, plt_height))    #x, y
        gs = gridspec.GridSpec(plt_height*100, plt_length*100, figure = fig)  # rows, columns
#        print_ax_size(fig, gs, None, "render_floorplan...")
        gs.update(wspace=0, hspace=0)  # Remove any margin between subplots

        fig = create_outer_square(fig, gs, plt_length, plt_height, image_multiplier) 
        fig = new_place_footer(fig, gs, image_margin, footer_space, image_length, image_height, image_multiplier, footer_set)
        fig = new_place_header(fig, gs, image_margin, header_space, image_length, image_height, image_multiplier, header_set, footer_space)
        ax = render_revenue_graph_subplot(rxe, fig, gs, image_margin, header_space, footer_space, image_length, image_height, image_multiplier, floor_length, floor_height)


        if os.environ.get("RX_STATIC_GRAPHS_LOCATION") is not None:
                dir_loc = str(os.environ.get("RX_STATIC_GRAPHS_LOCATION"))
        else:
                dir_loc = None
        if( dir_loc is not None):
            pyplot_filename, pyplot_path = write_pyplot_to_file(plt, dir_loc, cdatetime)
        plt.close(fig)

        record_log_data("aaa_helper_functions_graphs.py", "render_revenue_graph", "completes: event name: " + str(rxe.re_name))
        return pyplot_filename



