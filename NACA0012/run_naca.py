from adflow_util import ADFLOW_UTIL
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-model', type=str, default='SST',
                    help='Turbulence model to use (SST, SA)')
args = parser.parse_args()


options = {
    'name': f'n0012_{args.model}',
    'resetAP': True,
    'autoRestart': False,
}

aeroOptions = {
    'alpha': 3,
    'reynolds': 5e6,
    'mach': 0.3,
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
    'gridFile': 'n0012.cgns',
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
    "nsubiterturb": 100,



    # ANK
    "useANKSolver": True,
    "ANKUseTurbDADI": True,
    "ANKADPC": False,
    # 'anksecondordswitchtol': 1e-3,
    # 'anksecondordswitchtol': 1e-8,
    # 'ankasmoverlap': 4,
    # "outerPreconIts": 3,
    # 'ankunsteadylstol': 1.2,



    # General
    'monitorvariables':['resrho', 'resturb', 'cl','cd'],
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
