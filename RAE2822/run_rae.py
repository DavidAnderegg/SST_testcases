from adflow_util import ADFLOW_UTIL
import argparse
from mpi4py import MPI
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('-model', type=str, default='SST',
                    help='Turbulence model to use (SST, SA)')
args = parser.parse_args()



state = f'base_{MPI.COMM_WORLD.Get_size()}np'

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
        'SST': [1e3, 1e-8],
    }[args.model],

    "nsubiter": 3,
    "nsubiterturb": 20,


    # ANK
    "useANKSolver": True,
    "ANKUseTurbDADI": True,
    "ANKADPC": False,


    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd', 'cmz'],
    'printIterations': True,
    'writeSurfaceSolution': True,
    'writeVolumeSolution': True,
    'outputsurfacefamily': 'wall',
    'surfacevariables': ['cp','vx', 'vy','vz', 'mach'],
    "volumeVariables": ["vort","eddy",'resrho'],
    'nCycles':20000,
    'L2Convergence':1e-12,
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
