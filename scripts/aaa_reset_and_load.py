#!/usr/bin/env python3

from django.utils import timezone
from django.contrib import messages
import os
from dotenv import load_dotenv
from django.conf import settings
from django.db.models import Max
import numpy as np
import pandas as pd
from pandas._libs.tslibs.nattype import NaTType
import random
import datetime


from base.models import *
from scripts.helper_functions import *
from scripts.helper_functions_render import *


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def create_stand(eve, stand_name, stand_number, x, y, x_length, y_length):
#        if(stand_number == "2123" or stand_name == "Verkada"):
#                print("create_stand: ", stand_name, stand_number, x, y, x_length, y_length)
        st, created = stands.objects.update_or_create(s_rx_event= eve, 
                        s_name=stand_name,
                        s_number=stand_number,
                        defaults={
                                's_stand_status':'Available', 
                                's_stand_price':'Base',
                                's_stand_price_gradient': random.randint(0, 100),})

        sl = stand_location.objects.update_or_create(sl_stand=st, defaults={
                                'sl_x':x, 'sl_y':y, 'sl_x_length':x_length, 'sl_y_length':y_length})

def create_event_group(group_name):
        try:
                event_group = rx_event_group.objects.get(reg_name=group_name)
        except rx_event_group.DoesNotExist:
                event_group = rx_event_group.objects.create(reg_name=group_name)
        return event_group
def create_event(eg_name, ev_name, ev_start_date, ev_end_date):
        egn = create_event_group(eg_name)
        eve, create = rx_event.objects.update_or_create(re_event_group = egn, 
                re_name=ev_name, defaults={
                're_floor_length': 0, 're_floor_height': 0,
                're_event_start_date': ev_start_date,
                're_event_end_date': ev_end_date})
        return eve
def update_event_length_height(eve, fl_length, fl_height):
        eve.re_floor_length = 1232#fl_length
        eve.re_floor_height = 1052#fl_height
        eve.save()
def load_floorplan_data(rxe, filename, ratio_multiplier):
        file_path = os.path.join(settings.BASE_DIR, 'data', filename)
        if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

        data = pd.read_excel(file_path)

    # Iterate through each row and create instances of event_sales_transactions
        for _, row in data.iterrows():
                max_length, min_length, side_lengths = get_polygon_side_lengths(row['geometry'], ratio_multiplier)
                xpos, ypos = get_nearest_position_to_origin(row['geometry'], ratio_multiplier)
                create_stand(rxe, row['Display Name'], row['Stand: Stand Name'], xpos, ypos, row['Width'], row['Length'])#row['Length'], row['Width'])
def determine_floorplan_max_length_height(rxe):

        min_x_length = 0
        min_y_length = 0
        max_x_length = 0
        max_y_length = 0

        for x in stand_location.objects.filter(sl_stand__s_rx_event=rxe):
                if(x.sl_x < min_x_length):
                        min_x_length = x.sl_x + x.sl_x_length
                if(x.sl_y < min_y_length):
                        min_y_length = x.sl_y + x.sl_y_length   
                if(x.sl_x + x.sl_x_length > max_x_length):
                        max_x_length = x.sl_x + x.sl_x_length
                if(x.sl_y + x.sl_y_length > max_y_length):
                        max_y_length = x.sl_y + x.sl_y_length
#        print("min_x_length: ", min_x_length, "min_y_length: ", min_y_length, "max_x_length: ", max_x_length, "max_y_length: ", max_y_length)
        update_event_length_height(rxe, abs(min_x_length)+abs(max_x_length), abs(min_y_length)+abs(max_y_length))

def zzzload_transaction_sales_data(rxe, filename):
        file_path = os.path.join(settings.BASE_DIR, 'data', filename)
        if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

        data = pd.read_excel(file_path)

    # Iterate through each row and create instances of event_sales_transactions
        for _, row in data.iterrows():
                if not isinstance(row['Order Created Date'], NaTType) and row['Recipient Country'] is not None and len(row['Recipient Country']) > 0:
                        last_modified_date = timezone.make_aware(row['Last Modified Date']) if pd.notnull(row['Last Modified Date']) else None
                        order_created_date = timezone.make_aware(row['Order Created Date']) if pd.notnull(row['Order Created Date']) else None

                        up, create = event_sales_transactions.objects.update_or_create(
                                est_event=rxe,
                                est_Company_Name=row['Company Name'],
                                est_Recipient_Country=row['Recipient Country'],
                                est_Customer_Type=row['Customer Type'],
                                est_Opportunity_Type=row['Opportunity Type'],
                                est_Opportunity_Owner=row['Opportunity Owner'],
                                est_Stand_Name_Length_Width=row['Stand Name (Length * Width)'],
                                est_Stand_Area=row['Stand Area'],
                                est_Number_of_Corners=row['Number of Corners'],
                                est_Stand_Zone=row['Stand Zone'],
                                est_Floor_Plan_Sector=row['Floor Plan Sector'],
                                est_Sharer_Entitlements=row['Sharer Entitlements'],
                                est_Last_Modified_Date=last_modified_date,
                                est_Total_Net_Amount=row['Total Net Amount'],
                                est_Order_Created_Date=order_created_date,
                                est_Packages_Sold=row['Packages Sold'],
                                est_Product_Name=row['Product Name'],)

