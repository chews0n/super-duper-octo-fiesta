import argparse
import os
import yaml
from matplotlib import pyplot as plt
import math


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

    flow_rates = input_dict["test_input"]["flow_rates"]
    flow_rate_time = input_dict["test_input"]["flow_rate_time"]
    thick = float(input_dict["test_input"]["thick"])
    perm = float(input_dict["test_input"]["perm"])
    init_press = float(input_dict["test_input"]["init_press"])
    c_eff = float(input_dict["test_input"]["c_eff"])
    skin_factor = float(input_dict["test_input"]["skin_factor"])
    mu_oil = float(input_dict["test_input"]["mu_oil"])
    phi = float(input_dict["test_input"]["phi"])
    gamma = float(input_dict["test_input"]["gamma"])
    wellbore_radius = float(input_dict["test_input"]["wellbore_radius"])

    time_resolution = 60  # this would be used for calculating draw down intervals for 60 seconds

    # TODO: Load the times and rates so that you can use them when coding, what do I mean by this? Make sure that you
    #  have a rate and the elapsed time defined for more than just the start and end of the well testing You will
    #  have to perform 6 different calculations because of superposition and sum them all up at the end Doing this
    #  with a 2d array or a dictionary is probably your best bet

    start_time = list()
    end_time = list()
    for val in flow_rate_time:
        if len(start_time) < 1:
            start_time.append(0.0)
            end_time.append(val)
        else:
            start_time.append(end_time[-1])
            end_time.append(end_time[-1] + val)

    # TODO: Calculate the pressure drawdown for each of the well tests and use superposition and the initial
    #  reservoir pressure from the provided equation to determine your well pressure at each time throughout the
    #  series, this should be done with a resolution that will make it so the draw down is plotted correctly

    max_number_of_steps = int(end_time[-1] / time_resolution)
    timelist = list()
    timelist.append(0.0)
    for t in range(0, max_number_of_steps):
        timelist.append(timelist[-1] + time_resolution)
    rateslist = list()
    pressurelist = list()
    for elapsed_time in timelist:
        pressure_current = init_press
        rate_to_use = 0.0

        for rateidx, flowrate in enumerate(flow_rates):

            if start_time[rateidx] <= elapsed_time:
                qlast = 0.0
                if rateidx != 0:
                    qlast = flow_rates[rateidx - 1]

                # Make a calculation for the pressure draw down and add it to the pressure drawdown
                if elapsed_time - start_time[rateidx] > 0.0:
                    pressure_current -= ((flowrate - qlast) * mu_oil / (4 * math.pi * perm * thick)) * (math.log(4 * perm * (elapsed_time - start_time[rateidx]) / (phi * c_eff * mu_oil * math.pow(wellbore_radius, 2) * math.exp(gamma))) + 2*skin_factor)

                if start_time[rateidx] <= elapsed_time <= end_time[rateidx]:
                    rate_to_use = flowrate
        # add the values to the pressure and rate list
        pressurelist.append(pressure_current)
        rateslist.append(rate_to_use)

    # TODO: Plot your results, use the provided function for this.

    plot_results(timelist, rateslist, pressurelist)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", action="store", default=os.path.join("inputs", "test_input.yml"),
                        help="Location of the well test inputs to parse.")

    inputArgs = parser.parse_args()

    main(inputArgs.input_file)
