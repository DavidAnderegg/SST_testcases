from adflow_util import ADFLOW_UTIL
import argparse
from mpi4py import MPI
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('-model', type=str, default='SST',
                    help='Turbulence model to use (SST, SA)')
parser.add_argument('-level', type=str, default='L4',
                    help='The grid level to use')

args = parser.parse_args()

with open('../current_build_state', 'r') as file:
     current_build_state = file.read().replace('\n', '')

state = f'{current_build_state}_{MPI.COMM_WORLD.Get_size()}np'

def save_conv_history(Solver, AP, n):
    hist = Solver.getConvergenceHistory()
    if MPI.COMM_WORLD.rank == 0:
        with open(f'conv_hist_{state}_{args.model}_{args.level}.pkl', "wb") as f:
            pickle.dump(hist, f)

def preRunCallBack(solver, ap, n):
    ap.setBCVar("Pressure", 1013e2, "out")

options = {
    'name': f'flatplate_{state}_{args.model}_{args.level}',
    'resetAP': True,
    'autoRestart': False,

    'preRunCallBack':  preRunCallBack,
    'postRunCallback': save_conv_history,
}

aeroOptions = {
    'alpha': 0,
    'T': 300, # 540 rankine
    'P': 1013e2,
    'V': 78.554,

    'reynoldsLength': 1.0,
    'xRef': 0.25,
    'areaRef': 1.5,
    'chordRef': 1.5,
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
    'gridFile': f'meshes/flatplate_{args.level}.cgns',
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useblockettes': False,
    'liftIndex': 3,

    'turbulenceModel': model,
    "turbResScale": {
        'SA': 10e4,
        'SST': [1e3, 1e-8],
    }[args.model],

    "nsubiter": 3,
    "nsubiterturb": 20,

    # "smoother": "DADI", 
    # "useANKSolver": False,

    # ANK
    "ANKUseTurbDADI": True,
    "ANKADPC": True,
    'ANKASMOverlap': 2,
    'ANKPCILUFill': 3,
    'ANKInnerPreconIts': 2,
    'ANKOuterPreconIts': 2,

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
