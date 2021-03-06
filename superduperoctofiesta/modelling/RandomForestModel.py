from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
import random
import pandas as pd

PROD_VALS = ['IP30', 'IP60', 'IP90', 'IP120', 'IP150', 'IP180', 'IP210', 'IP240', 'IP270', 'IP300', 'IP330', 'IP360',
             'IP390', 'IP420', 'IP450', 'IP480', 'IP510', 'IP540', 'IP570', 'IP600', 'IP630', 'IP660', 'IP690', 'IP720',
             'IP750', 'IP780', 'IP810', 'IP840', 'IP870', 'IP900', 'IP930', 'IP960', 'IP990', 'IP1020', 'IP1050',
             'IP1080', 'IP1110', 'IP1140', 'IP1170', 'IP1200', 'IP1230', 'IP1260', 'IP1290', 'IP1320', 'IP1350',
             'IP1380', 'IP1410', 'IP1440', 'IP1470', 'IP1500', 'IP1530', 'IP1560', 'IP1590', 'IP1620', 'IP1650',
             'IP1680', 'IP1710', 'IP1740', 'IP1770', 'IP1800']

PLOT_X_VALS = ['30', '60', '90', '120', '150', '180', '210', '240', '270', '300', '330', '360',
             '390', '420', '450', '480', '510', '540', '570', '600', '630', '660', '690', '720',
             '750', '780', '810', '840', '870', '900', '930', '960', '990', '1020', '1050',
             '1080', '1110', '1140', '1170', '1200', '1230', '1260', '1290', '1320', '1350',
             '1380', '1410', '1440', '1470', '1500', '1530', '1560', '1590', '1620', '1650',
             '1680', '1710', '1740', '1770', '1800']

