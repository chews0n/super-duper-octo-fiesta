from superduperoctofiesta.data import ScrapeOGC
from superduperoctofiesta.modelling import RandomForestModel
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd

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
                          'PERF COMMENTS'],
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
             'pst_dtl.csv': ["UWI", "Run_depth_temp (C)", "Run_depth_press (kPa)", "Datum_press (kPa)", "Run_depth (m)"], # might be multiple
             'pay_zone.csv': ["Oil porsty", "Gas porsty", "Oil water satrtn", "Gas water satrtn",
                              "Tvd oil net pay size", "Tvd gas net pay size"],
             'dst_rate.csv': ["Dst_num", "Flowing_fluid_type", "Init_fluid_rate", "Avg_fluid_rate", "Final_fluid_rate"],#multiple WA
             'zone_prd_2007_to_2015.csv': ["UWI", "Prod_period", "Oil_prod_vol (m3)", "Gas_prod_vol (e3m3)", "Cond_prod_vol (m3)"],#multiple WA
             'zone_prd_2016_to_present.csv': ["UWI", "Prod_period", "Oil_prod_vol (m3)", "Gas_prod_vol (e3m3)", "Cond_prod_vol (m3)"],#multiple WA
             'BC Total Production.csv': ["UWI", "Zone Prod Period", "Oil Production (m3)", "Gas Production (e3m3)", "Condensate Production (m3)"],
              #'zone_prd.csv': ["Prod_period", "UWI", "Area_code", "Formtn_code", "Pool_seq", "Gas_prod_vol (e3m3)", "Oil_prod_vol (m3)", "Water_prod_vol (m3)", "Cond_prod_vol (m3)", "Prod_period", "Gas_prod_cum (e3m3)", "Oil_prod_cum (m3)", "Water_prod_cum (m3)", "Cond_prod_cum (m3)"],
             #'Fracture Fluid Data.csv': ["Fracture Date", "Well Area Name", "UWI", "Ingredient Name", "Ingredient Concentration in HF Fluid % by Mass", "Ingredient Percentage in Additive by % Mass", "Total Water Volume (m^3)"],
             #'compl_wo.csv': ["UWI", "Area_code", "Formtn_code", "Pool_seq", "Compltn_event_seq", "Compltn_date", "Compltn_top_depth (m)", "Compltn_base_depth (m)", "Compltn_type", "Stimltn_type", "Flow_fluid_type", "Stimltn_vol (m3)", "Stimltn_press (kPa)"]
             } #multiple WA

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
                'Total Fluid Pumped (m3)',
                'CHARGE SIZE (g)',
                'SHOTS PER METER',
                'DEGREE OF PHASING',
                'AVG RATE (m3/min)',
                'AVG TREATING PRESSURE (MPa)',
                'FRAC GRADIENT (KPa/m)_x',
                'Oil porsty',
                'Gas porsty',
                #'Permblty',
                #'Directional Flag',
                'Oil water satrtn',
                'Gas water satrtn',
                'Tvd oil net pay size',
                'Tvd gas net pay size',
                'Average Treating Pressure',
                'Average Injection Rate',
                'FRAC GRADIENT (KPa/m)_y',
                'Fluid per m',
                'Tonnage per m3',
                'IP30',
                'IP60',
                'IP90',
                'IP120',
                'IP150',
                'IP180',
                'IP210',
                'IP240',
                'IP270',
                'IP300',
                'IP330',
                'IP360',
                'IP390',
                'IP420',
                'IP450',
                'IP480',
                'IP510',
                'IP540',
                'IP570',
                'IP600',
                'IP630',
                'IP660',
                'IP690',
                'IP720',
                'IP750',
                'IP780',
                'IP810',
                'IP840',
                'IP870',
                'IP900',
                'IP930',
                'IP960',
                'IP990',
                'IP1020',
                'IP1050',
                'IP1080',
                'IP1110',
                'IP1140',
                'IP1170',
                'IP1200',
                'IP1230',
                'IP1260',
                'IP1290',
                'IP1320',
                'IP1350',
                'IP1380',
                'IP1410',
                'IP1440',
                'IP1470',
                'IP1500',
                'IP1530',
                'IP1560',
                'IP1590',
                'IP1620',
                'IP1650',
                'IP1680',
                'IP1710',
                'IP1740',
                'IP1770',
                'IP1800'
                #'Compltn_top_depth',
                #'Compltn_base_depth'
                 ]

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

PROD_VALS = ['IP30', 'IP60', 'IP90', 'IP120', 'IP150', 'IP180', 'IP210', 'IP240', 'IP270', 'IP300', 'IP330', 'IP360',
             'IP390', 'IP420', 'IP450', 'IP480', 'IP510', 'IP540', 'IP570', 'IP600', 'IP630', 'IP660', 'IP690', 'IP720',
             'IP750', 'IP780', 'IP810', 'IP840', 'IP870', 'IP900', 'IP930', 'IP960', 'IP990', 'IP1020', 'IP1050',
             'IP1080', 'IP1110', 'IP1140', 'IP1170', 'IP1200', 'IP1230', 'IP1260', 'IP1290', 'IP1320', 'IP1350',
             'IP1380', 'IP1410', 'IP1440', 'IP1470', 'IP1500', 'IP1530', 'IP1560', 'IP1590', 'IP1620', 'IP1650',
             'IP1680', 'IP1710', 'IP1740', 'IP1770', 'IP1800']
