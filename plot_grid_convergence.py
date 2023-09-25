import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math 
import os
import argparse
import pickle

plt.style.use('tableau-colorblind10')

from testcases import grid_convergence_cases, turb_models


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-case', type=str, default='2d_bump_nan-fix',
    # parser.add_argument('-case', type=str, default='flatplate_nan-fix',
                    help='The Test-case to plot')
    parser.add_argument('-save', type=int, default=0,
                        help='Saves the plot when set to 1')
    args = parser.parse_args()

    # set style stuff
    mpl.rcParams['font.family'] = 'Avenir'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.linewidth'] = 2

    case = grid_convergence_cases[args.case]

    N = np.array(case['ref-data']['N'])
    h = 1/N**(1/2)


    # figure out plot isze
    n_values2plot = len(case['ref-data']['values2plot'])
    s = 1.5
    fig = plt.figure(figsize=(6.4*s, 4.8*s), layout='tight')
    n_fig = math.ceil(math.sqrt(n_values2plot))
    axs = fig.subplots(n_fig, n_fig)
    axs = axs.flatten()

    # Edit the major and minor ticks of the x and y axes
    for ax in axs:
        ax.xaxis.set_tick_params(which='major', size=10, width=1.5, direction='in')
        ax.yaxis.set_tick_params(which='major', size=10, width=1.5, direction='in')
        ax.xaxis.set_tick_params(which='minor', size=7, width=1, direction='in')
        ax.yaxis.set_tick_params(which='minor', size=7, width=1, direction='in')


    # plot ADflow values
    for plot_name, plot_data in case['plots'].items():
        values2plot = np.ones((n_values2plot, len(N))) * np.nan

        for n in range(len(case['ref-data']['levels'])):
            level = case['ref-data']['levels'][n]

            # read convergence history
            file_name = os.path.join(
                    plot_data['dir'], 
                    plot_data['hist'].format(level=level)
                    )
            try: 
                with open(file_name, 'rb') as f:
                    hist = pickle.load(f)

            except FileNotFoundError:
                hist = None
                continue

            for m in range(n_values2plot):
                values2plot[m][n] = hist[case['ref-data']['values2plot'][m]][-1]

        # actually plot
        for m in range(n_values2plot):
            axs[m].plot(h, values2plot[m, :], '-+', label=plot_name)

    # plot comparision data
    for plot_name, plot_data in case['data'].items():
        for m in range(n_values2plot):
            axs[m].plot(
                    h, plot_data[case['ref-data']['values2plot'][m]], 
                    '--+', label=plot_name
                    )


    n = 0
    for ax in axs:
        ax.set_xlabel('$\\sqrt{\\frac{1}{N}}$', labelpad=5)
        ax.set_xlim(0, None)
        ax.set_ylim(
                case['ref-data']['min2plot'][n],
                case['ref-data']['max2plot'][n],
                )

        n += 1

    # adjust plot
    for m in range(n_values2plot):
        axs[m].set_ylabel(case['ref-data']['names2plot'][m])

    axs[0].legend(frameon=False, fontsize=10, borderpad=1)

    if not args.save:
        plt.suptitle(args.case)
        plt.show()
    else:
        d = 'plots'
        if not os.path.exists(d):
            os.makedirs(d)

        plt.savefig(
            os.path.join(d, f'gc_{args.case}.pdf'),
            dpi=300, transparent=False, bbox_inches='tight'
        )



if __name__ == '__main__':
    main()
