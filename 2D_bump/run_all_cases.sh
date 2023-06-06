#!/bin/bash


for i in {4..0..-1}
do
	for model in 'SA' 'SST';
	do
		mpirun -np 6 python run_2d_bump.py -level L${i} -model $model
	done
done
