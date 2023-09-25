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
    'areaRef': 2.0,
    'chordRef': 2.0,
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

    'turbulenceModel': model,
    "turbResScale": {
        'SA': 10e4,
        'SST': [1e3, 1e-6],
       }[args.model],

    "nsubiterturb": 20,

    # ANK
    "useANKSolver": True,
    "ANKSecondOrdSwitchTol": 1e-5,
    # "ANKCoupledSwitchTol": 1e-7,
    # 'ANKUnsteadyLSTol': 1.1,
    # 'ANKASMOverlap': 4,
    # 'ANKPCILUFill': 5,
    # 'ANKInnerPreconIts': 4,
    # 'ANKOuterPreconIts': 3,

    # "ANKUseTurbDADI": False,
    "ANKADPC": True,

    # "ANKCFLLimit": 1e3,
    'ANKCFlFactor': 2.,
    # 'ANKCFLCutback': 0.,

    # "ANKMaxIter": 40,
    # 'ANKLinearSolveTol': 0.025,
    # 'ANKLinResMax': 0.04,
    # "ANKLinResMax": 0.04,


    # "smoother": "DADI", 
    # "useANKSolver": False,

    # ANK
    # "ANKUseTurbDADI": True,
    # "ANKADPC": True,
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
    'nCycles':40000,
    'L2Convergence':1e-12,
}

if args.level == 'L2':
    solverOptions['ANKCFLLimit'] = 1.5e2

elif args.level == 'L1':
    solverOptions['ANKCFlFactor'] = 1.3
    solverOptions['ANKCFLExponent'] = 0.01
    # solverOptions['ANKJacobianLag'] = 2
    solverOptions['ANKCFLLimit'] = 1.0e2
    solverOptions['ANKSecondOrdSwitchTol'] = 1e-7


au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
