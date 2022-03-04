from random import random

import pandas
import argparse
import os
import yaml


def main(input_file=""):


    with open(input_file) as f:
        input_dict = yaml.safe_load(f)

    flow_rates = input_dict["test_inputs"]["flow_rates"]
    flow_rate_time = input_dict["test_inputs"]["flow_rate_time"]
    wellbore_radius = float(input_dict["test_inputs"]["wellbore_radius"])
    thick = float(input_dict["test_inputs"]["thick"])
    perm = float(input_dict["test_inputs"]["perm"])
    init_press = float(input_dict["test_inputs"]["init_press"])
    c_eff = float(input_dict["test_inputs"]["c_eff"])
    skin_factor = float(input_dict["test_inputs"]["skin_factor"])
    mu_oil = float(input_dict["test_inputs"]["mu_oil"])
    phi = float(input_dict["test_inputs"]["phi"])
    gamma = float(input_dict["test_inputs"]["gamma"])
    wellbore_radius = float(input_dict["test_inputs"]["wellbore_radius"])


    # for rateidx, rates in enumerate(flow_rates):
    #     testlist.append(rates*2)
    #     if rates >= 0.0065:
    #         print("The rate is larger or equal to 0.0065!!")
    #         print("I'm printing another statement")
    #     elif rates == 0.0065:
    #         print("The rate is equal to 0.0065")
    #     else:
    #         print("The number is less than 0.0065")
    #
    #     print("this is outside of the if statement")
    #
    print("hello")






if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", action="store", default=os.path.join("inputs", "test_input.yml"),
                        help="Location of the well test inputs to parse.")

    inputArgs = parser.parse_args()

    main(inputArgs.input_file)



