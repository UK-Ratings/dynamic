#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from integrations.models import *
from tourneys.models import *

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from django.db.models.functions import Length
from django.db.models import ForeignKey

from django.utils import timezone
from django.db.models import F
import os
import inspect
import re
from django.db import connection

from dotenv import load_dotenv
from django.conf import settings

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

def get_database_schema():
    """
    Get all tables from the PostgreSQL database and their attributes, including foreign key relationships.
    """
    schema_info = []

    with connection.cursor() as cursor:
        # Get the list of all tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            table_info = {
                'table_name': table_name,
                'columns': [],
                'foreign_keys': []
            }

            # Get the columns and their attributes
            cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table_name}'")
            columns = cursor.fetchall()
            for column in columns:
                column_info = {
                    'column_name': column[0],
                    'data_type': column[1],
                    'is_nullable': column[2]
                }
                table_info['columns'].append(column_info)

            # Get the foreign key relationships
            cursor.execute(f"""
                SELECT
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{table_name}';
            """)
            foreign_keys = cursor.fetchall()
            for fk in foreign_keys:
                fk_info = {
                    'column_name': fk[0],
                    'foreign_table_name': fk[1],
                    'foreign_column_name': fk[2]
                }
                table_info['foreign_keys'].append(fk_info)

            schema_info.append(table_info)

    return schema_info



def get_row_value(row, column_names, col_name):
        found_value = None

#        print('get_row_value')
        col_num = 0
#        print(row)
        for x in row:
#                print(column_names[col_num], x)
                qq = 0
                while qq < len(column_names):
                        if(column_names[qq] == col_name):
                                found_value = int(row[qq])
#                                print('found column name', column_names[qq], 'fk_id_vale',found_value)
                        qq = qq + 1

#        print('get_row_value--> found_value', found_value)
        return(found_value)        

def column_not_in_foreign_keys(column_name, foreign_keys):
        not_in = True
        for fk in foreign_keys:
                if(column_name == fk['column_name']):
#                        print(f"  - {fk['column_name']} references {fk['foreign_table_name']}({fk['foreign_column_name']})")
                        not_in = False

        return (not_in)


def print_all_data_in_table(f, schema_info, table, id_value):

        table_name = table['table_name']
#        table['foreign_keys']
        row_to_text = ''
        if(1==1):
#        if(table_name == 'tourneys_events'):
#                print(f"Table: {table_name}")

                with connection.cursor() as cursor:
                        # Fetch and print all data from the table
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        
                        # Fetch column names
                        column_names = [desc[0] for desc in cursor.description]

                        if rows:
#                                print("Data:")
#                                row_to_text = row_to_text + "\n\nTable named " + table_name.replace('_', ' ') + " has record: "
                                for row in rows:
                                        if(id_value is not None):
#                                                print('here')
                                                get_value = get_row_value(row, column_names, 'id')
                                                if(get_value == id_value):
#                                                        print('found the record')
                                                        row_to_text = "Table named '" + table_name.replace('_', ' ') + "' has record: "
                                                        col_num = 0
                                                        for x in row:
                                                                if(col_num > 0): #removes id
#                                                                        print(column_names[col_num], x)
                                                                        if(column_not_in_foreign_keys(column_names[col_num], table['foreign_keys'])):
                                                                                row_to_text = row_to_text \
                                                                                + str(column_names[col_num].replace('_', ' ')) \
                                                                                + " is " + str(x) + ", "
                                                                col_num = col_num + 1
                                        else:
#                                                row_to_text = row_to_text + "Table named " + table_name.replace('_', ' ') + " has record: "
                                                row_to_text = "Table named '" + table_name.replace('_', ' ') + "' has record: "
#                                                if(row[2] in ('Epee (72/91 Entries)', 'Harry')):
                                                if(1==1):
                                                        col_num = 0
        #                                                print(row)
                                                        for x in row:
                                                                if(col_num > 0): #removes id
#                                                                        print(column_names[col_num], x)
                                                                        if(column_not_in_foreign_keys(column_names[col_num], table['foreign_keys'])):
                                                                                row_to_text = row_to_text \
                                                                                        + str(column_names[col_num].replace('_', ' ')) \
                                                                                        + " is " + str(x) + ", "
                                                                col_num = col_num + 1
                                                        for fk in table['foreign_keys']:
#                                                                print(f"  - {fk['column_name']} references {fk['foreign_table_name']}({fk['foreign_column_name']})")
                                                                qq = 0
                                                                fk_id_value = get_row_value(row, column_names, fk['column_name'])
                                                                if(fk_id_value is None):
                                                                        print('Error:  Could not find fk_id')
                                                                else:
                                                                        for fk_table in schema_info:
                                                                                if(fk_table['table_name'] == fk['foreign_table_name']):
#                                                                                        print('found fk_table', fk_table['table_name'], fk_id_value)
                                                                                        fk_string = print_all_data_in_table(f, schema_info, fk_table, fk_id_value)
                                                                                        row_to_text = row_to_text \
                                                                                                + ' and record is a member of: (' \
                                                                                                + str(fk_string) + ')'
                                                row_to_text = row_to_text + "\n"
                                                f.write(row_to_text)
                        else:
                                print("No data found.")
#        print(row_to_text)
        return(row_to_text)

# Example usage
def print_database_schema(f, table_prefix):
        schema_info = get_database_schema()
        for table in schema_info:
#                if('assn_mgr' in table['table_name']
#                   or 'tourneys' in table['table_name']
#                   or 'club_mgr' in table['table_name']):
                if(table_prefix in table['table_name']):
#                if(1==1):
                        f.write(f"Table: {table['table_name']}\n")
#                        all_the_data = print_all_data_in_table(f,schema_info, table, None)



def run(*args):
        if(1==1): #basic setup
                db_host_name = str(settings.DATABASES['default']['HOST'])
                db_name = str(settings.DATABASES['default']['NAME'])
                path_logs = os.path.join(settings.BASE_DIR, "logs/")
                path_input = os.path.join(settings.BASE_DIR, "scripts/")

                load_dotenv()  #must have to access .env file values

        table_space = 'club_mgr'
        logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + "__"+table_space+".txt"
        f = open(logs_filename, "w", encoding='utf-8')
        print_database_schema(f, table_space)
        f.close()

        table_space = 'tourneys'
        logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + "__"+table_space+".txt"
        f = open(logs_filename, "w", encoding='utf-8')
        print_database_schema(f, table_space)
        f.close()

        table_space = 'assn_mgr'
        logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + "__"+table_space+".txt"
        f = open(logs_filename, "w", encoding='utf-8')
        print_database_schema(f, table_space)
        f.close()


# python manage.py runscript llm_data