#        cn = 'AIC Inc.'
#        cn = 'Aiphone Corporation'
        if(1==0):
                for x in event_sales_transactions.objects.filter(est_event=rxe):
                        print(x.est_event, x.est_Company_Name, x.est_Recipient_Country, x.est_Customer_Type, x.est_Opportunity_Type,
                                x.est_Opportunity_Owner, x.est_Stand_Name_Length_Width, x.est_Stand_Area, x.est_Number_of_Corners,
                                x.est_Stand_Zone, x.est_Floor_Plan_Sector, x.est_Sharer_Entitlements, x.est_Sharer_Companies,
                                x.est_Last_Modified_Date, x.est_Total_Net_Amount, x.est_Order_Created_Date, x.est_Packages_Sold,
                                x.est_Product_Name, x.est_Stand_Name_Cleaned, x.est_Stand_Name_Dim_Cleaned)

#        for x in event_sales_transactions.objects.filter(est_event=rxe, est_Company_Name=cn):
        for x in event_sales_transactions.objects.filter(est_event=rxe):
                snlw = x.est_Stand_Name_Length_Width.split(",")
                if(len(snlw) > 0):
                        first = True
#                        print("snlw: ", x.est_Stand_Name_Length_Width, snlw )
                        for y in snlw:
                                first_space_index = y.find(" ")
                                if first_space_index != -1:
                                        st_name = y[:first_space_index].strip()
                                        st_dim = y[first_space_index:].strip()
#                                        print("y: ", x.est_Stand_Name_Length_Width, y, st_name, st_dim )
                                        if first:
                                                x.est_Stand_Name_Cleaned = st_name
                                                x.est_Stand_Name_Dim_Cleaned = st_dim
                                                x.save()
                                                first = False
                                        else:
                                                up, create = event_sales_transactions.objects.update_or_create(
                                                        est_event=x.est_event,
                                                        est_Company_Name=x.est_Company_Name,
                                                        est_Recipient_Country=x.est_Recipient_Country,
                                                        est_Customer_Type=x.est_Customer_Type,
                                                        est_Opportunity_Type=x.est_Opportunity_Type,
                                                        est_Opportunity_Owner=x.est_Opportunity_Owner,
                                                        est_Stand_Name_Length_Width=x.est_Stand_Name_Length_Width,
                                                        est_Stand_Area=x.est_Stand_Area,
                                                        est_Number_of_Corners=x.est_Number_of_Corners,
                                                        est_Stand_Zone=x.est_Stand_Zone,
                                                        est_Floor_Plan_Sector=x.est_Floor_Plan_Sector,
                                                        est_Sharer_Entitlements=x.est_Sharer_Entitlements,
                                                        est_Last_Modified_Date=x.est_Last_Modified_Date,
                                                        est_Total_Net_Amount=0,
                                                        est_Order_Created_Date=x.est_Order_Created_Date,
                                                        est_Packages_Sold=x.est_Packages_Sold,
                                                        est_Product_Name=x.est_Product_Name,
                                                        est_Stand_Name_Cleaned=st_name,
                                                        est_Stand_Name_Dim_Cleaned=st_dim)

        if(1==0):
#                cn = 'Milestone Systems'
#                for x in event_sales_transactions.objects.filter(est_event=rxe, est_Company_Name=cn):
                for x in event_sales_transactions.objects.filter(est_event=rxe):
                        print(x.est_event, x.est_Company_Name, x.est_Recipient_Country, x.est_Customer_Type, x.est_Opportunity_Type,
                                x.est_Opportunity_Owner, x.est_Stand_Name_Length_Width, x.est_Stand_Area, x.est_Number_of_Corners,
                                x.est_Stand_Zone, x.est_Floor_Plan_Sector, x.est_Sharer_Entitlements, x.est_Sharer_Companies,
                                x.est_Last_Modified_Date, x.est_Total_Net_Amount, x.est_Order_Created_Date, x.est_Packages_Sold,
                                x.est_Product_Name, x.est_Stand_Name_Cleaned, x.est_Stand_Name_Dim_Cleaned)

