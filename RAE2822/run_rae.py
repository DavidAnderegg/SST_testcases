from adflow_util import ADFLOW_UTIL
import argparse
from mpi4py import MPI
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('-model', type=str, default='SST',
                    help='Turbulence model to use (SST, SA)')
args = parser.parse_args()

with open('../current_build_state', 'r') as file:
     current_build_state = file.read().replace('\n', '')

state = f'{current_build_state}_{MPI.COMM_WORLD.Get_size()}np'

def save_conv_history(Solver, AP, n):
    hist = Solver.getConvergenceHistory()
    if MPI.COMM_WORLD.rank == 0:
        with open(f'conv_hist_{state}_{args.model}.pkl', "wb") as f:
            pickle.dump(hist, f)

options = {
    'name': f'rae2822_{state}_{args.model}',
    'resetAP': True,
    'autoRestart': False,

    'postRunCallback': save_conv_history,
}

aeroOptions = {
    'alpha': 2.92,
    'reynolds': 6.5e6,
    'mach': 0.725,
    'T': 288,

    'reynoldsLength': 1.0,
    'xRef': 0.25,
    'areaRef': 1.0,
    'chordRef': 1.0,
    'evalFuncs': ['cl','cd', 'cmz'],
}

model = None
if args.model == 'SST':
    model = 'Menter SST'
elif args.model == 'SA':
    model = 'SA'

if model is None:
    print('Selected turbulence model does not exist.')

solverOptions = {
    # Common Parameters
    'gridFile': 'rae2822.cgns',
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useblockettes': False,

    'turbulenceModel': model,
    "turbResScale": {
        'SA': 10e4,
        'SST': [1e3, 1e-6],
       }[args.model],

    "nsubiterturb": 20,

    # ANK
    "useANKSolver": True,
    "ANKADPC": True,
    "ANKNSubiterTurb": 3,
    "ANKSecondOrdSwitchTol": 1e-5,
    "ANKCoupledSwitchTol": 1e-7,
    "ANKMaxIter": 80,
    "ANKLinResMax": 0.05,

    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd', 'cmz'],
    'printIterations': True,
    'writeSurfaceSolution': True,
    'writeVolumeSolution': True,
    'outputsurfacefamily': 'wall',
    'surfacevariables': ['cp','vx', 'vy','vz', 'mach'],
    "volumeVariables": ["vort","eddy",'resrho'],
    'nCycles':20000,
    'L2Convergence':1e-14,
}

if MPI.COMM_WORLD.Get_size() == 1:
    solverOptions['ANKMaxIter'] = 35
    # solverOptions["ANKCFLLimit"] = 1e4

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
