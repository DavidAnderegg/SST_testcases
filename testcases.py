convergence_cases = {
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
# 2d bump
# #############################################
        "2d_bump_L2_nan-fix": {
            "SST_nan-fix_np6": {
                "dir": '2D_bump',
                "hist": 'conv_hist_nan-fix_6np_SST_L2.pkl',
                "model": 'SST',
                },

            "SA_nan-fix_np6": {
                "dir": '2D_bump',
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


grid_convergence_cases = {
        "2d_bump_nan-fix": {
            "ref-data": {
                "N": [901120, 225280, 56320, 14080, 3520],
                "levels": ['L00', 'L11', 'L2', 'L3', 'L4'],
                "values2plot": ['CoefLift', 'CoefDrag', 'CoefPressureDrag', 'CoefViscousDrag'],
                "names2plot": ['$C_l$', '$C_d$', '$C_{d_p}$', '$C_{d_v}$'],
                },
            "data": {
                "CFL3D": {
                    "CoefLift": [0.25042114320E-01, 0.24973567751E-01, 0.24830931115E-01, 0.24521025965E-01, 0.23545740973E-01],
                    "CoefDrag": [0.35821385120E-02, 0.35790139443E-02, 0.35811925373E-02, 0.36777912402E-02, 0.45344720607E-02],
                    "CoefPressureDrag": [0.40024315819E-03, 0.39978590512E-03, 0.41208507053E-03, 0.53646990508E-03, 0.14620096660E-02],
                    "CoefViscousDrag": [0.31818953538E-02, 0.31792280391E-02, 0.31691074667E-02, 0.31413213351E-02, 0.30724623947E-02],
                    },
                "FUN3d": {
                    "CoefLift": [0.2506589E-01, 0.2508930E-01, 0.2505324E-01, 0.2495296E-01, 0.2465064E-01],
                    "CoefDrag": [0.3573127E-02, 0.3578124E-02, 0.3575861E-02, 0.3657039E-02, 0.4202193E-02],
                    "CoefPressureDrag": [0.3992834E-03, 0.3973396E-03, 0.4077565E-03, 0.5085476E-03, 0.1096002E-02],
                    "CoefViscousDrag": [0.3173843E-02, 0.3180784E-02, 0.3168105E-02, 0.3148491E-02, 0.3106191E-02],
                    }
                },
            "plots": {
                "SST_nan-fix_np6": {
                    "dir": '2D_bump',
                    "hist": 'conv_hist_nan-fix_6np_SST_{level}.pkl',
                    "model": 'SST',
                    },

                # "SA_nan-fix_np6": {
                #     "dir": '2D_bump',
                #     "hist": 'conv_hist_nan-fix_6np_SA_{level}.pkl',
                #     "model": 'SA',
                #     }
                }
            }
        }


