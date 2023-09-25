#!/bin/bash

# solver convergence
python ./plot_convergence.py -save 1 -case NACA0012
python ./plot_convergence.py -save 1 -case RAE2822

# grid convergence
python ./plot_grid_convergence.py -save 1 -case 2d_bump_nan-fix