def load_transaction_sales_data(rxe, filename):
        file_path = os.path.join(settings.BASE_DIR, 'data', filename)
        if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

        data = pd.read_excel(file_path)

    # Iterate through each row and create instances of event_sales_transactions
        for _, row in data.iterrows():
                if not isinstance(row['Order Created Date'], NaTType) and row['Recipient Country'] is not None and len(row['Recipient Country']) > 0:
                        last_modified_date = timezone.make_aware(row['Last Modified Date']) if pd.notnull(row['Last Modified Date']) else None
                        order_created_date = timezone.make_aware(row['Order Created Date']) if pd.notnull(row['Order Created Date']) else None
                        if(str(row['Stand Zone'])[0] == ","):
                                szr = str(row['Stand Zone'])[1:]
                        else:
                                szr = str(row['Stand Zone'])
                        szr = szr.strip()

                        up, create = event_sales_transactions.objects.update_or_create(
                                est_event=rxe,
                                est_Company_Name=row['Company Name'],
                                est_Recipient_Country=row['Recipient Country'],
                                est_Customer_Type=row['Customer Type'],
                                est_Opportunity_Type=row['Opportunity Type'],
                                est_Opportunity_Owner=row['Opportunity Owner'],
                                est_Stand_Name_Length_Width=row['Stand Name (Length * Width)'],
                                est_Stand_Area=row['Stand Area'],
                                est_Number_of_Corners=row['Number of Corners'],
                                est_Stand_Zone=szr,#row['Stand Zone'],
                                est_Floor_Plan_Sector=row['Floor Plan Sector'],
                                est_Sharer_Entitlements=row['Sharer Entitlements'],
                                est_Last_Modified_Date=last_modified_date,
                                est_Total_Net_Amount=row['Total Net Amount'],
                                est_Order_Created_Date=order_created_date,
                                est_Packages_Sold=row['Packages Sold'],
                                est_Product_Name=row['Product Name'],)

        cn = 'Verkada'
#        cn = 'Aiphone Corporation'
        if(1==0):
                for x in event_sales_transactions.objects.filter(est_event=rxe, est_Company_Name=cn):
                        print(x.est_event, x.est_Company_Name, x.est_Recipient_Country, x.est_Customer_Type, x.est_Opportunity_Type,
                                x.est_Opportunity_Owner, x.est_Stand_Name_Length_Width, x.est_Stand_Area, x.est_Number_of_Corners,
                                x.est_Stand_Zone, x.est_Floor_Plan_Sector, x.est_Sharer_Entitlements, x.est_Sharer_Companies,
                                x.est_Last_Modified_Date, x.est_Total_Net_Amount, x.est_Order_Created_Date, x.est_Packages_Sold,
                                x.est_Product_Name, x.est_Stand_Name_Cleaned, x.est_Stand_Name_Dim_Cleaned)

#        for x in event_sales_transactions.objects.filter(est_event=rxe, est_Company_Name=cn):
        for x in event_sales_transactions.objects.filter(est_event=rxe):
                snlw = x.est_Stand_Name_Length_Width.split(", ")
                noc = x.est_Number_of_Corners.split(",")
                sz = x.est_Stand_Zone.split(",")
                fps = x.est_Floor_Plan_Sector.split(",")
                if(len(fps) > 1):
                        for qq in snlw:
                                print(qq)
                        for qq in noc:
                                print(qq)
                        for qq in sz:
                                print("sz", qq, "----", x.est_Stand_Zone)
                        for qq in fps:
                                print("fps", qq, "----", x.est_Floor_Plan_Sector)
                if(len(snlw) > 0):
                        noc_cnt = 0
                        first = True
#                        print("snlw: ", x.est_Stand_Name_Length_Width, snlw )
                        for y in snlw:
                                try:
                                        noc_val = noc[noc_cnt]
                                except:
                                        noc_val = 0
                                try:
                                        sz_val = sz[noc_cnt].strip()
                                except:
                                       sz_val = sz[0].strip()
                                try:
                                        fps_val = fps[noc_cnt].strip()
                                except:
                                       fps_val = fps[0].strip()
                                first_space_index = y.find(" ")
                                if first_space_index != -1:
                                        st_name = y[:first_space_index].strip()
                                        st_dim = y[first_space_index:].strip()
