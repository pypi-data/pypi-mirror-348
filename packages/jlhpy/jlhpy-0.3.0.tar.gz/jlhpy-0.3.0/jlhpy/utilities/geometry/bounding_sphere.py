#!/usr/bin/env python
#
# bounding_sphere.py
#
# Copyright (C) 2020 IMTEK Simulation
# Author: Johannes Hoermann, johannes.hoermann@imtek.uni-freiburg.de
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Bounding sphere of coordinates set read from file."""

# NOTE: for serializing and deserializing snippets with
# the utilities within wf.serialize and dill, formulate
# imports as below (otherwise, the builtin __import__
# will be missing when deserializing the functions)

# NOTE: never return numpy types, always convert to standard types

# https://stackoverflow.com/questions/9452775/converting-numpy-dtypes-to-native-python-types
def as_std_type(value):
    """Convert numpy type to standard type."""
    return getattr(value, "tolist", lambda: value)()


def get_bounding_sphere_from_coordinates(coordinates):
    import miniball
    import numpy as np
    C, R_sq = miniball.get_bounding_ball(coordinates)
    R = np.sqrt(R_sq)
    # for some reason, directly returning numpy types can make troubles
    # when serializing results into database. Locally, everything worked
    # fine, but on JUWELS, numpy arrays got serialized as their string
    # representation. Numpy version-dependent?
    return as_std_type(C), as_std_type(R)


def get_bounding_sphere_from_ase_atoms(atoms):
    coordinates = atoms.get_positions()
    return get_bounding_sphere_from_coordinates(coordinates)


def get_bounding_sphere_via_ase(
        infile, format='proteindatabank'):
    import ase.io
    atoms = ase.io.read(infile, format=format)
    return get_bounding_sphere_from_ase_atoms(atoms)


def get_bounding_sphere_via_parmed(
        infile, atomic_number_replacements={}):
    """atomic_number_replacements: {str: int}."""
    import parmed as pmd
    import ase
    pmd_structure = pmd.load_file(infile)
    ase_structure = ase.Atoms(
        numbers=[
            atomic_number_replacements[str(a.atomic_number)]
            if str(a.atomic_number) in atomic_number_replacements
            else a.atomic_number for a in pmd_structure.atoms],
        positions=pmd_structure.get_coordinates(0))
    return get_bounding_sphere_from_ase_atoms(ase_structure)


def get_atom_position_via_parmed(
        infile, n, atomic_number_replacements={}):
    import parmed as pmd
    import ase
    pmd_structure = pmd.load_file(infile)
    ase_structure = ase.Atoms(
        numbers=[
            atomic_number_replacements[str(a.atomic_number)]
            if str(a.atomic_number) in atomic_number_replacements
            else a.atomic_number for a in pmd_structure.atoms],
        positions=pmd_structure.get_coordinates(0))

    # PDB / parmed indices are 1-indexed, ase indices 0-indexed
    return as_std_type(ase_structure.get_positions()[n-1, :])


def get_distance(x, y):
    import numpy as np
    return as_std_type(np.linalg.norm(np.array(x) - np.array(y)))
