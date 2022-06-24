from superduperoctofiesta.common import EnumData, RecoveryMethodEnum
from superduperoctofiesta.data import ScrapeOGC
from enum import Enum
import argparse
import os

OGC_URLS = ['https://reports.bcogc.ca/ogc/app001/r/ams_reports/bc_total_production?request=CSV_Y',
            'https://reports.bcogc.ca/ogc/app001/r/ams_reports/2?request=CSV_N',
            'https://iris.bcogc.ca/download/hydraulic_fracture_csv.zip',
            'https://iris.bcogc.ca/download/drill_csv.zip',
            'https://iris.bcogc.ca/download/prod_csv.zip']

AREA_CODE = [6200, 9022, 9021]

FORMATION_CODE = [4990, 4995, 4997, 5000, 4000]

# The format of the FILE_DICT is as follows:
# {FILENAME(IN FULL): [list of headers that you need to read from the file into the program]}
# In python {} means dictionary and [] means list, these are all comma separated

FILE_DICT = {'wells.csv': ["Surf Nad83 Lat", "Surf Nad83 Long", "Directional Flag"], #TODO: Also, here you will want to do the full range of inputs that you need from the individual CSV's
             "perf.csv": ['PERF STAGE NUM', 'CHARGE TYPE', 'CHARGE SIZE (g)', 'SHOTS PER METER', 'DEGREE OF PHASING',
                          'PERF COMMENTS', 'COMPLTN TOP DEPTH (m)', 'COMPLTN BASE DEPTH (m)'],
             'hydraulic_fracture.csv': ['COMPLTN TOP DEPTH (m)', 'COMPLTN BASE DEPTH (m)', 'FRAC STAGE NUM',
                                        'VISCOSITY GEL TYPE', 'ENERGIZER', 'ENERGIZER TYPE', 'AVG RATE (m3/min)',
                                        'AVG TREATING PRESSURE (MPa)', 'FRAC GRADIENT (KPa/m)','TOTAL FLUID PUMPED (m3)'
                                        ,'TOTAL CO2 PUMPED (m3)', 'TOTAL N2 PUMPED (scm)','TOTAL CH4 PUMPED (e3m3)',
                                        'PROPPANT TYPE1','PROPPANT TYPE1 PLACED (t)','PROPPANT TYPE2',
                                        'PROPPANT TYPE2 PLACED (t)', 'PROPPANT TYPE3','PROPPANT TYPE3 PLACED (t)',
                                        'PROPPANT TYPE4','PROPPANT TYPE4 PLACED (t)'],
             'compl_ev.csv':["Compltn_top_depth", "Compltn_base_depth", "Formtn_code"], # multiple WA
             'form_top.csv':["Formtn_code", "Tvd_formtn_top_depth "], # multiple WA
             'perf_net_interval.csv':["PERF STAGE NUM", "INTERVAL TOP DEPTH (m)", "INTERVAL BASE DEPTH (m)"], #multiple WA
             'dst.csv': ["Dst_num", "Top_intrvl_depth (m)", "Base_intrvl_depth (m)", "Init_shutin_press",
                         "Final_shutin_press", "Misrun_flag", "Skin", "Permblty", "Run_temp (c)", "Formtn_code"], # multiple WA, filter out misruns
             'pst_dtl.csv': ["Run_depth_temp (C)", "Run_depth_press (kPa)", "Datum_press (kPa)", "Run_depth (m)"], # might be multiple
             'pay_zone.csv': ["Oil porsty", "Gas porsty", "Oil water satrtn", "Gas water satrtn",
                              "Tvd oil net pay size", "Tvd gas net pay size"],
             'dst_rate.csv': ["Dst_num", "Flowing_fluid_type", "Init_fluid_rate", "Avg_fluid_rate", "Final_fluid_rate"],#multiple WA
             'zone_prd_2007_to_2015.csv': ["Prod_period", "Oil_prod_vol (m3)", "Gas_prod_vol (e3m3)", "Cond_prod_vol (m3)"],#multiple WA
             'zone_prd_2016_to_present.csv': ["Prod_period", "Oil_prod_vol (m3)", "Gas_prod_vol (e3m3)", "Cond_prod_vol (m3)"],#multiple WA
             'BC Total Production.csv': ["Zone Prod Period", "Oil Production (m3)", "Gas Production (e3m3)", "Condensate Production (m3)"]}#multiple WA

#TODO: populate this list with the headers that you will need for the model
INPUT_HEADERS = ['Well Authorization Number',
                'Surf Nad83 Lat',
                'Surf Nad83 Long',
                'CHARGE TYPE',
                'VISCOSITY GEL TYPE',
                'ENERGIZER',
                'ENERGIZER TYPE',
                'PROPPANT TYPE1',
                'PROPPANT TYPE2',
                'PROPPANT TYPE3',
                'PROPPANT TYPE4',
                'FRAC TYPE',
                'Energizer',
                'Energizer Type',
                'COMPLTN TOP DEPTH (m)',
                'COMPLTN BASE DEPTH (m)',
                'FRAC STAGE NUM',
                'IP90',
                'IP180',
                'Total Fluid Pumped (m3)',
                'CHARGE SIZE (g)',
                'SHOTS PER METER',
                'DEGREE OF PHASING',
                'AVG RATE (m3/min)',
                'AVG TREATING PRESSURE (MPa)',
                'FRAC GRADIENT (KPa/m)_x',
                'Oil porsty',
                'Gas porsty',
                'Permblty',
                'Directional Flag',
                'Oil water satrtn',
                'Gas water satrtn',
                'Tvd oil net pay size',
                'Tvd gas net pay size',
                'Average Treating Pressure',
                'Average Injection Rate',
                'FRAC GRADIENT (KPa/m)_y',
                'Fluid per m',
                'Tonnage per m3',
                'Formtn_code',
                'Compltn_top_depth',
                'Compltn_base_depth']

STRING_INPUTS = ['CHARGE TYPE',
                'VISCOSITY GEL TYPE',
                'ENERGIZER',
                'ENERGIZER TYPE',
                'PROPPANT TYPE1',
                'PROPPANT TYPE2',
                'PROPPANT TYPE3',
                'PROPPANT TYPE4',
                'FRAC TYPE',
                'Energizer',
                'Energizer Type']

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def parse_arguments():
    # create parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='A Machine Learning Based Predictor for production prediction '
                                                 'in the Montney Formation.')

    parser.add_argument("--download-ogc", type=str2bool, nargs='?', dest='download_ogc',
                        const=True, default=False,
                        help="Force Download the OGC data and rebuild the features list")

    parser.add_argument("--output-folder", type=dir_path, nargs='?', default=os.getcwd(), dest='output_folder',
                        help="Folder to save the OGC data csv files to or read them in from if they have already been downloaded")

    # parse the arguments
    args = parser.parse_args()
    return args

def main():

    # Use the above function to parse the arguments input into the program
    args = parse_arguments()

    # Download the data from OGC using the provided class
    ogc_data = ScrapeOGC(folder=args.output_folder, urls=OGC_URLS)

    ogc_data.download_data_url(file_names=FILE_DICT, force_download=args.download_ogc)

    ogc_data.find_well_names(area_code=AREA_CODE, formation_code=FORMATION_CODE)

    ogc_data.read_well_data(file_name=FILE_DICT)



if __name__ == "__main__":
    main()