# these are in cums, did you want to do just that month's prduction?
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
        raise argparse.ArgumentTypeError("readable_dir:{} is not a valid path".format(path))

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

    parser.add_argument("--input-file", type=str, nargs='?', default='input.csv', dest='input_file',
                        help="Input file for the input to the model predictor.")

    parser.add_argument("--feature-file", type=str, nargs='?', default='feature_list.csv', dest='feature_file',
                        help="CSV file containing the feature list and values used to train the model.")

    parser.add_argument("--number-of-iterations", type=int, nargs='?', default=5,
                        dest='numiters',
                        help="Number of iterations to create a model and get results from it")

    parser.add_argument("--confidence-interval", type=float, nargs='?', default=95,
                        dest='confidence_interval',
                        help="Confidence interval for the ensemble based evaluation of the model")

    # parse the arguments
    args = parser.parse_args()
    return args

def plot_ens_well_vals(yplotvalsorig, yplotvalspred, wellnum):

    xvalsplot = list()

    for idx, prodlist in enumerate(PROD_VALS):

        xvalsplot.append((idx + 1) * 30)

    plt.plot(xvalsplot, yplotvalsorig, 'b-', label='actual')

    for idx, yvals in enumerate(yplotvalspred):
        plt.plot(xvalsplot, yvals, 'ro', label='pred')

    #plt.legend()
    plt.xlabel('Time [Days]')
    plt.ylabel('BOE Production [SM3]')
    plt.title('Actual and Predicted Values')
    plt.xticks(np.arange(min(xvalsplot), max(xvalsplot) + 1, 360))

    plt.savefig('ActualVsPred_well_{}.png'.format(wellnum), dpi=300)
    plt.clf()

def main():

    # Use the above function to parse the arguments input into the program
    args = parse_arguments()

    # Download the data from OGC using the provided class
    ogc_data = ScrapeOGC(folder=args.output_folder, urls=OGC_URLS)

    prediction = True

    # use the input value(s) to predict the outputs
    wellnames = None
    if (os.path.isfile(args.input_file)):
        inputcsv = pd.read_csv(args.input_file)
        wellnames = inputcsv.filter(['Well Authorization Number'], axis=1).values.tolist()[0][0]
        inputcsv = inputcsv.drop(['Well Authorization Number'], axis=1)

    else:
        print("the input file {} could not be found \n".format(args.input_file))
        print("Prediction module will not proceed")
        prediction = False

    ogc_data.download_data_url(file_names=FILE_DICT, force_download=args.download_ogc)
    if (args.feature_file is not None and os.path.isfile(args.feature_file) and args.download_ogc is False):
        ogc_data.feature_list = pd.read_csv(args.feature_file)
        ogc_data.feature_list = ogc_data.feature_list.iloc[:, 1:]

    else:
        ogc_data.download_data_url(file_names=FILE_DICT)

        ogc_data.find_well_names(area_code=AREA_CODE, formation_code=FORMATION_CODE)

        ogc_data.read_well_data(file_name=FILE_DICT)

        ogc_data.calc_monthly_prod()

        ogc_data.determine_frac_type()

        ogc_data.fill_feature_list_nan_with_val(columns=['PROPPANT TYPE1 PLACED (t)', 'PROPPANT TYPE2 PLACED (t)',
                                                        'PROPPANT TYPE3 PLACED (t)', 'PROPPANT TYPE4 PLACED (t)'],
                                               val=0)

        ogc_data.calc_frac_props()

        ogc_data.fill_feature_list_nan_with_val(columns=['Total CO2 Pumped (m3)', 'Total N2 Pumped (scm)',
                                                        'Total CH4 Pumped (e3m3)'], val=0)

        ogc_data.remove_wells()

        ogc_data.create_cleaned_feature_list()

        ogc_data.convert_string_inputs_to_none(STRING_INPUTS)

        ogc_data.fill_feature_list_nan_with_val(columns=INPUT_HEADERS, val=0)

        ogc_data.print_feature_list_to_csv()

    ensemble_pred = list()

    # Create 30 day prod predictions.

    # FROM here, we train the model based on past data, we will remove a section of the data as verification data to check out predictions against
    # for loop here around the data for separate model creation depending on or have one model, but for us
    if not prediction:
        ogcModel = RandomForestModel(df=ogc_data.feature_list)

        ogcModel.split_data()

        print("Training the model...\n")

        ogcModel.train_model()

        print("Model Evaluation...\n")

        ogcModel.y_predprod = ogcModel.predict_initial_production(ogcModel.x_testprod)

        ogcModel.feature_importance(0)

        ogcModel.model_statistics()

        ogcModel.plot_test_vs_pred()
    else:

        predicted_vals = list()
        orig_vals = list()
        well_num = -1
        for ens_iter in range(0, args.numiters):
            ogcModel = RandomForestModel(df=ogc_data.feature_list)

            ogcModel.split_data()

            print("Training the model...\n")

            ogcModel.train_model()

            print("Model Evaluation...\n")

            ogcModel.y_predprod = ogcModel.predict_initial_production(ogcModel.x_testprod)

            ogcModel.feature_importance(ens_iter)

            predvalstmp = ogcModel.predict_initial_production(inputcsv, ensemble=True)

            predvalstmp = np.concatenate(np.concatenate(predvalstmp, axis=0), axis=0).tolist()

            predicted_vals.append(predvalstmp)

            if ens_iter == 1:
                well_num = ogcModel.df.index[ogcModel.df["Well Authorization Number"] == wellnames].values.tolist()[0]

                orig_vals = ogcModel.df.iloc[well_num].values.tolist()

                orig_vals = orig_vals[18:18+len(PROD_VALS)]

            ogcModel.model_statistics(ens_iter)

            ensemble_pred.append(predicted_vals)

        plot_ens_well_vals(orig_vals, predicted_vals, well_num)

    print("Super Duper Octofiesta is finishing....")

if __name__ == "__main__":
    main()
