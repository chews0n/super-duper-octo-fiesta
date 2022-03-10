import argparse
import os
import yaml
from matplotlib import pyplot as plt
import numpy as np
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
    #print the final plot
    print(plot_results())


def main(input_file="test_input.yml"):
    # TODO: Load and Parse the input file, save it to separate variables to then use in the program

    with open(input_file) as f:
        input_dict = yaml.safe_load(f)

    flow_rates = input_dict["flow_rates"]
    flow_rate_time = input_dict["flow_rate_time"]
    wellbore_radius = float(input_dict["wellbore_radius"])
    thick = float(input_dict["thick"])
    perm = float(input_dict["perm"])
    init_press = float(input_dict["init_press"])
    c_eff = float(input_dict["c_eff"])
    skin_factor = float(input_dict["skin_factor"])
    mu_oil = float(input_dict["mu_oil"])
    phi = float(input_dict["phi"])
    gamma = float(input_dict["gamma"])
    wellbore_radius = float(input_dict["wellbore_radius"])

    time_resolution = 60 # this would be used for calculating draw down intervals for 60 seconds



    # TODO: Load the times and rates so that you can use them when coding, what do I mean by this?
    # Make sure that you have a rate and the elapsed time defined for more than just the start and end of the well testing
    # You will have to perform 6 different calculations because of superposition and sum them all up at the end
    # Doing this with a 2d array or a dictionary is probably your best bet
    # Your code here
    #create 2d array for rates and time elapsed
    array1 = np.array([flow_rates,flow_rate_time])
    print(array1)
    print(array1[0,0],array1[0,1],array1[0,2]) #test

    cumulative_time_array = []
    cumulative_time_array = [0 for i in range(6)]
    cumulative_time_array[0] = array1[1,0]
    print(cumulative_time_array)
    i = 1
    for i in range (1,6):
        cumulative_time_array[i] = (array1[1,i]+cumulative_time_array[i-1])
        i = i + 1
        print(cumulative_time_array)

    array2 = np.array([flow_rates,cumulative_time_array])
    print(array2)


    # TODO: Calculate the pressure drawdown for each of the well tests and use superposition and the initial reservoir pressure from the provided equation to determine your well pressure at each time throughout the series, this should be done with a resolution that will make it so the draw down is plotted correctly
    # Your code here
    # Now do the 6 calculations and save the answers into another array and then sum them.
    # TODO: This overwrites the pressure_array variable each time in the loop, not really sure what this is doing.
    # TODO: You will have to divide the problem up into smaller time segments to get an appropriate resolution for the plots, to give you a hand with this your loop should look something like this:
    # linspace in numpy creates an array of times, from 0.0 to the last entry in the cumulative time array [-1] means last entry and has cumulative_time_array[-1] / time_resolution number of partitions
    flow_rates_to_plot = list()

    for time_of_the_well_test in np.linspace(0., cumulative_time_array[-1], int(cumulative_time_array[-1] / time_resolution)):
        for rate_idx, well_rate in enumerate(flow_rates):
            # In here you would then check if the well has started, you can exploit the fact that the first rate provided starts at time zero
            if rate_idx == 0:
                # calculate pressure and add it to the pressure array, continue is a placeholder
                continue

            else:
                # Check if the well has started
                if time_of_the_well_test >= cumulative_time_array[rate_idx - 1]:
                    # calculate pressure and add it to the pressure array, continue is a placeholder
                    continue

    for i in range (1,6):
        pressure_array = []
        pressure_array = [0 for i in range(6)]
        i = 0 # TODO: This will overwrite i from the above for loop
        # TODO: phi was loaded from the dictionary above already into the variable phi, the reason you were getting an error is that the first key in the dictionary is the name of the input "test_input", I'm actually going to remove this in your input file to make it less cumbersome
        print(input_dict.get("phi"));
        #stopped with error dict Mar.7 and 8'22

      #  for i in range(1, 6):
      #      pressure_array[i] = init_press -((array1[0,i]*mu_oil)/(4*np.pi()*perm*thick))*(math.log((4*perm*array1[1,i])/(phi*c_eff*mu_oil*(wellbore_radius^2)*np.exp(gamma)))+(2*skin_factor))
      #      i = i + 1
      #      print(pressure_array)

        total_pressure = 0
        for i in range(0, len(pressure_array)):
            # TODO: similar to above, you can't reuse the same variable name for a NESTED loop, a NESTED loop should look something like this:
            # for i in range (0, 6):
            #     for j in range(0,6):
            #         for k in range(0,6):
            # and so on and so forth, reusing variables overwrites them based on whatever has been executed last
            sum = sum + pressure_array[i];
            print(total_pressure)

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

# Should the argparser go here???
# TODO: This should go at the bottom of the file
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", action="store", default=os.path.join("inputs", "test_input.yml"),
                        help="Location of the well test inputs to parse.")

    inputArgs = parser.parse_args()

    main(inputArgs.input_file)







