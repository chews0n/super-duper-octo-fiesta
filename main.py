from random import random
import argparse
import os
import yaml
from matplotlib import pyplot as plt


def plot_results(plot_time, plot_rates, plot_pressures):
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(plot_time, plot_rates, 'b-')
    ax2.plot(plot_time, plot_pressures, 'r-')

    ax1.set_xlabel('Time In Seconds')
    ax1.set_ylabel('Well Rate [m3/s]', color='b')
    ax2.set_ylabel('Well Pressure [Pa]', color='r')

    fig.suptitle('Well Testing Assignment')

    plt.savefig("example.jpg")


def main(input_file=""):
    # TODO: Load and Parse the input file, save it to separate variables to then use in the program

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

    time_resolution = 60 # this would be used for calculating draw down intervals for 60 seconds

    # TODO: Load the times and rates so that you can use them when coding, what do I mean by this?
    # Make sure that you have a rate and the elapsed time defined for more than just the start and end of the well testing
    # You will have to perform 6 different calculations because of superposition and sum them all up at the end
    # Doing this with a 2d array or a dictionary is probably your best bet


    # Your code here


    # TODO: Calculate the pressure drawdown for each of the well tests and use superposition and the initial reservoir pressure from the provided equation to determine your well pressure at each time throughout the series, this should be done with a resolution that will make it so the draw down is plotted correctly


    # Your code here

    # TODO: Plot your results, use the provided function for this.

    # plot_results(timelist, rateslist, pressurelist)



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

    # a comment comment


