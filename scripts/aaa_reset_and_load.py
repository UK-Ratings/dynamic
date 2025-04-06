#!/usr/bin/env python3

from django.utils import timezone
import os
from dotenv import load_dotenv
from django.conf import settings
import pandas as pd
from pandas._libs.tslibs.nattype import NaTType
import datetime
import csv

from base.models import *
from scripts.helper_functions_render import *
from scripts.helper_functions_event import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

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
def load_stand_attribute_data(rxe, filename):
        file_path = os.path.join(settings.BASE_DIR, 'data', filename)
        if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

        data = pd.read_excel(file_path)

    # Iterate through each row and create instances of event_sales_transactions
        for _, row in data.iterrows():
                up, create = stands_attribute_data.objects.update_or_create(
                        sad_event=rxe,
                        sad_stand_name=row['Stand Name'],
                        sad_title=row['Title'],
                        sad_value=row['Value'],
                        sad_data_type=row['Data Type'],
                        sad_datetime=timezone.now(),)

#                print(f"load_stand_attribute_data: {row}")
                for st in stands.objects.filter(s_rx_event=rxe, s_number=row['Stand Name']):
#                        print(f"load_stand_attribute_data: {st} {row['Stand Name']}")
                        stand_attributes_record(st, None, str(row['Title']), str(row['Value']), str(row['Data Type']), timezone.now())
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
#                if(len(fps) > 1):
#                        for qq in snlw:
#                                print(qq)
#                        for qq in noc:
#                                print(qq)
#                        for qq in sz:
#                                print("sz", qq, "----", x.est_Stand_Zone)
#                        for qq in fps:
#                                print("fps", qq, "----", x.est_Floor_Plan_Sector)
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

def load_error_report_stand(rxe):
        print(f"load_error_report_stand: {rxe}")
        errors = []
        #first - look for stands with no x, y, x_length, y_lenght attributes
        for st_stand in stands.objects.filter(s_rx_event=rxe).order_by('s_number'):
                x = stand_attributes_get_value(st_stand, None, 'Stand x')
                y = stand_attributes_get_value(st_stand, None, 'Stand y')
                x_length = stand_attributes_get_value(st_stand, None, 'Stand x length')
                y_length = stand_attributes_get_value(st_stand, None, 'Stand y length')
                if(x is None or y is None or x_length is None or y_length is None):
                        errors.append([st_stand.s_number, "missing x, y, x_length, y_length attributes"])
        #second - look for stands that occur twice in the data
        duplicates = stands.objects.filter(s_rx_event=rxe).values('s_number').annotate(count=models.Count('s_number')).filter(count__gt=1)
        for st_stand in duplicates:
                errors.append([st_stand.s_number, "In stand file " + str(st_stand.count) + " times."])
        if(len(errors) == 0):
                errors.append(['No errors found', ''])
        log_errors_to_file(str(rxe.re_name).replace(' ','_')+'_errors_stand_floorplan.csv', errors)
def load_error_report_stand_attributes(rxe):
        print(f"load_error_report_stand_attributes: {rxe}")
        errors = []
        #first - look for attributes that have a stand number that does not exist in the stands table
        for st_attr in stands_attribute_data.objects.filter(sad_event=rxe).order_by('sad_stand_name'):
                st_stand = stands.objects.filter(s_rx_event=rxe, s_number__iexact=st_attr.sad_stand_name.lower().strip())
                if(len(st_stand) == 0):
                        errors.append([st_attr.sa_number, "Stand number not found in stands table"])
        #second - look for stands that have no attribute data
        for st_stand in stands.objects.filter(s_rx_event=rxe).order_by('s_number'):
                st_attr = stand_attributes.objects.filter(sa_stand=st_stand)
                if(len(st_attr) == 0):
                        errors.append([st_stand.s_number, "Stand has no attributes"])
        if(len(errors) == 0):
                errors.append(['No errors found', ''])
        log_errors_to_file(str(rxe.re_name).replace(' ','_')+'_errors_stand_attributes.csv', errors)
