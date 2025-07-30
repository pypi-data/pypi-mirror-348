# Copyright (C) 2013 Deutsches Zentrum fuer Luft- und Raumfahrt(DLR, German Aerospace Center) <www.dlr.de>
"""
Delismm is a pure python package for the creation of kriging-based metamodels.

It covers the following features:

- Perform parameter sensitivity analysis
- Generate Design of Experiments (DOE)
- Save/Load DOE
- Create Kriging Metamodels
- Create hierarchical kriging metamodels
- Perform a resampling to generate new Designs and improve the model
- Run DOEs using various parallelization methods local and remote


A simple example:

   >>> from delismm.example import runExample
   >>> runExample(doPlot = False)

This will create a

- doe
- sample values
- kriging model
- a diagram (if doPlot is active)


"""

from pathlib import Path

import importlib_metadata
from patme import getPyprojectMeta

name = Path(__file__).parent.name


description = ""

if Path(__file__).parts[-4] == name:
    # We have the full GitLab repository
    pkgMeta = getPyprojectMeta(__file__)
    version = str(pkgMeta["version"])
    description = str(pkgMeta["description"])
    programDir = str(Path(__file__).parents[2])
else:
    # package is installed
    version = importlib_metadata.version(name)
    programDir = str(Path(__file__).parent)
    description = importlib_metadata.metadata(name)["Summary"]
