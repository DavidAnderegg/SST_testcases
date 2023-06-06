import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-case', type=str, default='NACA0012_f1_mod',
                        help='The case to plot')
    args = parser.parse_args()



    cases = {
    # #############################################
    # NACA 0012
    # #############################################

            "NACA0012": {
                "SST_base_np6": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_base_6np_SST.pkl',
                    "model": 'SST',
                    },
                "SST_base_np1": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_base_1np_SST.pkl',
                    "model": 'SST',
                    },


                "SA_base_np6": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_base_6np_SA.pkl',
                    "model": 'SA',
                    },
                "SA_base_np1": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_base_1np_SA.pkl',
                    "model": 'SA',
                    },
                },


            "NACA0012_f1_mod": {
                "SST_base_np6": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_base_6np_SST.pkl',
                    "model": 'SST',
                    },
                "SST_base_np1": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_base_1np_SST.pkl',
                    "model": 'SST',
                    },


                "SST_f1_mod_np1": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_f1_mod_1np_SST.pkl',
                    "model": 'SST',
                    },
                "SST_f1_mod_np6": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_f1_mod_6np_SST.pkl',
                    "model": 'SST',
                    },
                 "SST_f1_mod_np12": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_f1_mod_12np_SST.pkl',
                    "model": 'SST',
                    },
                 "SST_f1_mod_np24": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_f1_mod_24np_SST.pkl',
                    "model": 'SST',
                    },
                 "SST_f1_mod_np48": {
                    "dir": 'NACA0012',
                    "hist": 'conv_hist_f1_mod_48np_SST.pkl',
                    "model": 'SST',
                    },

               },


    # #############################################
    # RAE 2822
    # #############################################
            "RAE2822": {
                "SST_base_np6": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_base_6np_SST.pkl',
                    "model": 'SST',
                    },
                "SST_base_np1": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_base_1np_SST.pkl',
                    "model": 'SST',
                    },


                "SA_base_np6": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_base_6np_SA.pkl',
                    "model": 'SA',
                    },
                "SA_base_np1": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_base_1np_SA.pkl',
                    "model": 'SA',
                    },
                },

            "RAE2822_f1_mod": {
                "SST_base_np6": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_base_6np_SST.pkl',
                    "model": 'SST',
                    },
                "SST_base_np1": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_base_1np_SST.pkl',
                    "model": 'SST',
                    },


                "SST_f1_mod_np6": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_f1_mod_6np_SST.pkl',
                    "model": 'SST',
                    },
                "SST_f1_mod_np1": {
                    "dir": 'RAE2822',
                    "hist": 'conv_hist_f1_mod_1np_SST.pkl',
                    "model": 'SST',
                    },
                },

    # #############################################
    # flatplate
    # #############################################
            "flatplate_L2_nan-fix": {
                "SST_nan-fix_np6": {
                    "dir": 'flatplate',
                    "hist": 'conv_hist_nan-fix_6np_SST_L2.pkl',
                    "model": 'SST',
                    },
                "SST_nan-fix_np1": {
                    "dir": 'flatplate',
                    "hist": 'conv_hist_nan-fix_1np_SST_L2.pkl',
                    "model": 'SST',
                    },

                "SA_nan_fix_np6": {
                    "dir": 'flatplate',
                    "hist": 'conv_hist_nan-fix_6np_SA_L2.pkl',
                    "model": 'SA',
                    },
                },


    # #############################################
    # MACH_tut_wing
    # #############################################
            "wing_nan-fix": {
                "SST_nan-fix_np6": {
                    "dir": 'MACH_tut_wing',
                    "hist": 'conv_hist_nan-fix_6np_SST.pkl',
                    "model": 'SST',
                    },

                "SA_nan_fix_np6": {
                    "dir": 'MACH_tut_wing',
                    "hist": 'conv_hist_nan-fix_6np_SA.pkl',
                    "model": 'SA',
                    },
                },

            }

    turb_models = {
            "SST": {
                "vars": ['RSDTurbulentEnergyKineticRMS', 'RSDTurbulentDissRateRMS']
                },
            "SA": {
                "vars": ['RSDTurbulentSANuTildeRMS']
                },
            }



    # create figure
    fig, axs = plt.subplots(2, 3)
    if isinstance(axs, np.ndarray):
        axs = axs.flatten()


    if not args.case in list(cases.keys()):
        print(f'{args.case} does not exist!')
        exit()


    case_name = args.case
    sub_cases = cases[case_name]

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

    axs[3].set_ylabel('log(RSDMassRMS)')
    axs[4].set_ylabel('log(RSDTurbVar1RMS)')
    axs[5].set_ylabel('log(RSDTurbVar2RMS)')

    axs[0].legend()


    fig.set_figwidth(18)
    fig.set_figheight(10)

    plt.suptitle(case_name)
    plt.tight_layout()
    plt.show()

def minmax_coef(minmax, hist_array):
    minmax[0] = min(minmax[0], hist_array[-1])
    minmax[1] = max(minmax[1], hist_array[-1])

    return minmax


if __name__ == '__main__':
    main()
