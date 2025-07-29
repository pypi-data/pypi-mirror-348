from functools import lru_cache

import ase.io
import numpy as np
from ase import Atoms
from ase.data import covalent_radii
from ase.data.colors import jmol_colors as atom_colors
from ase.neighborlist import NeighborList, natural_cutoffs
from numpy.typing import NDArray


class MoleculesReader:
    molecules: list[Atoms]
    scale: float
    path: str

    def __init__(self, path, index: str = ":"):
        self.path = path
        # TODO npz?
        mols = ase.io.read(path, index=index)
        if isinstance(mols, Atoms):
            mols = [mols]
        self.molecules = mols
        self.ase = True
        for x in mols:
            x.pbc = False

    def get_n_molecules(self) -> int:
        return len(self.molecules)

    def get_atomic_numbers(self, index: int) -> list[int]:
        atoms = self.molecules[index]
        return atoms.get_atomic_numbers()

    def get_chemical_formula(self, index: int) -> str:
        return self.molecules[index].get_chemical_formula()

    def get_n_atoms(self, index: int) -> int:
        return len(self.molecules[index])

    def get_positions(self, index: int) -> NDArray:
        atoms = self.molecules[index]
        return atoms.get_positions()

    def get_radii(self, index: int) -> NDArray:
        z = self.get_atomic_numbers(index)
        return covalent_radii[z]

    def get_spheres(self, index: int) -> tuple[float, NDArray, NDArray]:
        z = self.get_atomic_numbers(index)

        radii = covalent_radii[z]
        # colors = [f'{c[0]};{c[1]};{c[2]}' for c in atom_colors[z]]
        colors = atom_colors[z]
        r = self.get_positions(index)
        r -= np.mean(r, axis=0)

        return r, radii, colors

    @lru_cache
    def get_center(self, index):
        return np.mean(self.get_positions(index), axis=0)

    @lru_cache
    def get_bonds(self, index: int, mult: float = 0.7) -> NDArray:
        atoms = self.molecules[index]

        nl = NeighborList(natural_cutoffs(atoms, mult=mult), self_interaction=False)  # type: ignore
        nl.nl.update(False, atoms.cell, atoms.get_positions(wrap=True))
        cm = nl.get_connectivity_matrix(sparse=False)
        neighbors = np.argwhere(cm != 0)
        return neighbors
