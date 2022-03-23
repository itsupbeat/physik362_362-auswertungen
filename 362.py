import numpy as np
import matplotlib.pyplot as plt
from kafe2 import XYContainer, Fit, Plot, ContoursProfiler


def xy_data(x_data, y_data, x_err=0, y_err=0):
    '''
    Function to make code more clear. Builds the XYContainer used by kafe2
    :param x_data: x-data for fit
    :param y_data: y-data for fit
    :param x_err: error of x-data for fit
    :param y_err: error of y-data for fit
    :return:
    '''
    data = XYContainer(x_data=x_data, y_data=y_data)
    data.add_error(axis='x', err_val=x_err)
    data.add_error(axis='y', err_val=y_err)
    return data

###
# a
###


def lin_model(x, a, b):
    '''
    Fit model for 370.b
    :param x: the inverse wavelength squared (not just wavelength)
    :param a: constant
    :param b: constant
    :return:
    '''
    return x * a + b


def lin_fit(x, y, x_err, y_err, title="", x_name="", y_name=""):
    """
    Function for linear fit
    :param x: values x axis
    :param y: values y axis
    :param x_err: error x axis
    :param y_err: error y axis
    :param title: string used as header
    :param x_name: string used as label for x axis
    :param y_name: string used as label for y axis
    :return:
    """
    data = xy_data(x, y, x_err, y_err)

    fit = Fit(data=data, model_function=lin_model)
    results = fit.do_fit()
    fit.report()

    a = results['parameter_values']['a']
    b = results['parameter_values']['b']

    data_range = np.linspace(x[0], x[np.size(x) - 1], np.size(x) * 5)
    y_fit = lin_model(data_range, a, b)

    fig, ax = plt.subplots()
    ax.errorbar(x, y, fmt='x', xerr=x_err, yerr=y_err, label='Datenpunkte', color='#004287', capsize=1)
    ax.plot(data_range, y_fit, label='Fit', color='#e94653')

    ax.grid(True)
    ax.set_title(title)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)

    ax.legend()

    fig.savefig(f'370_a.pdf')

    plt.show()


a_data = np.loadtxt('a.txt')
x = a_data[:, 3]
x_err = a_data[:, 4]
durch_gamma = a_data[:, 7]
durch_gamma_err = a_data[:, 8]

x_strich = a_data[:, 5]
x_strich_err = a_data[:, 6]
gamma = a_data[:, 9]
gamma_err = a_data[:, 10]

print(x_strich)
lin_fit(durch_gamma, x, durch_gamma_err, x_err, 'Abbesches Verfahren 1', '1 + 1/gamma', 'x [cm]')
lin_fit(gamma, x_strich, gamma_err, x_strich_err, 'Abbesches Verfahren 2', '1 + gamma', 'x\' [cm]')


##
# e bis g
##


def errorbar(data):
    names = ["362.e", "362.f", "362.g 1", "362.g 2"]
    fig, ax = plt.subplots()
    x = data[:, 0]
    for n in range(4):
        print(n)
        ax.errorbar(x, data[:, n*2+1], yerr=data[:, n*2+2], label=names[n], fmt='x')

    ax.grid(True)
    ax.set_title("Beleuchtung der Punkte")
    ax.set_xlabel("Messpunkt")
    ax.set_ylabel("Ausleuchtung [lx]")

    ax.legend()

    fig.savefig(f'370_e.pdf')

    plt.show()


data = np.loadtxt("e_bis_g.txt")
errorbar(data)
