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
    'name': f'flatplate_{state}_{args.model}',
    'resetAP': True,
    'autoRestart': False,

    'postRunCallback': save_conv_history,
}

aeroOptions = {
    'mach': 0.8, 
    'altitude': 10000, 
    'alpha': 1.5, 
    'areaRef': 45.5, 
    'chordRef':3.25,

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
    'gridFile': f'meshes/wing_vol.cgns',
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
    # 'ANKASMOverlap': 2,
    # 'ANKPCILUFill': 3,
    # 'ANKInnerPreconIts': 2,
    # 'ANKOuterPreconIts': 2,

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
