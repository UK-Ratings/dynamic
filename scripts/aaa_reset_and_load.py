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

from base.models import *
from scripts.aaa_helper_functions import *


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def zzzget_next_stand_id():
    max_id = stands.objects.aggregate(max_id=Max('s_id'))['max_id']
    return (max_id or 0) + 1
def create_stand(eve, stand_name, stand_number, x, y, x_length, y_length):
        st, created = stands.objects.update_or_create(s_rx_event= eve, 
                        s_name=stand_name,
                        s_number=stand_number,
                        defaults={
                                's_stand_status':'Available', 
                                's_stand_price':'Base'})

        sl = stand_location.objects.update_or_create(sl_stand=st, defaults={
                                'sl_x':x, 'sl_y':y, 'sl_x_length':x_length, 'sl_y_length':y_length})

def zzzpopulate_for_test():
#        f.write("populate_for_test: " + str(timezone.now()) + "\n")
#        record_log_data("aaa_load_test_data.py", "populate_for_test", "populate_for_test")

        eve = rx_event.objects.update_or_create(re_name='ISC West 2025', defaults={
                're_floor_length': 1080, 're_floor_height': 720,
                're_event_start_date': timezone.datetime(2025, 3, 31, 0, 0, 0),
                're_event_end_date': timezone.datetime(2025, 4, 4, 0, 0, 0)})

        if(1==0):  #row 7
                row_amt = 300

                create_stand(eve, 'Stand 1', '1', 20, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 20, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 20, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 4', '4', 20, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 30, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 30, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 30, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 50, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 50, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 50, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 4', '4', 50, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 60, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 60, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 60, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 3', '3', 80, (row_amt - 0), 10, -30)
                create_stand(eve, 'Stand 4', '4', 80, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 90, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 6', '6', 90, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 3', '3', 110, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 4', '4', 110, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 120, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 6', '6', 120, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 3', '3', 140, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 4', '4', 140, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 150, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 6', '6', 150, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 170, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 170, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 170, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 180, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 180, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 180, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 200, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 3', '3', 200, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 210, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 210, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 210, (row_amt - 20), 10, -20)

                create_stand(eve, 'HID', '8053', 230, (row_amt - 0), 40, -40)
                create_stand(eve, 'ASSA ABLOY Entrance Systems', '10053', 280, (row_amt - 0), 30, -40)
                create_stand(eve, 'Bosch Security and Safety Systems', '11053', 320, (row_amt - 0), 80, -40)
                create_stand(eve, 'AXis Communications Inc', '14051', 410, (row_amt - 0), 100, -50)
                create_stand(eve, 'Milestone Systems', '18053', 520, (row_amt - 0), 60, -50)
                create_stand(eve, 'Everon - Nationwide Commercial Security, Fire, and', '20051', 590, (row_amt - 0), 40, -50)
                create_stand(eve, 'TP-Link Systems Inc.', '22053', 640, (row_amt - 0), 30, -50)
                create_stand(eve, 'Stid - Smarter Security Answers', '23051', 680, (row_amt - 0), 30, -50)
                create_stand(eve, 'Allegion', '25053', 720, (row_amt - 0), 30, -40)
                create_stand(eve, 'Affiliated Monitoring, Inc.', '26055', 760, (row_amt - 0), 30, -30)

                create_stand(eve, 'Stand 1', '1', 800, (row_amt - 0), 20, -10)
                create_stand(eve, 'Stand 1', '1', 830, (row_amt - 0), 20, -30)
                create_stand(eve, 'Stand 1', '1', 860, (row_amt - 0), 20, -30)
                create_stand(eve, 'Stand 1', '1', 890, (row_amt - 0), 20, -30)

                create_stand(eve, 'Stand 1', '1', 920, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 2', '2', 920, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 6', '6', 930, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 7', '7', 930, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 950, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 2', '2', 950, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 6', '6', 960, (row_amt - 0), 10, -20)
                create_stand(eve, 'Stand 7', '7', 960, (row_amt - 20), 10, -20)

                create_stand(eve, 'Stand 1', '1', 980, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 2', '2', 980, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 3', '3', 980, (row_amt - 20), 10, -20)
                create_stand(eve, 'Stand 5', '5', 990, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 990, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 990, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 7', '7', 990, (row_amt - 30), 10, -10)

                create_stand(eve, 'Stand 5', '5', 1010, (row_amt - 0), 10, -10)
                create_stand(eve, 'Stand 6', '6', 1010, (row_amt - 10), 10, -10)
                create_stand(eve, 'Stand 7', '7', 1010, (row_amt - 20), 10, -10)
                create_stand(eve, 'Stand 7', '7', 1010, (row_amt - 30), 10, -10)
                create_stand(eve, 'Stand 5', '5', 1020, (row_amt - 0), 10, -10)

        if(1==0):  #row 7
                create_stand(eve, 'Dorking Inc DKS', '20043', 590, 240, 40, -40)
                create_stand(eve, 'Eagle Eye Networks', '20037', 590, 190, 40, -30)
                create_stand(eve, 'Brivo', '20031', 590, 160, 40, -30)
                create_stand(eve, 'Wesco', '20017', 590, 120, 40, -40)
                create_stand(eve, 'dormakaba', '20007', 590, 70, 40, -40)
                create_stand(eve, 'CDVI Americas', '20001', 590, 20, 40, -10)

        if(1==0):  #row 7
                create_stand(eve, 'Speco Technologies', '22059', 640, 310, 30, 30)
                create_stand(eve, '3xLogic', '22067', 640, 350, 30, 30)
                create_stand(eve, 'Suprema', '22075', 640, 390, 30, 40)
                create_stand(eve, 'Qualvision Technology Co. Ltd', '22093', 640, 440, 40, 20)
                create_stand(eve, 'Lounge', '22095', 640, 460, 40, 20)
                create_stand(eve, '3Si', '22099', 640, 490, 30, 30)

                create_stand(eve, 'Smarter Security', '23109', 655, 540, 20, 30)
                create_stand(eve, 'Cheat 1', '1', 655, 580, 20, 30)
                create_stand(eve, 'Cheat 2', '1', 655, 620, 20, 20)
                create_stand(eve, 'Cheat 3', '1', 655, 650, 20, 20)
                create_stand(eve, 'Cheat 4', '1', 655, 680, 20, 20)

def create_event(ev_name, ev_start_date, ev_end_date):
        eve, create = rx_event.objects.update_or_create(re_name=ev_name, defaults={
                're_floor_length': 0, 're_floor_height': 0,
                're_event_start_date': ev_start_date,
                're_event_end_date': ev_end_date})
        return eve
def update_event_length_height(eve, fl_length, fl_height):
        eve.re_floor_length = 1232#fl_length
        eve.re_floor_height = 1052#fl_height
        eve.save()
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



def reset_test_data():
#        f.write("reset tables: " + str(timezone.now()) + "\n")
        rx_event.objects.all().delete()

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

        rxe = create_event('ISC West 2025', timezone.datetime(2025, 3, 31, 0, 0, 0), timezone.datetime(2025, 4, 4, 0, 0, 0))

        filename = 'ISC_West25_floorplan.xlsx'
        ratio_multiplier = 8.333333
        load_floorplan_data(rxe, filename, ratio_multiplier)
        determine_floorplan_max_length_height(rxe)

        filename = 'ISC_West_25_data.xlsx'
        load_transaction_sales_data(rxe, filename)

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()
 

#python manage.py runscript aaa_reset_and_load
