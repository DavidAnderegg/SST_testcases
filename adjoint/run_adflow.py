import os
import numpy as np
import pickle
import argparse
import ast
from mpi4py import MPI
from baseclasses import AeroProblem
from adflow import ADFLOW
from pygeo import DVGeometry, DVConstraints
from pyoptsparse import Optimization, OPT
from idwarp import USMesh
from multipoint import multiPointSparse

from adflow import ADFLOW_C
from idwarp import USMesh_C

from pyspline import Curve





input_dir = 'input'

aeroOptions = {
    # Common Parameters
    "gridFile": os.path.join(input_dir, 'mdo_tutorial_000_vol.cgns'),
    "restartFile": os.path.join(input_dir, 'mdo_tutorial_000_vol.cgns'),
    "outputDirectory": 'input',
    'equationType':'RANS',
    'useblockettes': False,

    'turbulenceModel': 'Menter SST',
    "turbResScale": [1e3, 1e-6],

    "nsubiterturb": 20,
    "useMatrixFreedrdw": False,

    # ANK
    "useANKSolver": True,
    "ANKUseTurbDADI": True,
    # "ANKADPC": True,


    "ANKSecondOrdSwitchTol": 1e-4,
    # "ANKCoupledSwitchTol": 1e-6,

    "monitorVariables": ["resrho", "totalr", "cl", "cd"],
    "L2Convergence": 1e-14,
    # "L2Convergence": 1-1e-14,
    "adjointL2Convergence": 1e-14,

    "outputSurfaceFamily": "wall",
    "nCycles": 20000,

    "adjointMaxIter": 1000,
    # "adjointSubspaceSize": 500,
    "ADPC": True,


    "solutionPrecision": "double",
    "outputSurfaceFamily": "wall",
}


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', type=str, default='adjoint',
                        help='Either "adjoint" or "complex"')
    parser.add_argument('-step_size', type=float, default=1e-40,
                        help='Step size for complex mode')
    parser.add_argument('-revFast', type=int, default=0,
                        help='use forwardPartials when 0;' + \
                                ' use reversFastPartials when 1')


    args = parser.parse_args()

    modes = ['adjoint', 'cfd', 'complex']
    if not args.mode in modes:
        print(f'"{args.mode}" is not supportd. Available modes: {modes} !')
        exit()



    idwarpOptions = {
                "gridFile": aeroOptions["gridFile"]
            }

    if not os.path.exists(aeroOptions['outputDirectory']):
        os.makedirs(aeroOptions['outputDirectory'])

    if args.revFast == 1:
        aeroOptions['useMatrixFreedrdw'] = True

    if args.mode == 'complex':
        aeroOptions['ANKCFLLimit'] = 1e40

    ap = AeroProblem(
        name="mdo_tutorial",
        alpha=1.8,
        mach=0.80,
        P=20000.0,
        T=220.0,
        areaRef=45.5,
        chordRef=3.25,
        beta=0.0,
        R=287.87,
        xRef=0.0,
        yRef=0.0,
        zRef=0.0,
        # evalFuncs=["fx", "mz", "cl", "cd", "cmz", "lift", "drag"],
        evalFuncs=['cl'],
    )

    for dv in ["alpha", "beta", "mach", "T", "xRef", "yRef", "zRef"]:
        ap.addDV(dv)

    if args.mode == 'complex':
        CFDSolver = ADFLOW_C(options=aeroOptions, debug=True)
    elif args.mode == 'adjoint':
        CFDSolver = ADFLOW(options=aeroOptions, debug=True)
    else:
        # solver normal CFD (without restart-file)
        aeroOptions['restartFile'] = None
        CFDSolver = ADFLOW(options=aeroOptions, debug=False)
        CFDSolver(ap)
        exit()



    ffd_file = os.path.join(input_dir, 'mdo_tutorial_ffd.fmt')

    if args.mode == 'complex':
        CFDSolver.setMesh(USMesh_C(options=idwarpOptions))
        CFDSolver.setDVGeo(getDVGeo(ffd_file, isComplex=True))
    else:
        CFDSolver.setMesh(USMesh(options=idwarpOptions))
        CFDSolver.setDVGeo(getDVGeo(ffd_file, isComplex=False))


    # propagates the values from the restart file throughout the code
    CFDSolver.getResidual(ap)



    # get gradients
    funcsSens = {}

    # solve comples
    if args.mode == 'complex':
        h = args.step_size

        # aero DVs
        for dv in ["alpha", "mach"]:  # defaultAeroDVs:
        # for dv in []:  # defaultAeroDVs:
            setattr(ap, dv, getattr(ap, dv) + h * 1j)

            CFDSolver.resetFlow(ap)
            CFDSolver(ap, writeSolution=False)

            funcs = {}
            CFDSolver.evalFunctions(ap, funcs)
            setattr(ap, dv, getattr(ap, dv) - h * 1j)

            for f in ap.evalFuncs:
                key = ap.name + "_" + f
                dv_key = dv + "_" + ap.name

                if not key in funcsSens:
                    funcsSens[key] = {}
                funcsSens[key][dv_key] = np.imag(funcs[key]) / h 

        # Geo DVs
        xRef = {"twist": [0.0] * 6, "span": [0.0], "shape": np.zeros(72, dtype="D")}

        for dv in ["span", "twist", "shape"]:
            xRef[dv][0] += h * 1j

            CFDSolver.resetFlow(ap)
            CFDSolver.DVGeo.setDesignVars(xRef)
            CFDSolver(ap, writeSolution=False)

            funcs = {}
            CFDSolver.evalFunctions(ap, funcs)

            xRef[dv][0] -= h * 1j

            for f in ap.evalFuncs:
                key = ap.name + "_" + f
                dv_key = dv
                funcsSens[key][dv_key] = np.imag(funcs[key]) / h
                # funcsSens[key] = {
                #         dv_key: np.imag(funcs[key]) / h
                #         }


    # solve adjoint
    else:
        CFDSolver.evalFunctionsSens(ap, funcsSens, evalFuncs=None)



    # save the functionals
    if MPI.COMM_WORLD.rank == 0:
        n_cpus = MPI.COMM_WORLD.size
        s1 = aeroOptions['turbResScale'][0]
        s2 = aeroOptions['turbResScale'][1]
        f_name = os.path.join(
                    'output',
                    f'funcSense_{args.mode}_np{n_cpus}_s1{s1}_s2{s2}'
                )

        if args.mode == 'complex':
            f_name += f'_h{h}'

        if args.mode == 'adjoint':
            if aeroOptions['useMatrixFreedrdw']:
                f_name += '_revFast'

        f_name += '.pkl'

        with open(f_name, "wb") as f:
            pickle.dump(funcsSens, f)




def getDVGeo(ffdFile, isComplex=False):
    # Setup geometry/mesh
    DVGeo = DVGeometry(ffdFile, isComplex=isComplex)

    nTwist = 6
    DVGeo.addRefAxis(
        "wing",
        Curve(
            x=np.linspace(5.0 / 4.0, 1.5 / 4.0 + 7.5, nTwist),
            y=np.zeros(nTwist),
            z=np.linspace(0, 14, nTwist),
            k=2,
        ),
    )

    def twist(val, geo):
        for i in range(nTwist):
            geo.rot_z["wing"].coef[i] = val[i]

    def span(val, geo):
        C = geo.extractCoef("wing")
        s = geo.extractS("wing")
        for i in range(len(C)):
            C[i, 2] += s[i] * val[0]
        geo.restoreCoef(C, "wing")

    DVGeo.addGlobalDV("twist", [0] * nTwist, twist, lower=-10, upper=10, scale=1.0)
    DVGeo.addGlobalDV("span", [0], span, lower=-10, upper=10, scale=1.0)
    DVGeo.addLocalDV("shape", lower=-0.5, upper=0.5, axis="y", scale=10.0)

    return DVGeo


if __name__ == '__main__':
    main()

