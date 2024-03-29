import pickle
import argparse
import os
from tabulate import tabulate
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-np', type=str, default=6,
                        help='Number of cpus to compare')
    args = parser.parse_args()


    output_dir = 'output'
    if not os.path.exists(output_dir):
        output_dir = os.path.join('adjoint', output_dir)

    n_significant_digits = 10

    cases = {
            "complex_np6_h1e-200": {
                    "file_name": os.path.join(
                        output_dir, f'funcSense_complex_np6_h1e-200.pkl'
                        # output_dir, f'funcSense_adjoint_np6_.pkl'
                        ),
                },

            "complex_np6": {
                    "file_name": os.path.join(
                        output_dir, f'funcSense_complex_np6_h1e-40.pkl'
                        # output_dir, f'funcSense_adjoint_np6_.pkl'
                        ),
                },



            "adjoint_np6": {
                    "file_name": os.path.join(
                        output_dir, f'funcSense_adjoint_np6_s11000.0_s21e-06.pkl'
                        ),
                },

            # "adjoint_np6_v2": {
            #         "file_name": os.path.join(
            #             output_dir, f'funcSense_adjoint_np6_s110000.0_s21e-10.pkl'
            #             ),
            #     },


            "adjoint_np1": {
                    "file_name": os.path.join(
                        output_dir, f'funcSense_adjoint_np1_s11000.0_s21e-06.pkl'
                        ),
                },

            "adjoint_np6_revFast": {
                    "file_name": os.path.join(
                        output_dir, f'funcSense_adjoint_np6_s11000.0_s21e-06_revFast.pkl'
                        ),
                },

            }

    base_case = 'complex_np6_h1e-200'

    # load deriv data
    for case_name, case in cases.items():
        with open(case["file_name"], 'rb') as f:
            case['funcsSens'] = pickle.load(f)




    table = list()

    # compare derivs
    for func_name in cases[base_case]['funcsSens'].keys():
        table.append([func_name])

        for dv_name in cases[base_case]['funcsSens'][func_name].keys():
            desvars = cases[base_case]['funcsSens'][func_name][dv_name]
            if not isinstance(desvars, np.ndarray):
                desvars = [[desvars]]

            # loop if desvar is array
            for m in range(len(desvars[0])):
                dv_name_full = dv_name + str(m)


                # iterate through all cases and gather values
                values = list()
                for case in cases.values():
                    try: 
                        value = case['funcsSens'][func_name][dv_name]
                    except KeyError:
                        continue

                    if isinstance(value, np.ndarray):
                        value = value[0][m]

                    values.append(value)

                    if len(values) >= 2:
                        # add absolute diff
                        values.append(
                                values[-1] - values[0]
                                )

                        # add relative diff
                        values.append(
                                values[-1] / values[0]
                                )

                table.append([
                    dv_name_full, *values
                    ])


    header = ['variable / function']
    n = 0
    for case_name in cases.keys():
        header.append(case_name)

        if n >= 1:
            header.append('Abs diff')
            header.append('Rel diff')

        n += 1




    print(
            tabulate(table, headers=header)
            )





    # compare funcs



if __name__ == '__main__':
    main()

