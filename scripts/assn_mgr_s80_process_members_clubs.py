#!/usr/bin/env python3

from assn_mgr.models import *
from users.models import User

from scripts.x_helper_functions import *
from scripts.x_helper_assn_specific import *
from scripts.y_reset_system import *

from django.utils import timezone
import os
from dotenv import load_dotenv
from django.conf import settings
from django.db import transaction


#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

# python manage.py runscript assn_mgr_s80_process_members_clubs

def add_association_countries_BF(f, association_name, DEBUG_WRITE):
        asn = get_association(f, association_name, DEBUG_WRITE)
        if(DEBUG_WRITE):  #association_countries
                f.write("      Working on association_countries data: " + str(asn.assn_name) + "\n")

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
def get_or_build_association_BF(f, association_name, DEBUG_WRITE):
        f.write("\nget_or_build_association_BritishFencing: " + str(timezone.now()) + "\n")

        asn = get_association(f, association_name, DEBUG_WRITE)
        if(asn is None):
                if(DEBUG_WRITE):  #association_ages
                        f.write("      Association does not exist: " + str(association_name) + "\n")
                next_assn_id = base_get_next_system_value('next_assn_id')
                asn = associations(assn_number=next_assn_id, assn_name=association_name, assn_status='active', 
                        assn_url='www.britishfencing.com', assn_phone='02076297200', 
                        assn_email='info@britishfencing.com', assn_description='pokie, pokie')
                asn.save()
                if(DEBUG_WRITE):
                        f.write("      Added Association: " + str(asn) + " " + str(asn.assn_number) + " " + str(asn.assn_name) + "\n")

                if(1==1): # load association data  in if to compress statements
                        add_association_countries_BF(f, association_name, DEBUG_WRITE)

                        if(DEBUG_WRITE):  #association_ages
                                f.write("      Working on association age data: " + str(asn.assn_name) + "\n")
                        association_ages.objects.filter(assn=asn).delete()
                        association_ages(assn=asn, age_category='all_ages', age_category_description='All Ages').save()
                        association_ages(assn=asn, age_category='Under 5', age_category_description='Under 5').save()
                        association_ages(assn=asn, age_category='Under 6', age_category_description='Under 6').save()
                        association_ages(assn=asn, age_category='Under 7', age_category_description='Under 7').save()
                        association_ages(assn=asn, age_category='Under 8', age_category_description='Under 8').save()
                        association_ages(assn=asn, age_category='Under 9', age_category_description='Under 9').save()
                        association_ages(assn=asn, age_category='Under 10', age_category_description='Under 10').save()
                        association_ages(assn=asn, age_category='Under 11', age_category_description='Under 11').save()
                        association_ages(assn=asn, age_category='Under 12', age_category_description='Under 12').save()
                        association_ages(assn=asn, age_category='Under 13', age_category_description='Under 13').save()
                        association_ages(assn=asn, age_category='Under 14', age_category_description='Under 14').save()
                        association_ages(assn=asn, age_category='Under 15', age_category_description='Under 15').save()
                        association_ages(assn=asn, age_category='Under 16', age_category_description='Under 16').save()
                        association_ages(assn=asn, age_category='Under 17', age_category_description='Under 17').save()
                        association_ages(assn=asn, age_category='Under 18', age_category_description='Under 18').save()
                        association_ages(assn=asn, age_category='Under 19', age_category_description='Under 19').save()
                        association_ages(assn=asn, age_category='Under 20', age_category_description='Under 20').save()
                        association_ages(assn=asn, age_category='Under 21', age_category_description='Under 21').save()
                        association_ages(assn=asn, age_category='Under 22', age_category_description='Under 22').save()
                        association_ages(assn=asn, age_category='Under 23', age_category_description='Under 23').save()
                        association_ages(assn=asn, age_category='U5', age_category_description='Under 5').save()
                        association_ages(assn=asn, age_category='U6', age_category_description='Under 6').save()
                        association_ages(assn=asn, age_category='U7', age_category_description='Under 7').save()
                        association_ages(assn=asn, age_category='U8', age_category_description='Under 8').save()
                        association_ages(assn=asn, age_category='U9', age_category_description='Under 9').save()
                        association_ages(assn=asn, age_category='U10', age_category_description='Under 10').save()
                        association_ages(assn=asn, age_category='U11', age_category_description='Under 11').save()
                        association_ages(assn=asn, age_category='U12', age_category_description='Under 12').save()
                        association_ages(assn=asn, age_category='U13', age_category_description='Under 13').save()
                        association_ages(assn=asn, age_category='U14', age_category_description='Under 14').save()
                        association_ages(assn=asn, age_category='U15', age_category_description='Under 15').save()
                        association_ages(assn=asn, age_category='U16', age_category_description='Under 16').save()
                        association_ages(assn=asn, age_category='U17', age_category_description='Under 17').save()
                        association_ages(assn=asn, age_category='U18', age_category_description='Under 18').save()
                        association_ages(assn=asn, age_category='U19', age_category_description='Under 19').save()
                        association_ages(assn=asn, age_category='U20', age_category_description='Under 20').save()
                        association_ages(assn=asn, age_category='U21', age_category_description='Under 21').save()
                        association_ages(assn=asn, age_category='U22', age_category_description='Under 22').save()
                        association_ages(assn=asn, age_category='U23', age_category_description='Under 23').save()
                        association_ages(assn=asn, age_category='Cadet', age_category_description='Cadet').save()
                        association_ages(assn=asn, age_category='Junior', age_category_description='Junior').save()
                        association_ages(assn=asn, age_category='Senior', age_category_description='Senior').save()
                        association_ages(assn=asn, age_category='Veteran', age_category_description='Veteran').save()
                        association_ages(assn=asn, age_category='U-5', age_category_description='Under 5').save()
                        association_ages(assn=asn, age_category='U-6', age_category_description='Under 6').save()
                        association_ages(assn=asn, age_category='U-7', age_category_description='Under 7').save()
                        association_ages(assn=asn, age_category='U-8', age_category_description='Under 8').save()
                        association_ages(assn=asn, age_category='U-9', age_category_description='Under 9').save()
                        association_ages(assn=asn, age_category='U-10', age_category_description='Under 10').save()
                        association_ages(assn=asn, age_category='U-11', age_category_description='Under 11').save()
                        association_ages(assn=asn, age_category='U-12', age_category_description='Under 12').save()
                        association_ages(assn=asn, age_category='U-13', age_category_description='Under 13').save()
                        association_ages(assn=asn, age_category='U-14', age_category_description='Under 14').save()
                        association_ages(assn=asn, age_category='U-15', age_category_description='Under 15').save()
                        association_ages(assn=asn, age_category='U-16', age_category_description='Under 16').save()
                        association_ages(assn=asn, age_category='U-17', age_category_description='Under 17').save()
                        association_ages(assn=asn, age_category='U-18', age_category_description='Under 18').save()
                        association_ages(assn=asn, age_category='U-19', age_category_description='Under 19').save()
                        association_ages(assn=asn, age_category='U-20', age_category_description='Under 20').save()
                        association_ages(assn=asn, age_category='U-21', age_category_description='Under 21').save()
                        association_ages(assn=asn, age_category='U-22', age_category_description='Under 22').save()
                        association_ages(assn=asn, age_category='U-23', age_category_description='Under 23').save()
                        association_ages(assn=asn, age_category='Unknown', age_category_description='Unknown').save()
                        if(DEBUG_WRITE):  #association_geographies
                                f.write("      Working on association_geographies data: " + str(asn.assn_name) + "\n")
                        association_geographies.objects.filter(assn=asn).delete()
                        association_geographies(assn=asn, geo_category='Domestic', geo_category_description='Domestic').save()
                        association_geographies(assn=asn, geo_category='International', geo_category_description='International').save()
                        association_geographies(assn=asn, geo_category='Unknown', geo_category_description='Unknown').save()
                        if(DEBUG_WRITE):  #association_types
                                f.write("      Working on association_types data: " + str(asn.assn_name) + "\n")
                        association_types.objects.filter(assn=asn).delete()
                        association_types(assn=asn, type_category='Individual', type_category_description='Individual').save()
                        association_types(assn=asn, type_category='Team', type_category_description='Team').save()
                        association_types(assn=asn, type_category='Unknown', type_category_description='Unknown').save()

                        if(DEBUG_WRITE):  #association_genders
                                f.write("      Working on association_genders data: " + str(asn.assn_name) + "\n")
                        association_genders.objects.filter(assn=asn).delete()
                        association_genders(assn=asn, gender_name='Men', gender_description='Men').save()
                        association_genders(assn=asn, gender_name='Women', gender_description='Women').save()
                        association_genders(assn=asn, gender_name='Mixed', gender_description='Mixed').save()
                        association_genders(assn=asn, gender_name='Unknown', gender_description='Unknown').save()


                        if(DEBUG_WRITE):  #association_discipline
                                f.write("      Working on association_tournament_extra_fields data: " + str(asn.assn_name) + "\n")
                        association_tournament_extra_fields.objects.filter(assn=asn).delete()
                        association_discipline(assn=asn, discipline_name='Foil', discipline_description='Weapon: Foil').save()
                        association_discipline(assn=asn, discipline_name='Epee', discipline_description='Weapon: Epee').save()
                        association_discipline(assn=asn, discipline_name='Sabre', discipline_description='Weapon: Sabre').save()
                        association_discipline(assn=asn, discipline_name='Unknown', discipline_description='Weapon: Unknown').save()

                        if(DEBUG_WRITE):  #association_event_extra_fields
                                f.write("      Working on association_event_extra_fields data: " + str(asn.assn_name) + "\n")
                        association_event_extra_fields.objects.filter(assn=asn).delete()
                        association_event_extra_fields(assn = asn,field_sequence = 10,
                                field_name = 'ev_ranking_points', field_type = 'boolean', field_value = 'True',
                                field_group = 'ev_ranking_points', field_active = True).save()
                        association_event_extra_fields(assn = asn,field_sequence = 20,
                                field_name = 'ev_number_of_fencers', field_type = 'int', field_value = '0',
                                field_group = 'ev_number_of_fencers', field_active = True).save()
                        association_event_extra_fields(assn = asn,field_sequence = 30,
                                field_name = 'ev_nif', field_type = 'int', field_value = '0',
                                field_group = 'ev_nif', field_active = True).save()
                        association_event_extra_fields(assn = asn,field_sequence = 40,
                                field_name = 'ev_potential_rating', field_type = 'string', field_value = '',
                                field_group = 'ev_potential_rating', field_active = True).save()
                        association_event_extra_fields(assn = asn,field_sequence = 50,
                                field_name = 'ev_final_rating', field_type = 'string', field_value = '',
                                field_group = 'ev_final_rating', field_active = True).save()
                        association_event_extra_fields(assn = asn,field_sequence = 60,
                                field_name = 'ev_potential_nif', field_type = 'int', field_value = '0',
                                field_group = 'ev_potential_nif', field_active = True).save()

                        if(DEBUG_WRITE):  #association_event_extra_fields
                                f.write("      Working on association_event_final_results_extra_fields data: " + str(asn.assn_name) + "\n")
                        association_event_final_results_extra_fields.objects.filter(assn=asn).delete()
                        association_event_final_results_extra_fields(assn = asn,field_sequence = 10,
                                field_name = 'efr_final_points', field_type = 'int', field_value = '0',
                                field_group = 'efr_final_points', field_active = True).save()
                        association_event_final_results_extra_fields(assn = asn,field_sequence = 20,
                                field_name = 'efr_previous_rating', field_type = 'string', field_value = '',
                                field_group = 'efr_previous_rating', field_active = True).save()
                        association_event_final_results_extra_fields(assn = asn,field_sequence = 30,
                                field_name = 'efr_rating', field_type = 'string', field_value = '',
                                field_group = 'efr_rating', field_active = True).save()
                        association_event_final_results_extra_fields(assn = asn,field_sequence = 40,
                                field_name = 'efr_award_date', field_type = 'datetime', field_value = '',
                                field_group = 'efr_award_date', field_active = True).save()

