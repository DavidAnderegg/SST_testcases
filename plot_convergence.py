import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse

plt.style.use('tableau-colorblind10')

from testcases import convergence_cases, turb_models

def main():

    parser = argparse.ArgumentParser() 
    parser.add_argument('-case', type=str, default='NACA0012_f1_mod',
    # parser.add_argument('-case', type=str, default='NACA0012',
    # parser.add_argument('-case', type=str, default='RAE2822',
                        help='The case to plot')
    parser.add_argument('-save', type=int, default=0,
                        help='Saves the plot when set to 1')
    args = parser.parse_args()

    # set style stuff
    mpl.rcParams['font.family'] = 'Avenir'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.linewidth'] = 2


    # create figure
    fig, axs = plt.subplots(2, 3)
    if isinstance(axs, np.ndarray):
        axs = axs.flatten()


    if not args.case in list(convergence_cases.keys()):
        print(f'{args.case} does not exist!')
        exit()


    case_name = args.case
    sub_cases = convergence_cases[case_name]

    cl_min_max = [1e3, -1e3]
    cd_min_max = [1e3, -1e3]
    cm_min_max = [1e3, -1e3]

    for sub_case_name, sub_case in sub_cases.items():

        # read convergence histor
        file_name = os.path.join(sub_case['dir'], sub_case['hist'])
        with open(file_name, 'rb') as f:
            hist = pickle.load(f)

        color=next(axs[0]._get_lines.prop_cycler)['color']

        # plot aero coefficients
        axs[0].plot(hist['CoefLift'], label=sub_case_name, color=color)
        axs[1].plot(hist['CoefDrag'], color=color)
        axs[2].plot(-hist['CoefMomentZ'], color=color)

        # save min/max on right side of plot
        cl_min_max = minmax_coef(cl_min_max, hist['CoefLift'])
        cd_min_max = minmax_coef(cd_min_max, hist['CoefDrag'])
        cm_min_max = minmax_coef(cm_min_max, -hist['CoefMomentZ'])

        # plot residuals
        axs[3].plot(np.log10(hist['RSDMassRMS']), color=color)
        n = 0
        for var_key in turb_models[sub_case['model']]["vars"]:
            axs[4+n].plot(np.log10(hist[var_key]), color=color)

            n += 1

    #set y min/max for coefficients
    cl_offset = 0.01
    cd_offset = 0.001
    cm_offset = 0.001
    axs[0].set_ylim(cl_min_max[0]-cl_offset, cl_min_max[1]+cl_offset)
    axs[1].set_ylim(cd_min_max[0]-cd_offset, cd_min_max[1]+cd_offset)
    axs[2].set_ylim(cm_min_max[0]-cm_offset, cm_min_max[1]+cm_offset)

    # format plot
    for ax in axs:
        ax.set_xlabel('Iterations')

    axs[0].set_ylabel('$C_l$')
    axs[1].set_ylabel('$C_d$')
    axs[2].set_ylabel('$C_m$')

    axs[3].set_ylabel('$log(||density||)$')
    axs[4].set_ylabel('$log(||k||)$')
    axs[5].set_ylabel('$log(||\omega||)$')

    axs[0].legend(frameon=False, fontsize=10, borderpad=1)



    s = 0.6
    fig.set_figwidth(18*s)
    fig.set_figheight(10*s)

    plt.suptitle(case_name)
    plt.tight_layout()


    if not args.save:
        plt.suptitle(args.case)
        plt.show()
    else:
        d = 'plots'
        if not os.path.exists(d):
            os.makedirs(d)

        plt.savefig(
            os.path.join(d, f'sc_{args.case}.pdf'),
            dpi=300, transparent=False, bbox_inches='tight'
        )


def minmax_coef(minmax, hist_array):
    minmax[0] = min(minmax[0], hist_array[-1])
    minmax[1] = max(minmax[1], hist_array[-1])

    return minmax


if __name__ == '__main__':
    main()