class RandomForestModel:

    def __init__(self, df=None):
        # put the class variables here
        self.modelprod = list()
        self.df = df
        self.feature_list = self.df.drop(
            ['IP30', 'IP60', 'IP90', 'IP120', 'IP150', 'IP180', 'IP210', 'IP240', 'IP270', 'IP300', 'IP330', 'IP360',
             'IP390', 'IP420', 'IP450', 'IP480', 'IP510', 'IP540', 'IP570', 'IP600', 'IP630', 'IP660', 'IP690', 'IP720',
             'IP750', 'IP780', 'IP810', 'IP840', 'IP870', 'IP900', 'IP930', 'IP960', 'IP990', 'IP1020', 'IP1050',
             'IP1080', 'IP1110', 'IP1140', 'IP1170', 'IP1200', 'IP1230', 'IP1260', 'IP1290', 'IP1320', 'IP1350',
             'IP1380', 'IP1410', 'IP1440', 'IP1470', 'IP1500', 'IP1530', 'IP1560', 'IP1590', 'IP1620', 'IP1650',
             'IP1680', 'IP1710', 'IP1740', 'IP1770', 'IP1800', 'Well Authorization Number'], axis=1)
        self.target_listprod = list()  # self.df.filter(['IP90'], axis=1)
        self.well_list_test = list() #self.df.filter(['Well Authorization Number'], axis=1)
        self.x_trainprod = list()
        self.x_testprod = list()
        self.y_trainprod = list()
        self.y_testprod = list()
        self.y_predprod = list()
        self.sc_xprod = list()
        self.sc_yprod = list()
        self.trainpoolprod = list()

        for pval in PROD_VALS:
            self.target_listprod.append(self.df.filter([pval], axis=1))

    def split_data(self):
        previous_prod = list()
        numprod = self.df[self.df.columns[0]].count()
        for idx, tlistprod in enumerate(self.target_listprod):
            if (idx == 0):
                for prodv in range(0,numprod):
                    previous_prod.append(np.float64(0.0))

                dat2 = pd.DataFrame({'prevprod': previous_prod})

                self.feature_list = self.feature_list.join(dat2)
            else:
                self.feature_list['prevprod'] = previous_prod


            # this loop goes over each of the production month values and trains a separate model
            # we'll have to change the feature list value for the previous month's production.

            x_trainprod, x_testprod, y_trainprod, y_testprod = train_test_split(self.feature_list,
                                                                                tlistprod, test_size=0.2,
                                                                                random_state=1)

            self.well_list_test = x_testprod.filter(['Well Authorization Number'], axis=1).index.tolist()

            self.x_trainprod.append(x_trainprod)
            self.x_testprod.append(x_testprod)
            self.y_trainprod.append(y_trainprod)
            self.y_testprod.append(y_testprod)

            previous_prod = np.float64(self.target_listprod[idx][PROD_VALS[idx]].to_list())

    def train_model(self):
        # Train the model with CatBoost Regressor

        for idx in range(0, len(self.target_listprod)):

            self.sc_xprod.append(StandardScaler())
            self.sc_yprod.append(StandardScaler())

            self.x_trainprod[idx] = self.sc_xprod[idx].fit_transform(self.x_trainprod[idx])
            self.y_trainprod[idx] = self.sc_yprod[idx].fit_transform(self.y_trainprod[idx])

            self.modelprod.append(CatBoostRegressor(iterations=1000, learning_rate=0.01,
                                               logging_level='Silent', random_seed=random.randint(0, 2500)))

            self.trainpoolprod.append(Pool(self.x_trainprod[idx], self.y_trainprod[idx]))
            self.modelprod[idx].fit(self.trainpoolprod[idx], eval_set=(self.x_testprod[idx], self.y_testprod[idx]))

    def predict_initial_production(self, xprod, ensemble=False, syntheticprev=False):
        # Pass in the inputs that you want to use to predict production
        y_predprod = list()

        if ensemble:
            dat2 = pd.DataFrame({'prevprod': [0.0]})
            xprod = xprod.join(dat2)

        for idx, modprod in enumerate(self.modelprod):
            if ensemble:
                y_predprod.append(self.sc_yprod[idx].inverse_transform(
                    self.modelprod[idx].predict(self.sc_xprod[idx].transform(xprod)).reshape(-1, 1)))
                xprod['prevprod'] = y_predprod[idx]
            else:
                if idx > 1 and syntheticprev:
                    xprod[idx]['prevprod'] = xprod[idx-1]['prevprod']

                y_predprod.append(self.sc_yprod[idx].inverse_transform(
                    self.modelprod[idx].predict(self.sc_xprod[idx].transform(xprod[idx])).reshape(-1, 1)))

        return y_predprod

    def model_statistics(self, iteration=0):

        for idx, proddays in enumerate(PROD_VALS):
            error = mean_absolute_error(self.y_testprod[idx], self.y_predprod[idx])
            print('{},{}: Prod Accuracy:'.format(proddays,iteration), round(error, 2))
            r2 = r2_score(self.y_testprod[idx], self.y_predprod[idx])
            print('{},{}: Prod R2:'.format(proddays,iteration), round(r2, 2))

            # Calculate mean absolute percentage error (MAPE)
            mape = 100 * (abs(self.y_predprod[idx] - self.y_testprod[idx]) / self.y_testprod[idx])
            accuracy = 100 - np.mean(mape)
            print('{},{}: Prod Accuracy:'.format(proddays,iteration), round(accuracy, 2), '%.')

    def plot_test_vs_pred(self):

        for idx,wells in enumerate(self.well_list_test):
            yplotvalsorig = list()
            yplotvalspred = list()

            xvalsplot = list()



            for idx2, prodlist in enumerate(PROD_VALS):

                # here we have the prod list that we're looking at
                # these are the original values
                yplotvalsorig.append(self.df.iloc[wells][prodlist])
                yplotvalspred.append(self.y_predprod[idx2][idx])

                xvalsplot.append((idx2 + 1)*30)


            plt.plot(xvalsplot, yplotvalsorig, 'b-', label='actual')
            plt.plot(xvalsplot, yplotvalspred, 'ro', label='prediction')
            plt.legend()
            plt.xlabel('Time [Days]')
            plt.ylabel('BOE Production [SM3]')
            plt.title('Actual and Predicted Values')
            plt.xticks(np.arange(min(xvalsplot), max(xvalsplot) + 1, 360))

            plt.savefig('ActualVsPred_well_{}.png'.format(wells), dpi=300)
            plt.clf()


    def feature_importance(self, iternum):
        x_col = self.feature_list.columns
        for idx, model in enumerate(self.trainpoolprod):
            feature_importances = self.modelprod[idx].get_feature_importance(self.trainpoolprod[idx])
            plot_labels = ['LAT', 'LONG',
                           'CHARGE', 'GEL',
                           'ENERGIZER', 'ENERGIZERT',
                           'PROP1', 'PROP2',
                           'PROP3', 'PROP4',
                           'FRACT', 'Energizer',
                           'EnergizerT', 'TOP',
                           'BASE', 'FRACNUM',
                           'CUMFLUID', 'CHARGESIZE',
                           'SHOTSPM', 'PHASING',
                           'RATE', 'PRESS',
                           'FGRADX', 'PORO',
                           'GPORO', 'Oil water satrtn',
                           'SAT', 'NETPAY',
                           'PAYGAS', 'TreatPRESS',
                           'INJRATE', 'FGRADY',
                           'FLUIDPM', 'TONPM',
                           'PREVPROD']
            for score, name in sorted(zip(feature_importances, x_col), reverse=True):
                print('{}: {}'.format(name, score))

            # for idx, val in enumerate(feature_importances)
            plt.bar(plot_labels, feature_importances)
            plt.xticks(rotation='vertical')
            plt.savefig('Feature_Importanceprod_PRODMONTH_{}_iter_{}.png'.format(idx,iternum), dpi=300)
            plt.clf()