def load_error_report_sales_data(rxe):
        print(f"load_error_report_stand_attributes: {rxe}")
        errors = []
        #first - look for sales data that have a stand number that does not exist in the stands table
        for s_trans in event_sales_transactions.objects.filter(est_event = rxe).order_by('est_Stand_Name_Cleaned'):
                if(s_trans.est_Stand_Name_Cleaned is not None):
                        st_stand = stands.objects.filter(s_rx_event=rxe, s_number__iexact=s_trans.est_Stand_Name_Cleaned.lower().strip())
                        if(len(st_stand) == 0):
                                errors.append([s_trans.est_Stand_Name_Cleaned, "Stand number not found in sales transaction table"])
                else:
                        errors.append(['None', "No stand number given in Sales Transaction Table"])
        #second - look for stand data in sales data multiple times
        duplicates = event_sales_transactions.objects.filter(est_event=rxe).values('est_Stand_Name_Cleaned').annotate(count=models.Count('est_Stand_Name_Cleaned')).filter(count__gt=1)
        for d in duplicates:
                errors.append([d['est_Stand_Name_Cleaned'], "In sales transaction file " + str(d['count']) + " times."])
        #third - look for stands with no sales data
        for st_stand in stands.objects.filter(s_rx_event=rxe).order_by('s_number'):
                st_attr = event_sales_transactions.objects.filter(est_event=rxe, est_Stand_Name_Cleaned=st_stand.s_number)
                if(len(st_attr) == 0):
                        errors.append([st_stand.s_number, "Stand has no sales data"])
        if(len(errors) == 0):
                errors.append(['No errors found', ''])
        log_errors_to_file(str(rxe.re_name).replace(' ','_')+'_errors_sales_transactions.csv', errors)

###Only if need to extract from sales transactions
def stand_attributes_temporary_extract_from_sales(rxe):
        missing = 0
        for st in stands.objects.filter(s_rx_event=rxe):
                est = event_sales_transactions.objects.filter(est_Stand_Name_Cleaned = st.s_number).order_by('est_Company_Name')[:1]
                if(len(est) == 0):
                        missing = missing + 1
                else:
                        for x in est:
#                                print(f"event_sales_transactions: {x.est_Stand_Name_Cleaned} {x.est_Company_Name} {x.est_Number_of_Corners} {x.est_Stand_Zone} {x.est_Floor_Plan_Sector}")
                                stand_attributes_record(st, None, 'Number of Corners', str(x.est_Number_of_Corners), 'integer', timezone.now())
                                stand_attributes_record(st, None, 'Stand Zone', str(x.est_Stand_Zone), 'string', timezone.now())
                                stand_attributes_record(st, None, 'Floor Plan Sector', str(x.est_Floor_Plan_Sector), 'string', timezone.now())
def write_stand_attributes_to_file(rxe):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'stand_attributes.csv')
        with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Stand Name', 'Title', 'Value', 'Data Type', 'Datetime'])
                for st in stands.objects.filter(s_rx_event=rxe):
                        sa = stand_attributes.objects.filter(sa_stand=st).order_by('sa_number')
                        for x in sa:
                                s_number = x.sa_number
                                s_title = x.sa_title
                                s_value = x.sa_value
                                s_type = x.sa_type
                                s_datetime = x.sa_datetime
                                st_data = [st.s_number, s_title, s_value, s_type, str(s_datetime)]
                                writer.writerow(st_data)
def create_stand_attributes_file_from_Sales_Data(rxe):
#this is a temporary effort to pull data from Sales Transactions - 
#fill need to shift csv file to excel file
        stand_attributes.objects.all().delete()
        stand_attributes_temporary_extract_from_sales(rxe)
        write_stand_attributes_to_file(rxe)
###Only if need to extract from sales transactions


def reset_test_data():
#        f.write("reset tables: " + str(timezone.now()) + "\n")
        rx_event.objects.all().delete()
        event_sales_transactions.objects.all().delete()
        event_sales_transactions_grouped.objects.all().delete()
        stands_attribute_data.objects.all().delete()
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

##        f = open(logs_filename, "w", encoding='utf-8')
##        f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
##        f.write("database_host_name: " + db_host_name + "\n")
##        f.write("database_name: " + db_name + "\n")

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
        event_determine_floorplan_max_length_height(rxe)

####        #Only do if need to recreate the stand attributes file
####        rxe = get_event('ISC West 2025')
####        create_stand_attributes_file_from_Sales_Data(rxe)

        filename = 'ISC_West25_stand_attributes.xlsx'
        rxe = get_event('ISC West 2025')
        load_stand_attribute_data(rxe, filename)

        load_error_report_stand(rxe)
        load_error_report_stand_attributes(rxe)
        load_error_report_sales_data(rxe)

#        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
#        f.close()

