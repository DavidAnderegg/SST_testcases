#!/bin/bash

for i in '1' '2' '6' '12' '24' '48'; do
    for model in 'SA' 'SST'; do
        mpirun -np $i --oversubscribe python run_naca.py -model $model
    done
done