#                                        print("y: ", x.est_Stand_Name_Length_Width, y, st_name, st_dim )
                                        if first:
                                                x.est_Stand_Name_Cleaned = st_name
                                                x.est_Stand_Name_Dim_Cleaned = st_dim
                                                x.est_Number_of_Corners = noc_val
                                                x.est_Stand_Zone = sz_val
                                                x.est_Floor_Plan_Sector = fps_val
                                                x.save()
                                                first = False
                                        else:
                                                up, create = event_sales_transactions.objects.update_or_create(
                                                        est_event=x.est_event,
                                                        est_Company_Name=x.est_Company_Name,
                                                        est_Recipient_Country=x.est_Recipient_Country,
                                                        est_Customer_Type=x.est_Customer_Type,
                                                        est_Opportunity_Type=x.est_Opportunity_Type,
                                                        est_Opportunity_Owner=x.est_Opportunity_Owner,
                                                        est_Stand_Name_Length_Width=x.est_Stand_Name_Length_Width,
                                                        est_Stand_Area=x.est_Stand_Area,
                                                        est_Number_of_Corners=noc_val,#x.est_Number_of_Corners,
                                                        est_Stand_Zone=sz_val,#x.est_Stand_Zone,
                                                        est_Floor_Plan_Sector=fps_val,#x.est_Floor_Plan_Sector,
                                                        est_Sharer_Entitlements=x.est_Sharer_Entitlements,
                                                        est_Last_Modified_Date=x.est_Last_Modified_Date,
                                                        est_Total_Net_Amount=0,
                                                        est_Order_Created_Date=x.est_Order_Created_Date,
                                                        est_Packages_Sold=x.est_Packages_Sold,
                                                        est_Product_Name=x.est_Product_Name,
                                                        est_Stand_Name_Cleaned=st_name,
                                                        est_Stand_Name_Dim_Cleaned=st_dim)
                                noc_cnt = noc_cnt + 1
        if(1==0):
                for x in event_sales_transactions.objects.filter(est_event=rxe, est_Company_Name=cn):
#                for x in event_sales_transactions.objects.filter(est_event=rxe):
                        print(x.est_event, x.est_Company_Name, x.est_Recipient_Country, x.est_Customer_Type, x.est_Opportunity_Type,
                                x.est_Opportunity_Owner, x.est_Stand_Name_Length_Width, x.est_Stand_Area, x.est_Number_of_Corners,
                                x.est_Stand_Zone, x.est_Floor_Plan_Sector, x.est_Sharer_Entitlements, x.est_Sharer_Companies,
                                x.est_Last_Modified_Date, x.est_Total_Net_Amount, x.est_Order_Created_Date, x.est_Packages_Sold,
                                x.est_Product_Name, x.est_Stand_Name_Cleaned, x.est_Stand_Name_Dim_Cleaned)

def reset_test_data():
#        f.write("reset tables: " + str(timezone.now()) + "\n")
        rx_event.objects.all().delete()
        event_sales_transactions.objects.all().delete()
        log_page_data.objects.all().delete()
        log_progress_data.objects.all().delete()
        log_messages.objects.all().delete()
        log_error_data.objects.all().delete()

def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"

#        f = open(logs_filename, "w", encoding='utf-8')
#        f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
#        f.write("database_host_name: " + db_host_name + "\n")
#        f.write("database_name: " + db_name + "\n")

        record_log_data("aaa_reset_and_load.py", "reset data", "reset data")
        reset_test_data()

        start_date = timezone.make_aware(datetime.datetime(2024, 4, 9, 0, 0, 0))
        end_date = timezone.make_aware(datetime.datetime(2024, 4, 12, 0, 0, 0))
        rxe = create_event('ISC West', 'ISC West 2024', start_date, end_date)
        filename = 'ISC_West_24_data.xlsx'
        load_transaction_sales_data(rxe, filename)

        start_date = timezone.make_aware(datetime.datetime(2025, 3, 31, 0, 0, 0))
        end_date = timezone.make_aware(datetime.datetime(2025, 4, 4, 0, 0, 0))
        rxe = create_event('ISC West', 'ISC West 2025', start_date, end_date)
        filename = 'ISC_West_25_data.xlsx'
        load_transaction_sales_data(rxe, filename)

        filename = 'ISC_West25_floorplan.xlsx'
        ratio_multiplier = 8.333333
        load_floorplan_data(rxe, filename, ratio_multiplier)
        determine_floorplan_max_length_height(rxe)


#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()
 

#python manage.py runscript aaa_reset_and_load
