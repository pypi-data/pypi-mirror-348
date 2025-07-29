#     Copyright 2025, GONHXH,  find license text at end of file


""" Test tool to run a program with various Pythons. """

from Gon.PythonVersions import getSupportedPythonVersions
from Gon.utils.Execution import check_output
from Gon.utils.InstalledPythons import findPythons


def findAllPythons():
    for python_version in getSupportedPythonVersions():
        for python in findPythons(python_version):
            yield python, python_version


def executeWithInstalledPython(python, args):
    return check_output([python.getPythonExe()] + args)



