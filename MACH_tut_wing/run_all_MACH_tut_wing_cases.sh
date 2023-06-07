#!/bin/bash


for model in 'SA' 'SST'; do
    mpirun -np 6 python run_MACH_tut_wing.py -model $model
done
