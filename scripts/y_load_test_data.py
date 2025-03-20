#!/usr/bin/env python3

from django.utils import timezone
from django.contrib import messages
import os
from dotenv import load_dotenv
from django.conf import settings

from assn_mgr.models import *    
from club_mgr.models import *
from base.models import *
from tourneys.models import *
from scripts.x_helper_functions import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")


def populate_for_test(f, DEBUG_WRITE):
    record_log_data("y_load_test_data.py", "y_load_test_data_populate_for_test", "populate_for_test")

    if(1==1):  #Create associations

        try:
                associations.objects.get(assn_name='British Veterans Fencing')
        except:
                new_tourney = True
        else:
                new_tourney = False
        if new_tourney:
                next_assn_id = base_get_next_system_value('next_assn_id')
                asn = associations(assn_number=next_assn_id, assn_name='British Veterans Fencing', assn_status='active', 
                        assn_url='www.bvf.com', 
                        assn_phone='02076297200', assn_email='info@bvf.com', assn_description='old pokie, pokie')
                asn.save()
                association_ages(assn=asn, age_category='All Ages', age_category_description='All Ages').save()
                association_ages(assn=asn, age_category='Vet-40', age_category_description='Vet-40').save()
                association_ages(assn=asn, age_category='Vet-50', age_category_description='Vet-50').save()
                association_ages(assn=asn, age_category='Vet-60', age_category_description='Vet-60').save()
                association_ages(assn=asn, age_category='Vet-70', age_category_description='Vet-70').save()
                association_geographies(assn=asn, geo_category='Domestic', geo_category_description='Domestic').save()
                association_geographies(assn=asn, geo_category='International', geo_category_description='International').save()
                association_types(assn=asn, type_category='Individual', type_category_description='Individual').save()
                association_types(assn=asn, type_category='Team', type_category_description='Team').save()
                association_discipline(assn=asn, discipline_name='Foil', discipline_description='Weapon: Foil').save()
                association_discipline(assn=asn, discipline_name='Epee', discipline_description='Weapon: Epee').save()
                association_discipline(assn=asn, discipline_name='Sabre', discipline_description='Weapon: Sabre').save()
                association_genders(assn=asn, gender_name = "Men", gender_description = "Men").save()
                association_genders(assn=asn, gender_name = "Women", gender_description = "Women").save()
                association_genders(assn=asn, gender_name = "Mixed", gender_description = "Mixed").save()
                association_genders(assn=asn, gender_name = "Unknown", gender_description = "Unknown").save()

        if(1==1):  #Create Association Countries British Venterans
                asn = associations.objects.get(assn_name='British Veterans Fencing')

                association_countries.objects.create(assn=asn, country_three_letter='AFG', country_name='Afghanistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='ALB', country_name='Albania').save()
                association_countries.objects.create(assn=asn, country_three_letter='ALG', country_name='Algeria').save()
                association_countries.objects.create(assn=asn, country_three_letter='ASA', country_name='American Samoa').save()
                association_countries.objects.create(assn=asn, country_three_letter='AND', country_name='Andorra').save()
                association_countries.objects.create(assn=asn, country_three_letter='ANG', country_name='Angola').save()
                association_countries.objects.create(assn=asn, country_three_letter='ANT', country_name='Antigua & Barbuda').save()
                association_countries.objects.create(assn=asn, country_three_letter='ARG', country_name='Argentina').save()
                association_countries.objects.create(assn=asn, country_three_letter='ARM', country_name='Armenia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ARU', country_name='Aruba').save()
                association_countries.objects.create(assn=asn, country_three_letter='ART', country_name='Athlete Refugee Team').save()
                association_countries.objects.create(assn=asn, country_three_letter='ANZ', country_name='Australasia').save()
                association_countries.objects.create(assn=asn, country_three_letter='AUS', country_name='Australia').save()
                association_countries.objects.create(assn=asn, country_three_letter='AUT', country_name='Austria').save()
                association_countries.objects.create(assn=asn, country_three_letter='AZE', country_name='Azerbaijan').save()
                association_countries.objects.create(assn=asn, country_three_letter='BAH', country_name='Bahamas').save()
                association_countries.objects.create(assn=asn, country_three_letter='BRN', country_name='Bahrain').save()
                association_countries.objects.create(assn=asn, country_three_letter='BAN', country_name='Bangladesh').save()
                association_countries.objects.create(assn=asn, country_three_letter='BAR', country_name='Barbados').save()
                association_countries.objects.create(assn=asn, country_three_letter='BLR', country_name='Belarus').save()
                association_countries.objects.create(assn=asn, country_three_letter='BEL', country_name='Belgium').save()
                association_countries.objects.create(assn=asn, country_three_letter='BIZ', country_name='Belize').save()
                association_countries.objects.create(assn=asn, country_three_letter='BEN', country_name='Benin').save()
                association_countries.objects.create(assn=asn, country_three_letter='BER', country_name='Bermuda').save()
                association_countries.objects.create(assn=asn, country_three_letter='BHU', country_name='Bhutan').save()
                association_countries.objects.create(assn=asn, country_three_letter='BOH', country_name='Bohemia').save()
                association_countries.objects.create(assn=asn, country_three_letter='BOL', country_name='Bolivia').save()
                association_countries.objects.create(assn=asn, country_three_letter='BIH', country_name='Bosnia-Herzegovina').save()
                association_countries.objects.create(assn=asn, country_three_letter='BOT', country_name='Botswana').save()
                association_countries.objects.create(assn=asn, country_three_letter='BRA', country_name='Brazil').save()
                association_countries.objects.create(assn=asn, country_three_letter='IVB', country_name='British Virgin Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='BRU', country_name='Brunei').save()
                association_countries.objects.create(assn=asn, country_three_letter='BUL', country_name='Bulgaria').save()
                association_countries.objects.create(assn=asn, country_three_letter='BUR', country_name='Burkina Faso').save()
                association_countries.objects.create(assn=asn, country_three_letter='BDI', country_name='Burundi').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAM', country_name='Cambodia').save()
                association_countries.objects.create(assn=asn, country_three_letter='CMR', country_name='Cameroon').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAN', country_name='Canada').save()
                association_countries.objects.create(assn=asn, country_three_letter='CPV', country_name='Cape Verde').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAY', country_name='Cayman Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='CAF', country_name='Central African Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='CHA', country_name='Chad').save()
                association_countries.objects.create(assn=asn, country_three_letter='CHI', country_name='Chile').save()
                association_countries.objects.create(assn=asn, country_three_letter='CHN', country_name='China').save()
                association_countries.objects.create(assn=asn, country_three_letter='COL', country_name='Colombia').save()
                association_countries.objects.create(assn=asn, country_three_letter='COM', country_name='Comoros').save()
                association_countries.objects.create(assn=asn, country_three_letter='CGO', country_name='Congo-Brazzaville').save()
                association_countries.objects.create(assn=asn, country_three_letter='COK', country_name='Cook Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='CRC', country_name='Costa Rica').save()
                association_countries.objects.create(assn=asn, country_three_letter='CIV', country_name='Cote d Ivoire').save()
                association_countries.objects.create(assn=asn, country_three_letter='CRO', country_name='Croatia').save()
                association_countries.objects.create(assn=asn, country_three_letter='CUB', country_name='Cuba').save()
                association_countries.objects.create(assn=asn, country_three_letter='CYP', country_name='Cyprus').save()
                association_countries.objects.create(assn=asn, country_three_letter='CZE', country_name='Czech Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='TCH', country_name='Czechoslovakia').save()
                association_countries.objects.create(assn=asn, country_three_letter='COD', country_name='Democratic Republic of the Congo').save()
                association_countries.objects.create(assn=asn, country_three_letter='DEN', country_name='Denmark').save()
                association_countries.objects.create(assn=asn, country_three_letter='DJI', country_name='Djibouti').save()
                association_countries.objects.create(assn=asn, country_three_letter='DMA', country_name='Dominica').save()
                association_countries.objects.create(assn=asn, country_three_letter='DOM', country_name='Dominican Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='TLS', country_name='East Timor').save()
                association_countries.objects.create(assn=asn, country_three_letter='ECU', country_name='Ecuador').save()
                association_countries.objects.create(assn=asn, country_three_letter='EGY', country_name='Egypt').save()
                association_countries.objects.create(assn=asn, country_three_letter='ESA', country_name='El Salvador').save()
                association_countries.objects.create(assn=asn, country_three_letter='GEQ', country_name='Equatorial Guinea').save()
                association_countries.objects.create(assn=asn, country_three_letter='ERI', country_name='Eritrea').save()
                association_countries.objects.create(assn=asn, country_three_letter='EST', country_name='Estonia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SWZ', country_name='Eswatini').save()
                association_countries.objects.create(assn=asn, country_three_letter='ETH', country_name='Ethiopia').save()
                association_countries.objects.create(assn=asn, country_three_letter='FSM', country_name='Federal States of Micronesia').save()
                association_countries.objects.create(assn=asn, country_three_letter='FIJ', country_name='Fiji').save()
                association_countries.objects.create(assn=asn, country_three_letter='FIN', country_name='Finland').save()
                association_countries.objects.create(assn=asn, country_three_letter='FRA', country_name='France').save()
                association_countries.objects.create(assn=asn, country_three_letter='GAB', country_name='Gabon').save()
                association_countries.objects.create(assn=asn, country_three_letter='GAM', country_name='Gambia').save()
                association_countries.objects.create(assn=asn, country_three_letter='GEO', country_name='Georgia').save()
                association_countries.objects.create(assn=asn, country_three_letter='GDR', country_name='German Democratic Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='GER', country_name='Germany').save()
                association_countries.objects.create(assn=asn, country_three_letter='GHA', country_name='Ghana').save()
                association_countries.objects.create(assn=asn, country_three_letter='GBR', country_name='Great Britain').save()
                association_countries.objects.create(assn=asn, country_three_letter='GRE', country_name='Greece').save()
                association_countries.objects.create(assn=asn, country_three_letter='GRN', country_name='Grenada').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUM', country_name='Guam').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUA', country_name='Guatemala').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUI', country_name='Guinea').save()
                association_countries.objects.create(assn=asn, country_three_letter='GBS', country_name='Guinea Bissau').save()
                association_countries.objects.create(assn=asn, country_three_letter='GUY', country_name='Guyana').save()
                association_countries.objects.create(assn=asn, country_three_letter='HAI', country_name='Haiti').save()
                association_countries.objects.create(assn=asn, country_three_letter='HON', country_name='Honduras').save()
                association_countries.objects.create(assn=asn, country_three_letter='HKG', country_name='Hong Kong').save()
                association_countries.objects.create(assn=asn, country_three_letter='HUN', country_name='Hungary').save()
                association_countries.objects.create(assn=asn, country_three_letter='ISL', country_name='Iceland').save()
                association_countries.objects.create(assn=asn, country_three_letter='IOA', country_name='Independent Olympic Athletes').save()
                association_countries.objects.create(assn=asn, country_three_letter='IND', country_name='India').save()
                association_countries.objects.create(assn=asn, country_three_letter='INA', country_name='Indonesia').save()
                association_countries.objects.create(assn=asn, country_three_letter='IRI', country_name='Iran').save()
                association_countries.objects.create(assn=asn, country_three_letter='IRQ', country_name='Iraq').save()
                association_countries.objects.create(assn=asn, country_three_letter='IRL', country_name='Ireland').save()
                association_countries.objects.create(assn=asn, country_three_letter='ISR', country_name='Israel').save()
                association_countries.objects.create(assn=asn, country_three_letter='ITA', country_name='Italy').save()
                association_countries.objects.create(assn=asn, country_three_letter='JAM', country_name='Jamaica').save()
                association_countries.objects.create(assn=asn, country_three_letter='JPN', country_name='Japan').save()
                association_countries.objects.create(assn=asn, country_three_letter='JOR', country_name='Jordan').save()
                association_countries.objects.create(assn=asn, country_three_letter='KAZ', country_name='Kazakhstan').save()
                association_countries.objects.create(assn=asn, country_three_letter='KEN', country_name='Kenya').save()
                association_countries.objects.create(assn=asn, country_three_letter='KIR', country_name='Kiribati').save()
                association_countries.objects.create(assn=asn, country_three_letter='KOS', country_name='Kosovo').save()
                association_countries.objects.create(assn=asn, country_three_letter='KUW', country_name='Kuwait').save()
                association_countries.objects.create(assn=asn, country_three_letter='KGZ', country_name='Kyrgyzstan').save()
                association_countries.objects.create(assn=asn, country_three_letter='LAO', country_name='Laos').save()
                association_countries.objects.create(assn=asn, country_three_letter='LAT', country_name='Latvia').save()
                association_countries.objects.create(assn=asn, country_three_letter='LIB', country_name='Lebanon').save()
                association_countries.objects.create(assn=asn, country_three_letter='LES', country_name='Lesotho').save()
                association_countries.objects.create(assn=asn, country_three_letter='LBR', country_name='Liberia').save()
                association_countries.objects.create(assn=asn, country_three_letter='LBA', country_name='Libya').save()
                association_countries.objects.create(assn=asn, country_three_letter='LBA', country_name='Libya').save()
                association_countries.objects.create(assn=asn, country_three_letter='LIE', country_name='Liechtenstein').save()
                association_countries.objects.create(assn=asn, country_three_letter='LTU', country_name='Lithuania').save()
                association_countries.objects.create(assn=asn, country_three_letter='LUX', country_name='Luxembourg').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAD', country_name='Madagascar').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAW', country_name='Malawi').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAS', country_name='Malaysia').save()
                association_countries.objects.create(assn=asn, country_three_letter='MDV', country_name='Maldives').save()
                association_countries.objects.create(assn=asn, country_three_letter='MLI', country_name='Mali').save()
                association_countries.objects.create(assn=asn, country_three_letter='MLT', country_name='Malta').save()
                association_countries.objects.create(assn=asn, country_three_letter='MHL', country_name='Marshall Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='MTN', country_name='Mauritania').save()
                association_countries.objects.create(assn=asn, country_three_letter='MRI', country_name='Mauritius').save()
                association_countries.objects.create(assn=asn, country_three_letter='MEX', country_name='Mexico').save()
                association_countries.objects.create(assn=asn, country_three_letter='MDA', country_name='Moldova').save()
                association_countries.objects.create(assn=asn, country_three_letter='MON', country_name='Monaco').save()
                association_countries.objects.create(assn=asn, country_three_letter='MGL', country_name='Mongolia').save()
                association_countries.objects.create(assn=asn, country_three_letter='MNE', country_name='Montenegro').save()
                association_countries.objects.create(assn=asn, country_three_letter='MAR', country_name='Morocco').save()
                association_countries.objects.create(assn=asn, country_three_letter='MOZ', country_name='Mozambique').save()
                association_countries.objects.create(assn=asn, country_three_letter='MYA', country_name='Myanmar').save()
                association_countries.objects.create(assn=asn, country_three_letter='NAM', country_name='Namibia').save()
                association_countries.objects.create(assn=asn, country_three_letter='NRU', country_name='Nauru').save()
                association_countries.objects.create(assn=asn, country_three_letter='NEP', country_name='Nepal').save()
                association_countries.objects.create(assn=asn, country_three_letter='NED', country_name='Netherlands').save()
                association_countries.objects.create(assn=asn, country_three_letter='AHO', country_name='Netherlands Antilles').save()
                association_countries.objects.create(assn=asn, country_three_letter='NZL', country_name='New Zealand').save()
                association_countries.objects.create(assn=asn, country_three_letter='NCA', country_name='Nicaragua').save()
                association_countries.objects.create(assn=asn, country_three_letter='NIG', country_name='Niger').save()
                association_countries.objects.create(assn=asn, country_three_letter='NGR', country_name='Nigeria').save()
                association_countries.objects.create(assn=asn, country_three_letter='NBO', country_name='North Borneo').save()
                association_countries.objects.create(assn=asn, country_three_letter='PRK', country_name='North Korea').save()
                association_countries.objects.create(assn=asn, country_three_letter='MKD', country_name='North Macedonia').save()
                association_countries.objects.create(assn=asn, country_three_letter='YAR', country_name='North Yemen').save()
                association_countries.objects.create(assn=asn, country_three_letter='NOR', country_name='Norway').save()
                association_countries.objects.create(assn=asn, country_three_letter='OAR', country_name='Olympic Athletes from Russia').save()
                association_countries.objects.create(assn=asn, country_three_letter='OMA', country_name='Oman').save()
                association_countries.objects.create(assn=asn, country_three_letter='PAK', country_name='Pakistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='PLW', country_name='Palau').save()
                association_countries.objects.create(assn=asn, country_three_letter='PLE', country_name='Palestine').save()
                association_countries.objects.create(assn=asn, country_three_letter='PAN', country_name='Panama').save()
                association_countries.objects.create(assn=asn, country_three_letter='PNG', country_name='Papua New Guinea').save()
                association_countries.objects.create(assn=asn, country_three_letter='PAR', country_name='Paraguay').save()
                association_countries.objects.create(assn=asn, country_three_letter='PER', country_name='Peru').save()
                association_countries.objects.create(assn=asn, country_three_letter='PHI', country_name='Philippines').save()
                association_countries.objects.create(assn=asn, country_three_letter='POL', country_name='Poland').save()
                association_countries.objects.create(assn=asn, country_three_letter='POR', country_name='Portugal').save()
                association_countries.objects.create(assn=asn, country_three_letter='PUR', country_name='Puerto Rico').save()
                association_countries.objects.create(assn=asn, country_three_letter='QAT', country_name='Qatar').save()
                association_countries.objects.create(assn=asn, country_three_letter='ROU', country_name='Romania').save()
                association_countries.objects.create(assn=asn, country_three_letter='RUS', country_name='Russia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ROC', country_name='Russian Olympic Committee').save()
                association_countries.objects.create(assn=asn, country_three_letter='RWA', country_name='Rwanda').save()
                association_countries.objects.create(assn=asn, country_three_letter='SAA', country_name='Saar').save()
                association_countries.objects.create(assn=asn, country_three_letter='SKN', country_name='Saint Kitts and Nevis').save()
                association_countries.objects.create(assn=asn, country_three_letter='LCA', country_name='Saint Lucia').save()
                association_countries.objects.create(assn=asn, country_three_letter='VIN', country_name='Saint Vincent and Grenadines').save()
                association_countries.objects.create(assn=asn, country_three_letter='SAM', country_name='Samoa').save()
                association_countries.objects.create(assn=asn, country_three_letter='SMR', country_name='San Marino').save()
                association_countries.objects.create(assn=asn, country_three_letter='STP', country_name='Sao Tome and Principe').save()
                association_countries.objects.create(assn=asn, country_three_letter='KSA', country_name='Saudi Arabia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SEN', country_name='Senegal').save()
                association_countries.objects.create(assn=asn, country_three_letter='SRB', country_name='Serbia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SCG', country_name='Serbia and Montenegro').save()
                association_countries.objects.create(assn=asn, country_three_letter='SEY', country_name='Seychelles').save()
                association_countries.objects.create(assn=asn, country_three_letter='SLE', country_name='Sierra Leone').save()
                association_countries.objects.create(assn=asn, country_three_letter='SIN', country_name='Singapore').save()
                association_countries.objects.create(assn=asn, country_three_letter='SVK', country_name='Slovakia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SLO', country_name='Slovenia').save()
                association_countries.objects.create(assn=asn, country_three_letter='SOL', country_name='Solomon Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='SOM', country_name='Somalia').save()
                association_countries.objects.create(assn=asn, country_three_letter='RSA', country_name='South Africa').save()
                association_countries.objects.create(assn=asn, country_three_letter='KOR', country_name='South Korea').save()
                association_countries.objects.create(assn=asn, country_three_letter='SSD', country_name='South Sudan').save()
                association_countries.objects.create(assn=asn, country_three_letter='VNM', country_name='South Vietnam').save()
                association_countries.objects.create(assn=asn, country_three_letter='YMD', country_name='South Yemen').save()
                association_countries.objects.create(assn=asn, country_three_letter='URS', country_name='Soviet Union').save()
                association_countries.objects.create(assn=asn, country_three_letter='ESP', country_name='Spain').save()
                association_countries.objects.create(assn=asn, country_three_letter='SRI', country_name='Sri Lanka').save()
                association_countries.objects.create(assn=asn, country_three_letter='SUD', country_name='Sudan').save()
                association_countries.objects.create(assn=asn, country_three_letter='SUR', country_name='Suriname').save()
                association_countries.objects.create(assn=asn, country_three_letter='SWE', country_name='Sweden').save()
                association_countries.objects.create(assn=asn, country_three_letter='SUI', country_name='Switzerland').save()
                association_countries.objects.create(assn=asn, country_three_letter='SYR', country_name='Syria').save()
                association_countries.objects.create(assn=asn, country_three_letter='TPE', country_name='Taiwan').save()
                association_countries.objects.create(assn=asn, country_three_letter='TJK', country_name='Tajikistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='TAN', country_name='Tanzania').save()
                association_countries.objects.create(assn=asn, country_three_letter='ROT', country_name='Team of Refugee Olympic Athletes').save()
                association_countries.objects.create(assn=asn, country_three_letter='THA', country_name='Thailand').save()
                association_countries.objects.create(assn=asn, country_three_letter='TOG', country_name='Togo').save()
                association_countries.objects.create(assn=asn, country_three_letter='TGA', country_name='Tonga').save()
                association_countries.objects.create(assn=asn, country_three_letter='TTO', country_name='Trinidad and Tobago').save()
                association_countries.objects.create(assn=asn, country_three_letter='TUN', country_name='Tunisia').save()
                association_countries.objects.create(assn=asn, country_three_letter='TUR', country_name='Turkey').save()
                association_countries.objects.create(assn=asn, country_three_letter='TKM', country_name='Turkmenistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='TUV', country_name='Tuvalu').save()
                association_countries.objects.create(assn=asn, country_three_letter='UGA', country_name='Uganda').save()
                association_countries.objects.create(assn=asn, country_three_letter='UKR', country_name='Ukraine').save()
                association_countries.objects.create(assn=asn, country_three_letter='EUN', country_name='Unified Team').save()
                association_countries.objects.create(assn=asn, country_three_letter='UAE', country_name='United Arab Emirates').save()
                association_countries.objects.create(assn=asn, country_three_letter='UAR', country_name='United Arab Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='UAR', country_name='United Arab Republic').save()
                association_countries.objects.create(assn=asn, country_three_letter='USA', country_name='United States of America').save()
                association_countries.objects.create(assn=asn, country_three_letter='URU', country_name='Uruguay').save()
                association_countries.objects.create(assn=asn, country_three_letter='UZB', country_name='Uzbekistan').save()
                association_countries.objects.create(assn=asn, country_three_letter='VAN', country_name='Vanuatu').save()
                association_countries.objects.create(assn=asn, country_three_letter='VEN', country_name='Venezuela').save()
                association_countries.objects.create(assn=asn, country_three_letter='VIE', country_name='Vietnam').save()
                association_countries.objects.create(assn=asn, country_three_letter='ISV', country_name='Virgin Islands').save()
                association_countries.objects.create(assn=asn, country_three_letter='FRG', country_name='West Germany').save()
                association_countries.objects.create(assn=asn, country_three_letter='BWI', country_name='West Indies Federation').save()
                association_countries.objects.create(assn=asn, country_three_letter='YEM', country_name='Yemen').save()
                association_countries.objects.create(assn=asn, country_three_letter='YUG', country_name='Yugoslavia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ZAM', country_name='Zambia').save()
                association_countries.objects.create(assn=asn, country_three_letter='ZIM', country_name='Zimbabwe').save()

    if(1==1):  #Create Coach2 Club

        try:
               clubs.objects.get(club_name='Coach2 Club')
        except:
                asn = associations.objects.get(assn_name='British Veterans Fencing')
                next_club_id = base_get_next_system_value('next_club_id')
                tc = clubs(club_number=next_club_id, club_name='Coach2 Club', club_status='active',
                        club_address=None, club_url='www.blah.com', 
                        club_phone='0204563736', club_email='info@blah.com', club_description='fun, fun, fun')
                tc.save()
                ad = address(address_line_1='99 Devereux Road', address_city='Windsor', address_postcode='SL41JJ')
                ad.save()
                ta = club_address(club=tc, club_addr = ad)
                ta.save()
                taa = club_admins(club=tc, club_admin=User.objects.get(email='admin@gmail.com'))
                taa.save()
                taa = club_admins(club=tc, club_admin=User.objects.get(email='coach2@gmail.com'))
                taa.save()
                #Create Club Association
                club_assn.objects.create(club=tc, club_assn=asn)
        else:
                tc = clubs.objects.get(club_name='Coach2 Club')

        #Create Club disciplines based on association
        for x in association_discipline.objects.filter(assn=asn):
            club_disciplines.objects.create(club=tc, club_discipline_name=x.discipline_name, club_discipline_name_value=True)
        for y in association_ages.objects.filter(assn=asn):
            club_ages.objects.create(club=tc, club_age_name=y.age_category, club_age_value=True)


    if(1==0): #Create Tournament
        asn = associations.objects.get(assn_name='British Veterans Fencing')
        ts = tournament_status.objects.get(status__iexact='active')
        next_tournament_id = base_get_next_system_value('next_tournament_id')
        tt = tournaments(tourney_number=next_tournament_id, 
                        tourney_name='The Lansdowne Fencing Club Veterans Open',
                        tourney_assn=asn,
                        tourney_start_date=timezone.now(),
                        tourney_end_date=timezone.now(),
                        tourney_entry_close_date=timezone.now(),
                        tourney_url='www.lansdowneclub.com',
                        tourney_license='123456',
                        tourney_status=ts,
                        date_added=timezone.now(),
                        date_updated=timezone.now())        
        tt.save()
#        ta = venue_address(tourney=tt, venue_name='The Lansdowne Fencing Club', venue_address_line_1='9 Fitzmaurice Place', venue_address_city='London', venue_address_postcode='W1J 5JD')
#        ta.save()
        taa = tournament_admins(tourney=tt, tourney_admin=User.objects.get(email='admin@gmail.com'))
        taa.save()
        taa = tournament_admins(tourney=tt, tourney_admin=User.objects.get(email='brandon@gmail.com'))
        taa.save()
        for a in association_ages.objects.filter(assn=asn):
            tournament_ages.objects.create(tourney=tt, age_category=a.age_category, age_category_value=False)
        #create geographies based on assn
        g = association_geographies.objects.get(assn=asn, geo_category="Domestic")
        tournament_geography.objects.create(tourney=tt, geo_name=g)
        #create types based on assn
        for qq in association_types.objects.filter(assn=asn):
            tournament_types.objects.create(tourney=tt, tourney_type=qq.type_category, tourney_type_value=False)


def create_test_users(f, DEBUG_WRITE):
        f.write("\n\ncreate_test_users: " + str(timezone.now()) + "\n")

        if os.environ.get("DURHAM_PASSWORDS_USERS") is not None:
                passwd = str(os.environ.get("DURHAM_PASSWORDS_USERS"))
        else:
                passwd = None

        user, created = User.objects.get_or_create(email='paul@gmail.com', 
                                        defaults={'first_name': 'Paul', 'last_name': 'Abrahams', 
                                                'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()

        user, created = User.objects.get_or_create(email='brandon@gmail.com', 
                                        defaults={'first_name': 'Brandon', 'last_name': 'Brittain', 
                                                'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()

        user, created = User.objects.get_or_create(email='brittainuk@hotmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Brian', 
                                        'last_name': 'Brittain', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()

        user, created = User.objects.get_or_create(email='brian@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'BrianTest', 
                                        'last_name': 'Brittain', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='rachael@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Racheal', 
                                        'last_name': 'Lever', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='mom@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Mom', 
                                        'last_name': 'Parent', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='dad@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Dad', 
                                        'last_name': 'Parent', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='coach1@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Coach', 
                                        'last_name': 'One', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='coach2@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Coach', 
                                        'last_name': 'Two', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='fencer1@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Fencer', 
                                        'last_name': 'One', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='fencer2@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Fencer', 
                                        'last_name': 'Two', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='fencer3@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Fencer', 
                                        'last_name': 'Three', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='fencer4@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Fencer', 
                                        'last_name': 'Four', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()
        user, created = User.objects.get_or_create(email='emily@gmail.com', 
                                defaults={'password': 'Test1234!', 'first_name': 'Emily', 
                                        'last_name': 'BEARDMORE', 'is_staff': False, 'is_superuser': False})
        if created:
                user.set_password(passwd)
                user.save()


def run(*args):

        db_host_name = str(settings.DATABASES['default']['HOST'])
        db_name = str(settings.DATABASES['default']['NAME'])
        path_logs = os.path.join(settings.BASE_DIR, "logs/")
        path_input = os.path.join(settings.BASE_DIR, "scripts/")

        logs_filename = path_logs+db_name+"_"+os.path.splitext(os.path.basename(__file__))[0] + ".txt"
        f = open(logs_filename, "w", encoding='utf-8')
        f.write("Starting " + logs_filename + str(timezone.now()) + "\n")
        f.write("database_host_name: " + db_host_name + "\n")
        f.write("database_name: " + db_name + "\n")

        DEBUG_WRITE = True
        record_log_data("y_load_test_data.py", "load test data", "Load Test Data")
        create_test_users(f, DEBUG_WRITE)
        populate_for_test(f, DEBUG_WRITE)

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()
 
        #Email log file
#        send_attachment(fname)
#        os.remove(fname)


#python manage.py runscript y_load_test_data
