from adflow_util import ADFLOW_UTIL
import argparse
import os
import numpy as np


def solveAdjoint(solver, ap, n):
    funcsSens = {}
    # DVCon.evalFunctionsSens(funcsSens)
    solver.evalFunctionsSens(ap, funcsSens)
    solver.checkAdjointFailure(ap, funcsSens)


defaultFuncList = [
    "lift",
    "drag",
    "cl",
    "cd",
    "fx",
    "fy",
    "fz",
    "cfx",
    "cfy",
    "cfz",
    "mx",
    "my",
    "mz",
    "cmx",
    "cmy",
    "cmz",
    "sepsensor",
    "sepsensoravgx",
    "sepsensoravgy",
    "sepsensoravgz",
]

options = {
    'name': "mdo_tutorial",
    'autoRestart': False,
    # "postRunCallback": solveAdjoint
}

aeroOptions = {
        'alpha': 1.8,
        'mach': 0.80,
        'P': 20000.0,
        'T': 220.0,
        'areaRef':45.5,
        'chordRef':3.25,
        'beta':0.0,
        'R':287.87,
        'xRef':0.0,
        'yRef':0.0,
        'zRef':0.0,
        'evalFuncs':defaultFuncList,
}

solverOptions = {
    # Common Parameters
    'gridFile': 'mdo_tutorial_rans.cgns',
    # 'restartFile': 'output/mdo_tutorial_vol.cgns',
    'outputDirectory':'output',

    # Physics Parameters
    'equationType':'RANS',
    'useblockettes': False,

    'turbulenceModel': 'Menter SST',
    "turbResScale": [1e3, 1e-6],

    "nsubiterturb": 20,
    "useMatrixFreedrdw": False,


    # ANK
    "useANKSolver": True,
    "ANKUseTurbDADI": True,
    "ANKADPC": True,

    "ANKSecondOrdSwitchTol": 1e-4,
    "ANKCoupledSwitchTol": 1e-6,

    "monitorVariables": ["resrho", "totalr", "cl", "cd"],
    "L2Convergence": 1e-14,
    "adjointL2Convergence": 1e-14,

    "solutionPrecision": "double",
    "outputSurfaceFamily": "wall",
}

au = ADFLOW_UTIL(aeroOptions, solverOptions, options)
au.run()
