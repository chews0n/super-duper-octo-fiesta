import argparse
import os
import yaml
from matplotlib import pyplot as plt
import numpy as np
import math

def main(input_file="test_input.yml"):
    # TODO: Load and Parse the input file, save it to separate variables to then use in the program

    with open(input_file) as f:
        input_dict = yaml.safe_load(f)

    flow_rates = input_dict["test_input"]["flow_rates"]
    flow_rate_time = input_dict["test_input"]["flow_rate_time"]
    wellbore_radius = float(input_dict["test_input"]["wellbore_radius"])
    thick = float(input_dict["test_input"]["thick"])
    perm = float(input_dict["test_input"]["perm"])
    init_press = float(input_dict["test_input"]["init_press"])
    c_eff = float(input_dict["test_input"]["c_eff"])
    skin_factor = float(input_dict["test_input"]["skin_factor"])
    mu_oil = float(input_dict["test_input"]["mu_oil"])
    phi = float(input_dict["test_input"]["phi"])
    gamma = float(input_dict["test_input"]["gamma"])
    #wellbore_radius = float(input_dict["test_input"]["wellbore_radius"]) repeated above

    # this would be used for calculating draw down intervals for 60 seconds
    time_resolution = 60

    # test that the input_dict works
    #print(wellbore_radius,thick,c_eff,phi)
    # print(input_dict.get("phi")) Just all phi, not need to call dict!
    # stopped with error dict Mar.7 and 8'22

    # TODO: Load the times and rates so that you can use them when coding, what do I mean by this?
    # Make sure that you have a rate and the elapsed time defined for more than just the start and end of the well testing
    # You will have to perform 6 different calculations because of superposition and sum them all up at the end
    # Doing this with a 2d array or a dictionary is probably your best bet
    # Your code here
    #create 2d array for rates and time elapsed
    array1 = np.array([flow_rates,flow_rate_time])
    print(array1)
    #print(array1[1,0],array1[1,1],array1[1,2]) #test

    #cumulative_time_array = [] not needed
    cumulative_time_array = [0 for i in range(6)]
    cumulative_time_array[0] = array1[1,0]
    print(cumulative_time_array)
    i = 1
    for i in range (1,6):
        cumulative_time_array[i] = (array1[1,i]+cumulative_time_array[i-1])
        i = i + 1
        print(cumulative_time_array)

    array2 = np.array([flow_rates,cumulative_time_array])
    print("array2", array2)
    pressure_array = [] * 6 #creates 6 empty spots

    # TODO: Calculate the pressure drawdown for each of the well tests and use superposition and the initial reservoir pressure from the provided equation to determine your well pressure at each time throughout the series, this should be done with a resolution that will make it so the draw down is plotted correctly
    # Your code here
    # Now do the 6 calculations and save the answers into another array and then sum them.

    #for j in range(1, 6):
    #    pressure_array = [0 for j in range(6)]

    """print(array1[0, 0], mu_oil, np.pi)
    pressure_array = init_press - ((array1[0, 0] * mu_oil) / (4 * np.pi * perm * thick))* \
                     (((math.log((4 * perm * array1[1, 0]) / (phi * c_eff * mu_oil * (wellbore_radius ** 2) * np.exp(gamma)))) + (2 * skin_factor)))
    print(pressure_array)"""

    k = 0
    for k in range(0, 6):
        pressure_value = init_press - (((array1[0, k]*mu_oil)/(4*np.pi*perm*thick))*((math.log((4*perm*array1[1, k])/(phi*c_eff*mu_oil*(wellbore_radius**2)*np.exp(gamma)))+(2*skin_factor))))
        pressure_array.append(pressure_value)
        k = k + 1

    print("pressure_array", pressure_array)

    """total_pressure = 0
    for l in range(0, len(pressure_array)):
        sum = sum + pressure_array[l]
        print(total_pressure)

    for rateidx, rates in enumerate(flow_rates):
        testlist.append(rates*2)
        if rates >= 0.0065:
            print("The rate is larger or equal to 0.0065!!")
            print("I'm printing another statement")
        elif rates == 0.0065:
             print("The rate is equal to 0.0065")
        else:
             print("The number is less than 0.0065")

        print("this is outside of the if statement")"""

    # TODO: Plot your results, use the provided function for this.
    plot_rates = array2[0, :]  # take all rates
    print("plot_rates", plot_rates)

    plot_time = array2[1, :]  # take all cumulative times
    print("plot_time", plot_time)

    plot_pressures = pressure_array.copy() # take all pressures
    print("plot_pressures", plot_pressures)

# plot_results(timelist, rateslist, pressurelist)
def plot_results(plot_time, plot_rates, plot_pressures):
    fig, ax1 = plt.subplots()

    #test the plot fcn
    #plot_time = [86400.0, 259200.0, 518400.0, 691200.0, 936800.0, 1099332.0]
    #plot_rates = [6.000000e-03, 1.000000e-02, 0.000000e+00, 9.000000e-03, 2.000000e-03, 6.000000e-03]
    #plot_pressures = [15000000, 12877034.1, 15000000, 13089330.69, 14564216.02, 13732070.36]

    ax2 = ax1.twinx()
    ax1.plot(plot_time, plot_rates, 'b-')
    ax2.plot(plot_time, plot_pressures, 'r-')

    ax1.set_xlabel('Time In Seconds')
    ax1.set_ylabel('Well Rate [m3/s]', color='b')
    ax2.set_ylabel('Well Pressure [Pa]', color='r')

    fig.suptitle('Well Testing Assignment')

    plt.savefig("example_plot.jpg")
    # print the final plot
    plt.show()
    plt.ioff()
    plt.savefig()

# Should the argparser go here??? Stopped Mar.8'22
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", action="store", default=os.path.join("inputs", "test_input.yml"),
                    help="Location of the well test inputs to parse.")

    inputArgs = parser.parse_args()

    main(inputArgs.input_file)

""""#Parser Example: Create the parser
    parser = argparse.ArgumentParser(description='Does some stuff with an input file.')
    #add the argument
    parser.add_argument('-i', '--input', dest='infile', type=file, required=True,
                        metavar='INPUT_FILE', help='The input file to the script.')
    #parse and assign to the variable
    args = parser.parse_args()
    infile = args.infile"""