#    efr_final_points = models.BigIntegerField("BF Results Final Points", blank=True, null=True)
#    efr_previous_rating = models.CharField("Rating", max_length=3, blank=True, null=True)
#    efr_rating = models.CharField("Rating", max_length=3, blank=True, null=True)
#    efr_award_date = models.DateTimeField("Rating Awarded Date", blank=True, null=True)


        if(DEBUG_WRITE):
                f.write("   Returning Association: " + str(asn) + " " + str(asn.assn_name) + "\n")

def zzzupdate_or_create_association_club_BF(f, cl, asn, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      get_update_or_create_association_club_BF: " + str(asn.assn_name) + " " + str(cl.name) + " " + str(timezone.now()) + "\n")

        found_club_new = False
        try:  #does club exist.  If not create it
                association_clubs.objects.get(assn_club_name = cl.name, assn = asn)
        except:
                next_club_id = base_get_next_system_value('next_assn_club_id')
                if(DEBUG_WRITE):
                        f.write("         Club does not exist: " + str(cl.name) + " next_club_id = " + str(next_club_id) + "\n")
                found_club = association_clubs(
                        assn_club_number = next_club_id, 
                        assn = asn,
                        assn_club_name = cl.name,
                        assn_club_url = cl.img_url,
                        assn_club_status = cl.valid,
                        assn_club_phone = cl.phone,
                        assn_club_email = cl.email,
                        assn_club_description = ""
                        )
                found_club.save()
                found_club_new = True
        else:
                if(DEBUG_WRITE):
                        f.write("         Club exists... Updating: " + str(cl.name) + "\n")
                fc = association_clubs.objects.get(assn_club_name = cl.name, assn = asn)

                found_club, created = association_clubs.objects.update_or_create(
                        assn = fc.assn, 
                        assn_club_number = fc.assn_club_number, 
                                defaults={                                        
                                        'assn_club_name' : cl.name,
                                        'assn_club_url' : cl.img_url,
                                        'assn_club_status' : cl.valid,
                                        'assn_club_phone' : cl.phone,
                                        'assn_club_email' : cl.email,
                                        'assn_club_description' : ""})

        if(DEBUG_WRITE):
                f.write("      returning get_update_or_create_association_club_BF: " + str(found_club) + " " + str(found_club.assn_club_number) + " " + str(found_club.assn_club_name) + "\n")
        return(found_club, found_club_new)
def zzzget_update_or_create_association_club_extra_fields_BF(f, cl, found_club, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      get_update_or_create_association_club_extra_fields_BF: " + str(cl.name) + " " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")

        try:  #does club exist.  If not create it
                association_clubs.objects.get(id = found_club.id)
        except:
                if(DEBUG_WRITE):
                        f.write("         Club does not exist: "  + " " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("         Club exists " + str(cl.name) + " " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 10, 
                                defaults={'assn_club_field_name': 'uuid_s80','assn_club_field_type': 'string',
                                'assn_club_field_value': cl.uuid_s80,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 20, 
                                defaults={'assn_club_field_name': 'contact_uuid_s80','assn_club_field_type': 'string',
                                'assn_club_field_value': cl.contact_uuid_s80,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 30, 
                                defaults={'assn_club_field_name': 'add_on_type_uuid_s80','assn_club_field_type': 'string',
                                'assn_club_field_value': cl.add_on_type_uuid_s80,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 40, 
                                defaults={'assn_club_field_name': 'assn_add_on_type_name','assn_club_field_type': 'string',
                                'assn_club_field_value': cl.add_on_type_name,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 50, 
                                defaults={'assn_club_field_name': 'add_on_region','assn_club_field_type': 'string',
                                'assn_club_field_value': cl.add_on_region,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 60, 
                                defaults={'assn_club_field_name': 'add_on_region_org_uuid_s80','assn_club_field_type': 'string',
                                'assn_club_field_value': cl.add_on_region_org_uuid_s80,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 70, 
                                defaults={'assn_club_field_name': 'joined_date','assn_club_field_type': 'datetime',
                                'assn_club_field_value': cl.joined_date,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 80, 
                                defaults={'assn_club_field_name': 'start_date','assn_club_field_type': 'datetime',
                                'assn_club_field_value': cl.start_date,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 90, 
                                defaults={'assn_club_field_name': 'exp_date','assn_club_field_type': 'datetime',
                                'assn_club_field_value': cl.exp_date,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 100, 
                                defaults={'assn_club_field_name': 'valid','assn_club_field_type': 'boolean',
                                'assn_club_field_value': cl.valid,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
                association_club_extra_fields.objects.update_or_create(assn_club=found_club, assn_club_field_sequence = 110, 
                                defaults={'assn_club_field_name': 'suspended','assn_club_field_type': 'boolean',
                                'assn_club_field_value': cl.suspended,
                                'assn_club_field_group': 's80_club_records','assn_club_field_active': True})
def zzzload_or_update_association_clubs_BF(f, association_name, DEBUG_WRITE):
        f.write("\nload_or_update_association_clubs_BF: " + str(association_name) + " " + str(timezone.now()) + "\n")

        asn = get_association(f, association_name, DEBUG_WRITE)
        if(asn is not None):
                for cl in s80_club_records.objects.all():
                        if(DEBUG_WRITE):
                                f.write("   Club: " + str(cl.name) + " " 
                                        + str(cl.primary_address_line1) + " "
                                        + str(cl.primary_address_postal_code) + "\n")
                        found_club, found_club_new = update_or_create_association_club_BF(f, cl, asn, DEBUG_WRITE)
                        found_address = update_or_create_address(f, DEBUG_WRITE, "", cl.primary_address_line1, 
                                            cl.primary_address_line2, cl.primary_address_line3, 
                                            cl.primary_address_city, cl.primary_address_region, 
                                            cl.primary_address_region_abbr, cl.primary_address_postal_code, 
                                            "", cl.primary_address_country)
                        found_club_address, created = association_club_address.objects.update_or_create(assn_club=found_club, assn_club_addr = found_address)
                        get_update_or_create_association_club_extra_fields_BF(f, cl, found_club, DEBUG_WRITE)
                        if(found_club_new):
                                initial_association_club_values_from_association(f, found_club, asn, DEBUG_WRITE)
                                get_update_or_create_association_club_admin_BF(f, found_club, DEBUG_WRITE)
def zzzget_association_club_BF(f, cl_name, asn, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      get_association_club_BF: " + str(cl_name) + " " + str(timezone.now()) + "\n")

        try:  #does club exist.  If not create it
                association_clubs.objects.get(assn_club_name = cl_name, assn = asn)
        except:
                if(DEBUG_WRITE):
                        f.write("         WARNING!!! Club does not exist: " + str(cl_name) + "\n")
                        found_club = None
        else:
                if(DEBUG_WRITE):
                        f.write("         Club exists... : " + str(cl_name) + "\n")
                found_club = association_clubs.objects.get(assn_club_name = cl_name, assn = asn)
                                                           
        if(found_club is not None and DEBUG_WRITE):
                f.write("      returning get_association_club_BF: " + str(found_club) + " " + str(found_club.assn_club_number) + " " + str(found_club.assn_club_name) + "\n")
        return(found_club)
def zzzget_update_or_create_association_member_BF(f, mr, asn, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      get_update_or_create_association_member_BF: " 
                        + " identity number: " + str(mr.identity_number) + " "
                        + str(mr.first_name) + " " + str(mr.last_name) + " " + str(timezone.now()) + "\n")
        found_member_new = False
        try:  #does association_members exist.  If not create it
                association_members.objects.get(assn = asn, assn_member_identifier = mr.identity_number)
        except:
                if(DEBUG_WRITE):
                        f.write("         Association Member does not exist: " + str(mr.identity_number) + " " + str(mr.first_name) + " " + str(mr.last_name) + "\n")
                next_assn_member_id = base_get_next_system_value('next_assn_member_id')
                if(DEBUG_WRITE):
                        f.write("         next_assn_member_id = " + str(next_assn_member_id) + "\n")
                found_member = association_members(
                        assn_member_number = next_assn_member_id,
                        assn = asn,
                        assn_member_identifier = mr.identity_number,
                        assn_member_first_name = mr.first_name.title(),
                        assn_member_last_name = mr.last_name.upper(),
                        assn_member_full_name = mr.last_name.upper() + " " + mr.first_name.title(),
                        assn_member_dob = mr.dob,
                        assn_member_gender = mr.gender,
                        assn_member_joined_date = mr.joined_date,
                        assn_member_start_date = mr.start_date,
                        assn_member_exp_date = mr.exp_date,
                        assn_member_email = mr.email,
                        assn_member_phone = mr.phone,
                        assn_member_img_url = mr.img_url,
                        assn_member_valid = mr.valid,
                        assn_member_suspended = mr.suspended
                        )
                found_member.save()
                found_member_new = True
        else:
                fm = association_members.objects.get(assn = asn, assn_member_identifier = mr.identity_number)

                if(DEBUG_WRITE):
                        f.write("         Association Member does exist: " 
                                + " assn_member_identifier: " + str(fm.assn_member_identifier) + " " 
                                + str(fm.assn_member_first_name) + " " 
                                + str(fm.assn_member_last_name) + " " 
                                + " assn_member_number: " + str(fm.assn_member_number) + "\n")
                found_member, created = association_members.objects.update_or_create(
                        assn = fm.assn, 
                        assn_member_identifier = fm.assn_member_identifier, 
                                defaults={                                        
                                        'assn_member_identifier' : mr.identity_number,
                                        'assn_member_first_name' : mr.first_name.title(),
                                        'assn_member_last_name' : mr.last_name.upper(),
                                        'assn_member_full_name' : mr.last_name.upper() + " " + mr.first_name.title(),
                                        'assn_member_dob' : mr.dob,
                                        'assn_member_gender' : mr.gender,
                                        'assn_member_joined_date' : mr.joined_date,
                                        'assn_member_start_date' : mr.start_date,
                                        'assn_member_exp_date' : mr.exp_date,
                                        'assn_member_email' : mr.email,
                                        'assn_member_phone' : mr.phone,
                                        'assn_member_img_url' : mr.img_url,
                                        'assn_member_valid' : mr.valid,
                                        'assn_member_suspended' : mr.suspended})

        if(DEBUG_WRITE):
                f.write("       returning get_update_or_create_association_member_BF: " + str(found_member.assn_member_identifier) + " " + str(found_member.assn_member_first_name) + " " + str(found_member.assn_member_last_name) + "\n")
        return(found_member, found_member_new)
def zzzget_update_or_create_association_members_extra_fields_BF(f, mr, found_member, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      get_update_or_create_association_members_extra_fields_BF: " + str(mr.last_name) + " " + str(found_member.assn_member_full_name) + " " + str(timezone.now()) + "\n")

        try:  #does club exist.  If not create it
                association_members.objects.get(id = found_member.id)
        except:
                if(DEBUG_WRITE):
                        f.write("         Member does not exist: "  + " " + str(found_member.assn_member_full_name) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("         Member exists " + str(mr.last_name) + " " + str(found_member.assn_member_full_name) + " " + str(timezone.now()) + "\n")

                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 10, 
                                defaults={'assn_member_field_name': 'uuid_s80','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.uuid_s80,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 20, 
                                defaults={'assn_member_field_name': 'contact_uuid_s80','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.contact_uuid_s80,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 30, 
                                defaults={'assn_member_field_name': 'add_on_uuid_s80','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.add_on_uuid_s80,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 40, 
                                defaults={'assn_member_field_name': 'add_on_name','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.add_on_name,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 50, 
                                defaults={'assn_member_field_name': 'add_on_type_uuid_s80','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.add_on_type_uuid_s80,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 60, 
                                defaults={'assn_member_field_name': 'add_on_type_name','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.add_on_type_name,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 70, 
                                defaults={'assn_member_field_name': 'add_on_region','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.add_on_region,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
                association_member_extra_fields.objects.update_or_create(assn_member=found_member, 
                                                                         assn_member_field_sequence = 80, 
                                defaults={'assn_member_field_name': 'add_on_region_org_uuid_s80','assn_member_field1_type': 'string',
                                'assn_member_field1_value': mr.add_on_region_org_uuid_s80,
                                'assn_member_field_group': 's80_member_records','assn_member_field_active': True})
def zzzload_or_update_association_members_BF(f, association_name, DEBUG_WRITE):
        f.write("\nload_or_update_association_members_BF: " + str(association_name) + " " + str(timezone.now()) + "\n")

        asn = get_association(f, association_name, DEBUG_WRITE)

        if(asn is not None):
                for mr in s80_membership_records.objects.all():
#                        if(DEBUG_WRITE):
                        f.write("   Member: " + str(mr.first_name) + " " + str(mr.last_name) + " " + str(mr.identity_number) + " " + str(timezone.now()) + "\n")
                        found_member, found_member_new = get_update_or_create_association_member_BF(f, mr, asn, DEBUG_WRITE)
                        get_update_or_create_association_members_extra_fields_BF(f, mr, found_member, DEBUG_WRITE)
                        found_address = update_or_create_address(f, DEBUG_WRITE, "", mr.primary_address_line1, 
                                            mr.primary_address_line2, mr.primary_address_line3, 
                                            mr.primary_address_city, mr.primary_address_region, 
                                            mr.primary_address_region_abbr, mr.primary_address_postal_code, 
                                            "", mr.primary_address_country)
                        found_club_address, created = association_member_address.objects.update_or_create(
                                assn_member=found_member, association_member_addr = found_address)

                        club_record = s80_membership_records_clubs.objects.filter(membership_uuid=mr).first()
                        found_club = get_association_club_BF(f, club_record.add_on_clubs_name, asn, DEBUG_WRITE)
                        if found_club is not None:
                                found_club_member, created = association_club_members.objects.update_or_create(
                                        assn_club=found_club, assn_club_members=found_member)

def update_or_create_association_club_BF(f, cl, asn, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      get_update_or_create_association_club_BF: " + str(asn.assn_name) + " " + str(cl.name) + " " + str(timezone.now()) + "\n")

    found_club_new = False

    with transaction.atomic():
        try:
            # Check if the club exists
            found_club = association_clubs.objects.get(assn_club_name=cl.name, assn=asn)
            if DEBUG_WRITE:
                f.write("         Club exists... Updating: " + str(cl.name) + "\n")
            found_club.assn_club_url = cl.img_url
            found_club.assn_club_status = cl.valid
            found_club.assn_club_phone = cl.phone
            found_club.assn_club_email = cl.email
            found_club.assn_club_description = ""
            found_club.save()
        except association_clubs.DoesNotExist:
            next_club_id = base_get_next_system_value('next_assn_club_id')
            if DEBUG_WRITE:
                f.write("         Club does not exist: " + str(cl.name) + " next_club_id = " + str(next_club_id) + "\n")
            found_club = association_clubs(
                assn_club_number=next_club_id,
                assn=asn,
                assn_club_name=cl.name,
                assn_club_url=cl.img_url,
                assn_club_status=cl.valid,
                assn_club_phone=cl.phone,
                assn_club_email=cl.email,
                assn_club_description=""
            )
            found_club.save()
            found_club_new = True

    if DEBUG_WRITE:
        f.write("      returning get_update_or_create_association_club_BF: " + str(found_club) + " " + str(found_club.assn_club_number) + " " + str(found_club.assn_club_name) + "\n")
    return found_club, found_club_new
def get_update_or_create_association_club_extra_fields_BF(f, cl, found_club, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      get_update_or_create_association_club_extra_fields_BF: " + str(cl.name) + " " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")

    with transaction.atomic():
        try:
            # Check if the club exists
            association_clubs.objects.get(id=found_club.id)
        except association_clubs.DoesNotExist:
            if DEBUG_WRITE:
                f.write("         Club does not exist: " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")
        else:
            if DEBUG_WRITE:
                f.write("         Club exists " + str(cl.name) + " " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")

            extra_fields = [
                {'sequence': 10, 'name': 'uuid_s80', 'type': 'string', 'value': cl.uuid_s80},
                {'sequence': 20, 'name': 'contact_uuid_s80', 'type': 'string', 'value': cl.contact_uuid_s80},
                {'sequence': 30, 'name': 'add_on_type_uuid_s80', 'type': 'string', 'value': cl.add_on_type_uuid_s80},
                {'sequence': 40, 'name': 'assn_add_on_type_name', 'type': 'string', 'value': cl.add_on_type_name},
                {'sequence': 50, 'name': 'add_on_region', 'type': 'string', 'value': cl.add_on_region},
                {'sequence': 60, 'name': 'add_on_region_org_uuid_s80', 'type': 'string', 'value': cl.add_on_region_org_uuid_s80},
                {'sequence': 70, 'name': 'joined_date', 'type': 'datetime', 'value': cl.joined_date},
                {'sequence': 80, 'name': 'start_date', 'type': 'datetime', 'value': cl.start_date},
                {'sequence': 90, 'name': 'exp_date', 'type': 'datetime', 'value': cl.exp_date},
                {'sequence': 100, 'name': 'valid', 'type': 'boolean', 'value': cl.valid},
                {'sequence': 110, 'name': 'suspended', 'type': 'boolean', 'value': cl.suspended},
            ]

            for field in extra_fields:
                association_club_extra_fields.objects.update_or_create(
                    assn_club=found_club,
                    assn_club_field_sequence=field['sequence'],
                    defaults={
                        'assn_club_field_name': field['name'],
                        'assn_club_field_type': field['type'],
                        'assn_club_field_value': field['value'],
                        'assn_club_field_group': 's80_club_records',
                        'assn_club_field_active': True
                    }
                )

    if DEBUG_WRITE:
        f.write("      Completed get_update_or_create_association_club_extra_fields_BF: " + str(found_club.assn_club_name) + "\n")
def get_update_or_create_association_club_admin_BF(f, found_club, DEBUG_WRITE):
        if(DEBUG_WRITE):  
                f.write("      get_update_or_create_association_club_admin_BF: " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")

        try:  #does club exist.  
                association_clubs.objects.get(id = found_club.id)
        except:
                if(DEBUG_WRITE):
                        f.write("         Club does not exist: "  + " " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")
        else:
                if(DEBUG_WRITE):
                        f.write("         Club exists " + str(found_club.assn_club_name) + " " + str(timezone.now()) + "\n")
                email_admin = get_system_process_user()
                taa, created = association_club_admins.objects.update_or_create(assn_club=found_club, assn_club_admin=email_admin)
        if(DEBUG_WRITE):
                f.write("      returning get_update_or_create_association_club_admin_BF: " + str(found_club.assn_club_name) + " " + str(email_admin) + "\n")
def load_or_update_association_clubs_BF(f, association_name, DEBUG_WRITE):
    f.write("\nload_or_update_association_clubs_BF: " + str(association_name) + " " + str(timezone.now()) + "\n")

    asn = get_association(f, association_name, DEBUG_WRITE)
    if asn is not None:
        with transaction.atomic():
            for cl in s80_club_records.objects.all():
                if DEBUG_WRITE:
                    f.write("   Club: " + str(cl.name) + " " 
                            + str(cl.primary_address_line1) + " "
                            + str(cl.primary_address_postal_code) + "\n")
                
                found_club, found_club_new = update_or_create_association_club_BF(f, cl, asn, DEBUG_WRITE)
                found_address = update_or_create_address(f, DEBUG_WRITE, "", cl.primary_address_line1, 
                                        cl.primary_address_line2, cl.primary_address_line3, 
                                        cl.primary_address_city, cl.primary_address_region, 
                                        cl.primary_address_region_abbr, cl.primary_address_postal_code, 
                                        "", cl.primary_address_country)
                association_club_address.objects.update_or_create(assn_club=found_club, assn_club_addr=found_address)
                get_update_or_create_association_club_extra_fields_BF(f, cl, found_club, DEBUG_WRITE)
                
                if found_club_new:
                    initial_association_club_values_from_association(f, found_club, asn, DEBUG_WRITE)
                    get_update_or_create_association_club_admin_BF(f, found_club, DEBUG_WRITE)

    if DEBUG_WRITE:
        f.write("Completed: load_or_update_association_clubs_BF: " + str(association_name) + " " + str(timezone.now()) + "\n")
def get_association_club_BF(f, cl_name, asn, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      get_association_club_BF: " + str(cl_name) + " " + str(timezone.now()) + "\n")

    try:
        # Check if the club exists
        found_club = association_clubs.objects.get(assn_club_name=cl_name, assn=asn)
        if DEBUG_WRITE:
            f.write("         Club exists... : " + str(cl_name) + "\n")
    except association_clubs.DoesNotExist:
        found_club = None
        if DEBUG_WRITE:
            f.write("         WARNING!!! Club does not exist: " + str(cl_name) + "\n")

    if found_club is not None and DEBUG_WRITE:
        f.write("      returning get_association_club_BF: " + str(found_club) + " " + str(found_club.assn_club_number) + " " + str(found_club.assn_club_name) + "\n")
    
    return found_club
def get_update_or_create_association_member_BF(f, mr, asn, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      get_update_or_create_association_member_BF: " 
                + " identity number: " + str(mr.identity_number) + " "
                + str(mr.first_name) + " " + str(mr.last_name) + " " + str(timezone.now()) + "\n")
    
    found_member_new = False

    with transaction.atomic():
        try:
            # Check if the association member exists
            found_member = association_members.objects.get(assn=asn, assn_member_identifier=mr.identity_number)
            if DEBUG_WRITE:
                f.write("         Association Member does exist: " 
                        + " assn_member_identifier: " + str(found_member.assn_member_identifier) + " " 
                        + str(found_member.assn_member_first_name) + " " 
                        + str(found_member.assn_member_last_name) + " " 
                        + " assn_member_number: " + str(found_member.assn_member_number) + "\n")
            
            # Update the existing member
            found_member.assn_member_first_name = mr.first_name.title()
            found_member.assn_member_last_name = mr.last_name.upper()
            found_member.assn_member_full_name = mr.last_name.upper() + " " + mr.first_name.title()
            found_member.assn_member_dob = mr.dob
            found_member.assn_member_gender = mr.gender
            found_member.assn_member_joined_date = mr.joined_date
            found_member.assn_member_start_date = mr.start_date
            found_member.assn_member_exp_date = mr.exp_date
            found_member.assn_member_email = mr.email
            found_member.assn_member_phone = mr.phone
            found_member.assn_member_img_url = mr.img_url
            found_member.assn_member_valid = mr.valid
            found_member.assn_member_suspended = mr.suspended
            found_member.save()
        except association_members.DoesNotExist:
            if DEBUG_WRITE:
                f.write("         Association Member does not exist: " + str(mr.identity_number) + " " + str(mr.first_name) + " " + str(mr.last_name) + "\n")
            next_assn_member_id = base_get_next_system_value('next_assn_member_id')
            if DEBUG_WRITE:
                f.write("         next_assn_member_id = " + str(next_assn_member_id) + "\n")
            
            # Create a new member
            found_member = association_members(
                assn_member_number=next_assn_member_id,
                assn=asn,
                assn_member_identifier=mr.identity_number,
                assn_member_first_name=mr.first_name.title(),
                assn_member_last_name=mr.last_name.upper(),
                assn_member_full_name=mr.last_name.upper() + " " + mr.first_name.title(),
                assn_member_dob=mr.dob,
                assn_member_gender=mr.gender,
                assn_member_joined_date=mr.joined_date,
                assn_member_start_date=mr.start_date,
                assn_member_exp_date=mr.exp_date,
                assn_member_email=mr.email,
                assn_member_phone=mr.phone,
                assn_member_img_url=mr.img_url,
                assn_member_valid=mr.valid,
                assn_member_suspended=mr.suspended
            )
            found_member.save()
            found_member_new = True

    if DEBUG_WRITE:
        f.write("       returning get_update_or_create_association_member_BF: " + str(found_member.assn_member_identifier) + " " + str(found_member.assn_member_first_name) + " " + str(found_member.assn_member_last_name) + "\n")
    
    return found_member, found_member_new
def get_update_or_create_association_members_extra_fields_BF(f, mr, found_member, DEBUG_WRITE):
    if DEBUG_WRITE:
        f.write("      get_update_or_create_association_members_extra_fields_BF: " + str(mr.last_name) + " " + str(found_member.assn_member_full_name) + " " + str(timezone.now()) + "\n")

    with transaction.atomic():
        try:
            # Check if the member exists
            association_members.objects.get(id=found_member.id)
        except association_members.DoesNotExist:
            if DEBUG_WRITE:
                f.write("         Member does not exist: " + str(found_member.assn_member_full_name) + " " + str(timezone.now()) + "\n")
        else:
            if DEBUG_WRITE:
                f.write("         Member exists " + str(mr.last_name) + " " + str(found_member.assn_member_full_name) + " " + str(timezone.now()) + "\n")

            extra_fields = [
                {'sequence': 10, 'name': 'uuid_s80', 'type': 'string', 'value': mr.uuid_s80},
                {'sequence': 20, 'name': 'contact_uuid_s80', 'type': 'string', 'value': mr.contact_uuid_s80},
                {'sequence': 30, 'name': 'add_on_uuid_s80', 'type': 'string', 'value': mr.add_on_uuid_s80},
                {'sequence': 40, 'name': 'add_on_name', 'type': 'string', 'value': mr.add_on_name},
                {'sequence': 50, 'name': 'add_on_type_uuid_s80', 'type': 'string', 'value': mr.add_on_type_uuid_s80},
                {'sequence': 60, 'name': 'add_on_type_name', 'type': 'string', 'value': mr.add_on_type_name},
                {'sequence': 70, 'name': 'add_on_region', 'type': 'string', 'value': mr.add_on_region},
                {'sequence': 80, 'name': 'add_on_region_org_uuid_s80', 'type': 'string', 'value': mr.add_on_region_org_uuid_s80},
            ]

            for field in extra_fields:
                association_member_extra_fields.objects.update_or_create(
                    assn_member=found_member,
                    assn_member_field_sequence=field['sequence'],
                    defaults={
                        'assn_member_field_name': field['name'],
                        'assn_member_field1_type': field['type'],
                        'assn_member_field1_value': field['value'],
                        'assn_member_field_group': 's80_member_records',
                        'assn_member_field_active': True
                    }
                )

    if DEBUG_WRITE:
        f.write("      Completed get_update_or_create_association_members_extra_fields_BF: " + str(found_member.assn_member_full_name) + "\n")
def load_or_update_association_members_BF(f, association_name, DEBUG_WRITE):
    f.write("\nload_or_update_association_members_BF: " + str(association_name) + " " + str(timezone.now()) + "\n")

    asn = get_association(f, association_name, DEBUG_WRITE)

    s80_mr = s80_membership_records.objects.all()
    s80_cnt = s80_mr.count()
    cnt = 0
    if asn is not None:
#        if(1==1):
        with transaction.atomic():
            for mr in s80_mr:
                if DEBUG_WRITE:
                    f.write("   Member: " + str(mr.first_name) + " " + str(mr.last_name) + " " + str(mr.identity_number) + " " + str(timezone.now()) + "\n")
###HERE                
#                print("1", timezone.now())
                found_member, found_member_new = get_update_or_create_association_member_BF(f, mr, asn, DEBUG_WRITE)
#                print("2", timezone.now())
                get_update_or_create_association_members_extra_fields_BF(f, mr, found_member, DEBUG_WRITE)
                
#                print("3", timezone.now())
                found_address = update_or_create_address(f, DEBUG_WRITE, "", mr.primary_address_line1, 
                                        mr.primary_address_line2, mr.primary_address_line3, 
                                        mr.primary_address_city, mr.primary_address_region, 
                                        mr.primary_address_region_abbr, mr.primary_address_postal_code, 
                                        "", mr.primary_address_country)
#                print("4", timezone.now())
                association_member_address.objects.update_or_create(
                    assn_member=found_member, association_member_addr=found_address)
#                print("5", timezone.now())
                club_record = s80_membership_records_clubs.objects.filter(membership_uuid=mr).first()
#                print("6", timezone.now())
                if club_record:
#                    print("7", timezone.now())
                    found_club = get_association_club_BF(f, club_record.add_on_clubs_name, asn, DEBUG_WRITE)
#                    print("8", timezone.now())
                    if found_club is not None:
                        association_club_members.objects.update_or_create(
                            assn_club=found_club, assn_club_members=found_member)
#                        print("9", timezone.now())
                if(cnt % 100 == 0):
                        f.write("   Completed: " + str(cnt) + " of " + str(s80_cnt)+ " " +str(timezone.now()) + "\n")
                        print("   Completed: " + str(cnt) + " of " + str(s80_cnt)+ " " +str(timezone.now()))
                cnt += 1
    if DEBUG_WRITE:
        f.write("Completed: load_or_update_association_members_BF: " + str(association_name) + " " + str(timezone.now()) + "\n")


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

        assn_name_list = ["British Fencing"]
        for assn_name in assn_name_list:
                f.write("Process Association: " + assn_name + "\n")

                DEBUG_WRITE = False
        ####        create_system_users(f, DEBUG_WRITE)  #just for testing.  moved there
        ####        clear_association_tables(f, assn_name, DEBUG_WRITE)  #only needed for testing a full association reset with no Tournaments.

                record_log_data("assn_mgr_s80_process_membership_clubs", "get_or_build_association_BF", "Starting")
                get_or_build_association_BF(f, assn_name, DEBUG_WRITE)  
                record_log_data("assn_mgr_s80_process_membership_clubs", "get_or_build_association_BF", "Completed")

                record_log_data("assn_mgr_s80_process_membership_clubs", "load_or_update_association_clubs_BF", "Starting")
                load_or_update_association_clubs_BF(f, assn_name, DEBUG_WRITE)  #45 secs
                record_log_data("assn_mgr_s80_process_membership_clubs", "load_or_update_association_clubs_BF", "Completed")

                record_log_data("assn_mgr_s80_process_membership_clubs", "load_or_update_association_members_BF", "Starting")
                load_or_update_association_members_BF(f, assn_name, DEBUG_WRITE)  #25 mins
                record_log_data("assn_mgr_s80_process_membership_clubs", "load_or_update_association_members_BF", "Completed")

###                clear_clubs_for_association(f, assn_name, DEBUG_WRITE) #only needed for testing a full association reset
                record_log_data("assn_mgr_s80_process_membership_clubs", "move_association_clubs_to_clubs", "Starting")
                move_association_clubs_to_clubs(f, assn_name, DEBUG_WRITE)  #10 secs
                record_log_data("assn_mgr_s80_process_membership_clubs", "move_association_clubs_to_clubs", "Completed")

                record_log_data("assn_mgr_s80_process_membership_clubs", "move_association_members_to_clubs", "Starting")
                move_association_members_to_clubs(f, assn_name, DEBUG_WRITE)  # 3 mins
                record_log_data("assn_mgr_s80_process_membership_clubs", "move_association_members_to_clubs", "Completed")

        f.write("Complete: " + logs_filename + str(timezone.now()) + "\n")
        f.close()

        #Email log file
#        send_attachment(fname)
#        os.remove(fname)

#python manage.py runscript assn_mgr_s80_process_members_clubs



