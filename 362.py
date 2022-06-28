import numpy as np
import matplotlib.pyplot as plt
from kafe2 import XYContainer, Fit, Plot, ContoursProfiler


plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif'
})


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


def lin_fit(x, y, x_err, y_err, title="", x_name="", y_name="", filename=f"lin-fit"):
    """
    Function for linear fit
    :param x: values x axis
    :param y: values y axis
    :param x_err: error x axis
    :param y_err: error y axis
    :param title: string used as header
    :param x_name: string used as label for x axis
    :param y_name: string used as label for y axis
    :param filename: name your exported file
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

    fig.savefig(f'{filename}.pdf')

    plt.show()


# a_data = np.loadtxt('a.txt')
# x = a_data[:, 3]
# x_err = a_data[:, 4]
# durch_gamma = a_data[:, 7]
# durch_gamma_err = a_data[:, 8]
#
# x_strich = a_data[:, 5]
# x_strich_err = a_data[:, 6]
# gamma = a_data[:, 9]
# gamma_err = a_data[:, 10]
#
# print(x_strich)
# lin_fit(durch_gamma, x, durch_gamma_err, x_err, 'Abbesches Verfahren 1', '1 + 1/gamma', 'x [cm]', 'a_1')
# lin_fit(gamma, x_strich, gamma_err, x_strich_err, 'Abbesches Verfahren 2', '1 + gamma', 'x\' [cm]', 'a_2')


##
# e bis g
##


def errorbar(data):
    names = ["362.e", "362.f", "362.g 1", "362.g 2"]
    fig, ax = plt.subplots()
    x = data[:, 0]
    for n in range(4):
        print(n)
        ax.errorbar(x, data[:, n * 2 + 1], yerr=data[:, n * 2 + 2], label=names[n], fmt='x')

    ax.grid(True)
    ax.set_title("Beleuchtung der Punkte")
    ax.set_xlabel("Messpunkt")
    ax.set_ylabel("Ausleuchtung [lx]")

    ax.legend()

    fig.savefig(f'362_e-bis-g.pdf')

    plt.show()


# data = np.loadtxt("e_bis_g.txt")
# errorbar(data)


def colormap(datapoints, filename, min=0, max=12, colour='gray', threshhold=7.5,
             title="Beleuchtung der Messstellen [lx]"):
    names = np.array([[25, 21, 17, 13, 9, 5],
                      [24, 20, 16, 12, 8, 3.5],
                      [23, 19, 15, 11, 7, 2],
                      [22, 18, 14, 10, 6, 1]])
    x_labels = ['1', '2', '3', '4', '5', '6']
    y_labels = ['4', '3', '2', '1']

    fig, ax = plt.subplots()
    im = ax.imshow(datapoints, cmap=colour, vmin=min, vmax=max)
    cbar = ax.figure.colorbar(im, ax=ax)

    ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
    ax.set_yticks(np.arange(len(y_labels)), labels=y_labels)

    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            if datapoints[i, j] >= threshhold and names[i, j] != 3.5:
                text = ax.text(j, i, f'(\#{int(names[i, j])})\n{datapoints[i, j]}', ha="center", va="center",
                               color="black")
            else:
                if names[i, j] == 3.5:
                    if datapoints[i, j] >= threshhold:
                        text = ax.text(j, i, f'(\#{names[i, j]})\n{datapoints[i, j]}', ha="center", va="center",
                                       color="black")
                    else:
                        text = ax.text(j, i, f'(\#{names[i, j]})\n{datapoints[i, j]}', ha="center", va="center",
                                       color="w")
                else:
                    text = ax.text(j, i, f'(\#{int(names[i, j])})\n{datapoints[i, j]}', ha="center", va="center",
                                   color="white")

    ax.set_title(title)
    fig.tight_layout()
    plt.show()
    fig.savefig(filename)


e = np.loadtxt("362_e.csv")
colormap(e, f'362_e.pdf', title="Beleuchtung der Messstellen 362.e [lx]")
f = np.loadtxt("362_f.csv")
colormap(f, f'362_f.pdf', title="Beleuchtung der Messstellen 362.f [lx]")
ef = np.around(f - e, 1)
print(ef)
colormap(ef, f'362_ef.pdf', -3.6, 3.6, 'coolwarm', -5,
         title='Differenz der Werte aus Versuchsteil\n362.e und 362.f (f-e) [lx]')
g_1 = np.loadtxt("362_g-1.csv")
colormap(g_1, f'362_g-1.pdf', title="Beleuchtung der Messstellen 362.g [lx]\n(Plane Seite zur Wand)")
g_2 = np.loadtxt("362_g-2.csv")
colormap(g_2, f'362_g-2.pdf', title="Beleuchtung der Messstellen 362.g [lx]\n(Gewölbte Seite zur Wand)")
