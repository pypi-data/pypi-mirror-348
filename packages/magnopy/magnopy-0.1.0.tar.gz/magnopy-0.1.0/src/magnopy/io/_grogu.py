# MAGNOPY - Python package for magnons.
# Copyright (C) 2023-2025 Magnopy Team
#
# e-mail: anry@uv.es, web: magnopy.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging

import numpy as np
from wulfric.constants import TORADIANS
from wulfric.geometry import absolute_to_relative

from magnopy._spinham._hamiltonian import SpinHamiltonian
from magnopy._spinham._notation import Notation
from magnopy._spinham._parameter import get_matrix_parameter
from magnopy.constants._internal_units import ENERGY, ENERGY_NAME, LENGTH, LENGTH_NAME
from magnopy.constants.si import (
    ANGSTROM,
    BOHR_RADIUS,
    ELECTRON_VOLT,
    K_BOLTZMANN,
    RYDBERG_ENERGY,
)
from magnopy.legacy._verify_grogu import verify_model_file

_logger = logging.getLogger(__name__)


TRUE_KEYWORDS = ["true", "t", "yes", "y", "1"]
SEPARATOR = "=" * 80
SUBSEPARATOR = "-" * 80


# Save local scope at this moment
old_dir = set(dir())
old_dir.add("old_dir")


def _read_cell(lines):
    R"""
    Read information from the cell section as described in the documentation.

    Input lines have to follow the format::

        Cell <units>
        <scale>
        a_x a_y a_z
        b_x b_y b_z
        c_x c_y c_z

    where optional keywords are:

    * <units> - starts either from "b" or "a".
    * <scale> - either one float or three floats separated by at least one space.

    Parameters
    ----------
    lines : (4,) list of str
        Cell section of the input file.

    Returns
    -------
    cell : (3,3) :numpy:`ndarray`
        Scaled unit cell in the default units of magnopy (``LENGTH``). First index
        corresponds to the lattice vector, second index to the component.
    scale : (3,) :numpy:`ndarray`
        Scale factors for the lattice vectors and absolute atom coordinates.
        Index corresponds to the component.

    Notes
    -----
    It is assumed, that the input file (i.e. ``lines``) is already pre-verified and filtered.
    """

    # cell <units>
    line = lines[0].split()

    # If no <units> keyword is provided, then the default is used
    if len(line) == 1:
        _logger.info("No <units> nor <scale> keywords are detected.")
        units = LENGTH_NAME
    # If <units> keyword is provided,
    if len(line) == 2:
        # <units> keyword can be first in the keyword list. Only the <units> keyword is alphabetic.
        units = line[1]
        _logger.info(f'"{units}" keyword is detected.')

    # Process <units> keyword
    # Only those two cases are possible since the input file is pre-verified
    if units.lower().startswith("b"):
        units_conversion = BOHR_RADIUS / LENGTH
    elif units.lower().startswith("a"):
        units_conversion = ANGSTROM / LENGTH

    # First we read the cell, since we might need to know its volume
    # For the computation of the scale factor

    # If scale factor is not provided
    if len(lines) == 4:
        cell_start = 1
    # If scale factor is provided
    elif len(lines) == 5:
        cell_start = 2

    cell = np.zeros((3, 3), dtype=float)
    for i in range(cell_start, cell_start + 3):
        line = lines[i]
        cell[i - cell_start] = [float(x) for x in line.split()[:3]]
    # Convert the units to the default units of magnopy
    cell *= units_conversion

    # Process <scale> keyword if it is present
    # s
    # or
    # s_x s_y s_z
    if len(lines) == 5:
        scale = lines[1].split()
        # One scale factor is provided
        if len(scale) == 1:
            scale = float(scale[0])

            # Target the desired volume if scale is negative
            if scale < 0:
                scale = abs(scale) / abs(np.linalg.det(cell))

            scale = np.ones(3, dtype=float) * scale
        elif len(scale) == 3:
            scale = [float(x) for x in scale]
    else:
        scale = np.ones(3, dtype=float)

    _logger.info(
        f"Units conversion factor: {units_conversion}; scale factors: {' '.join([str(f) for f in scale])}"
    )

    # Apply the scale factor
    cell *= scale

    return cell, scale


def _read_atoms(lines, scale, cell):
    R"""
    Read information from the atoms section as described in the documentation.

    Input lines have to follow the format::

        Atoms <Units>
        name r1 r2 r3 ...
        ...

    Parameters
    ==========
    lines : (N,) list of str
        Atoms section of the input file.
    scale : (3,) |array-like|_
        Scale factors for the lattice vectors and absolute atom coordinates.
    cell : (3, 3) |array-like|_
        Unit cell.

    Returns
    =======
    atoms : dict
        Dictionary of atoms.

    Notes
    -----
    It is assumed, that the input file (i.e. ``lines``) is already pre-verified and filtered.
    """

    scale = np.array(scale, dtype=float)
    cell = np.array(cell, dtype=float)

    line = lines[0].lower().split()

    # Search for the <units>
    if len(line) == 2:
        units = line[1]
        _logger.info(f'"{units}" keyword is detected.')
    else:
        units = "relative"
        _logger.info(
            f"No <units> keyword is detected. Fall back to default (relative)."
        )

    # Decide the case based on <units>
    # Only three cases are possible, since the input lines are verified.
    if units.startswith("r"):
        relative = True
        units_conversion = 1
    elif units.startswith("b"):
        relative = False
        units_conversion = BOHR_RADIUS / LENGTH
    elif units.startswith("a"):
        relative = False
        units_conversion = ANGSTROM / LENGTH

    _logger.info(
        f"Units conversion factor: {units_conversion};"
        + f"coordinates are {'relative' if relative else 'absolute'}"
    )

    # Read atom's data header
    data_header = lines[1].lower().split()

    atoms = {"names": [], "positions": [], "spins": [], "charges": [], "g_factors": []}
    # Read atoms's information
    for line in lines[2:]:
        line = line.split()
        name = line[data_header.index("name")]

        # Find the coordinates
        if "r1" in data_header:
            relative = True
            _logger.info(f"Atom {name}: Relative coordinates are detected.")
            position = (
                float(line[data_header.index("r1")]),
                float(line[data_header.index("r2")]),
                float(line[data_header.index("r3")]),
            )
        else:
            relative = False
            _logger.info(f"Atom {name}: Absolute coordinates are detected.")
            x, y, z = (
                float(line[data_header.index("x")]),
                float(line[data_header.index("y")]),
                float(line[data_header.index("z")]),
            )
            position = (
                np.array([x * scale[0], y * scale[1], z * scale[2]], dtype=float)
                * units_conversion
            )
            position = absolute_to_relative(vector=position, basis=cell)

        # Find charge
        if "q" in data_header:
            charge = float(line[data_header.index("q")])
        else:
            charge = 0

        # Find g factor
        if "g" in data_header:
            g = float(line[data_header.index("g")])
        else:
            g = 2.0

        # Find spin
        if "sx" in data_header:
            spin = (
                float(line[data_header.index("sx")]),
                float(line[data_header.index("sy")]),
                float(line[data_header.index("sz")]),
            )
        elif "sp" in data_header:
            phi = float(line[data_header.index("sp")])
            theta = float(line[data_header.index("st")])
            s = float(line[data_header.index("s")])
            spin = [
                s * np.sin(theta * TORADIANS) * np.cos(phi * TORADIANS),
                s * np.sin(theta * TORADIANS) * np.sin(phi * TORADIANS),
                s * np.cos(theta * TORADIANS),
            ]
        elif "s" in data_header:
            spin = (
                0,
                0,
                float(line[data_header.index("s")]),
            )
        else:
            spin = (0, 0, 0)

        # Add atom to the Hamiltonian
        atoms["names"].append(name)
        atoms["positions"].append(position)
        atoms["spins"].append(float(np.linalg.norm(spin)))
        atoms["charges"].append(charge)
        atoms["g_factors"].append(g)

    return atoms


def _read_notation(lines):
    R"""
    Read the notation of the Hamiltonian as described in the documentation.

    Parameters
    ----------
    lines : (4,) list of str
        Notation section of the input file.

    Returns
    -------
    notation : :py:class:`.Notation`
        Notation of spin Hamiltonian.

    Notes
    -----
    It is assumed, that the input file (i.e. ``lines``) is already pre-verified and filtered.
    """
    # Skip first line with the section header
    i = 1
    while i < len(lines):
        line = lines[i]
        # Whether spins are normalized
        if line.lower().startswith("s"):
            spin_normalized = line.split()[1].lower() in TRUE_KEYWORDS
        # Whether double counting is present
        elif line.lower().startswith("d"):
            double_counting = line.split()[1].lower() in TRUE_KEYWORDS
        # Exchange factor
        elif line.lower().startswith("e"):
            exchange_factor = float(line.split()[1])
        # On-site factor
        elif line.lower().startswith("o"):
            on_site_factor = float(line.split()[1])
        i += 1
    return Notation(
        spin_normalized=spin_normalized,
        multiple_counting=double_counting,
        c21=on_site_factor,
        c22=exchange_factor,
    )


def _read_exchange(lines, spinham: SpinHamiltonian):
    R"""
    Read information from the exchange section as described in the documentation.

    Input lines have to follow the format::

        Exchange <Units>
        ----------
        bond
        ----------
        ...

    where optional keywords are:

    * <Units> - starts either from "m" or "e" or "k" or "j" or "r".

    Parameters
    ----------
    lines : (N,) list of str
        Parameters section of the input file.
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian, where the data are saved.

    Returns
    -------
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian with added bonds.

    Notes
    -----
    It is assumed, that the input file (i.e. ``lines``) is already pre-verified and filtered.
    """

    # Search for the <units>
    # Exchange <units>
    line = lines[0].lower().split()
    if len(line) >= 2:
        units = line[1]
        _logger.info(f'"{units}" keyword is detected.')
    else:
        units = "meV"
        _logger.info(f"No <units> keyword is detected. Fall back to default (meV).")

    # Decide the case based on <Units>
    # Only those cases are possible, since the input lines are pre-verified.
    if units.startswith("r"):
        units_conversion = RYDBERG_ENERGY / ENERGY
        _logger.info(
            "Exchange parameters are provided in Rydberg energy units. "
            + f"Will be converted to {ENERGY_NAME}.",
        )
    elif units.startswith("j"):
        units_conversion = 1 / ENERGY_UNITS
        _logger.info(
            "Exchange parameters are provided in Joule. "
            + f" Will be converted to {ENERGY_NAME}.",
        )
    elif units.startswith("k"):
        units_conversion = K_BOLTZMANN / ENERGY
        _logger.info(
            "Exchange parameters are provided in Kelvin. "
            + f"Will be converted to {ENERGY_NAME}.",
        )
    elif units.startswith("e"):
        units_conversion = ELECTRON_VOLT / ENERGY
        _logger.info(
            "Exchange parameters are provided in electron Volts. "
            + f"Will be converted to {ENERGY_NAME}.",
        )
    elif units.startswith("m"):
        units_conversion = 1e-3 * ELECTRON_VOLT / ENERGY
        _logger.info(
            f"Exchange parameters are provided in meV. "
            + f"Will be converted to {ENERGY_NAME}.",
        )

    _logger.info(f"Units conversion factor: {units_conversion}")

    # Skip first line with the section header
    i = 1
    while i < len(lines):
        # Skip subsection separators
        while i < len(lines) and lines[i].startswith("-" * 10):
            i += 1

        # Check if we reached the end of the file
        if i >= len(lines):
            break

        # Detect the beginning and end of the bond data
        bond_start = i
        while i < len(lines) and not lines[i].startswith("-" * 10):
            i += 1
        bond_end = i

        # Read bond and add it to the Hamiltonian
        bond = _read_bond(
            lines[bond_start:bond_end], spinham, units_conversion=units_conversion
        )

    return spinham


def _read_bond(lines, spinham: SpinHamiltonian, units_conversion=1):
    R"""
    Read information from the bond subsection as described in the documentation.

    Input lines have to follow the format::

        A1 A2 i j k
        <Isotropic Jiso>
        <Matrix
        Jxx Jxy Jxz
        Jyx Jyy Jyz
        Jzx Jzy Jzz>
        <Symmetric anisotropy Sxx Syy Sxy Sxz Syz>
        <DMI Dx Dy Dz>

    Parameters
    ----------
    lines : (N,) list of str
        Parameters section of the input file.
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian, where the data are saved.

    Returns
    -------
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian with added bond.

    Notes
    -----
    It is assumed, that the input file (i.e. ``lines``) is already pre-verified and filtered.
    """
    # Two labels and a unit cell relative position are always present,
    # since the files are pre-verified.
    line = lines[0].split()
    name1, name2 = line[:2]
    R = tuple([int(x) for x in line[2:5]])

    iso = None
    matrix = None
    symm = None
    dmi = None

    i = 1
    while i < len(lines):
        if lines[i].lower().startswith("i"):
            iso = float(lines[i].split()[1])
        if lines[i].lower().startswith("d"):
            dmi = [float(x) for x in lines[i].split()[1:]]
        if lines[i].lower().startswith("s"):
            Sxx, Syy, Sxy, Sxz, Syz = [float(x) for x in lines[i].split()[1:]]
            symm = [[Sxx, Sxy, Sxz], [Sxy, Syy, Syz], [Sxz, Syz, -Sxx - Syy]]
        if lines[i].lower().startswith("m"):
            matrix = np.zeros((3, 3), dtype=float)
            for j in range(3):
                i += 1
                matrix[j] = [float(x) for x in lines[i].split()]

        for atom_index_1 in range(len(spinham.atoms.names)):
            if spinham.atoms.names[atom_index_1] == name1:
                break
        for atom_index_2 in range(len(spinham.atoms.names)):
            if spinham.atoms.names[atom_index_2] == name2:
                break

        spinham.add_22(
            alpha=atom_index_1,
            beta=atom_index_2,
            nu=R,
            parameter=get_matrix_parameter(iso=iso, aniso=symm, dmi=dmi),
            replace=True,
        )

        i += 1
    return spinham


def _read_on_site(lines, spinham: SpinHamiltonian):
    R"""
    Read information from the on-site section as described in the documentation.

    Input lines have to follow the format::

        On-site <Units>
        ----------
        A1
        Axx Ayy Azz Axy Axz Ayz
        ----------
        ...

    where optional keywords are:

    * <Units> - starts either from "m" or "e" or "k" or "j" or "r".

    Parameters
    ----------
    lines : (N,) list of str
        Parameters section of the input file.
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian, where the data are saved.

    Returns
    -------
    spinham : :py:class:`.SpinHamiltonian`
        Spin Hamiltonian with added on-site anisotropy.

    Notes
    -----
    It is assumed, that the input file (i.e. ``lines``) is already pre-verified and filtered.
    """

    # Search for the <units>
    # On-site <units>
    line = lines[0].lower().split()
    if len(line) >= 2:
        units = line[1]
        _logger.info(f'"{units}" keyword is detected.')
    else:
        units = "meV"
        _logger.info(
            f"No <units> keyword is detected. Fall back to default ({ENERGY_NAME})."
        )

    # Decide the case based on <units>
    # Only those cases are possible, since the input lines are pre-verified.
    if units.startswith("r"):
        units_conversion = RYDBERG_ENERGY / ENERGY
        _logger.info(
            "On-site anisotropy parameters are provided in Rydberg energy units. "
            + f"Will be converted to {ENERGY_NAME}."
        )
    elif units.startswith("j"):
        units_conversion = 1 / ENERGY
        _logger.info(
            f"On-site anisotropy parameters are provided in Joule. "
            + f"Will be converted to {ENERGY_NAME}."
        )
    elif units.startswith("k"):
        units_conversion = K_BOLTZMANN / ENERGY
        _logger.info(
            f"On-site anisotropy parameters are provided in Kelvin. "
            + f"Will be converted to {ENERGY_NAME}."
        )
    elif units.startswith("e"):
        units_conversion = ELECTRON_VOLT / ENERGY
        _logger.info(
            f"On-site anisotropy parameters are provided in electron-Volts. "
            + f"Will be converted to {ENERGY_NAME}."
        )
    elif units.startswith("m"):
        units_conversion = 1e-3 * ELECTRON_VOLT / ENERGY
        _logger.info(
            f"On-site anisotropy parameters are provided in meV. "
            + f"Will be converted to {ENERGY_NAME}."
        )

    _logger.info(f"Units conversion factor: {units_conversion}")

    # Skip first line with the section header
    i = 1
    while i < len(lines):
        # Skip subsection separators
        while i < len(lines) and lines[i].startswith("-" * 10):
            i += 1

        # Check if we reached the end of the file
        if i >= len(lines):
            break

        # Read atom's label:
        atom_name = lines[i].strip()
        for atom_index in range(len(spinham.atoms.names)):
            if spinham.atoms.names[atom_index] == atom_name:
                break

        i += 1

        Axx, Ayy, Azz, Axy, Axz, Ayz = [float(lines[i].split()[j]) for j in range(6)]
        matrix = (
            np.array([[Axx, Axy, Axz], [Axy, Ayy, Ayz], [Axz, Ayz, Azz]], dtype=float)
            * units_conversion
        )

        # Pass to the next line once matrix parameters are read
        i += 1

        # Add on-site anisotropy to the Hamiltonian
        spinham.add_21(alpha=atom_index, parameter=matrix)

    return spinham


def _filter_txt_file(filename=None, lines=None, save_filtered=False):
    R"""
    Filter out all comments and blank lines from the model input file.

    Parameters
    ----------
    filename : str, optional
        Path to the file. Either ``filename`` or ``lines`` have to be provided.
    lines : list of str, optional
        Lines of the model input file. Either ``filename`` or ``lines`` have to be provided.
    save_filtered : bool, default False
        Whether to save filtered copy as a separate file.
        A name is the same as of the original file with "filtered_" added to the beginning.

    Returns
    -------
    filtered_lines : (N,) list of str
        Content of the file without comments and blank lines.
    lines_indices : (N,) list
        Indices of filtered lines in the original file.

    Raises
    ------
    ValueError
        If neither ``filename`` nor ``lines`` are provided.
        If both ``filename`` and ``lines`` are provided.

    """

    # Verify input parameters
    if filename is None and lines is None:
        raise ValueError("Either filename or lines have to be provided.")

    if filename is not None and lines is not None:
        raise ValueError("Only one of filename or lines can be provided.")

    # Read the content of the file if lines are not provided
    if lines is None:
        # Read the content of the file
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

    # Filtered lines
    filtered_lines = []
    # Original line indices
    line_indices = []

    # Filter comments and blank lines
    for l_i, line in enumerate(lines):
        # Remove comment lines
        if line.startswith("#"):
            continue
        # Remove inline comments and leading/trailing whitespaces
        line = line.split("#")[0].strip()
        # Remove empty lines
        if line:
            filtered_lines.append(line)
            line_indices.append(l_i + 1)

    # Save filtered copy of the file
    if save_filtered:
        filtered_filename = f"filtered_{filename}"
        with open(filtered_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_lines))
        _logger.debug(
            f"Filtered input file is saved in {os.path.abspath(filtered_filename)}"
        )

    # Return filtered lines and original line indices
    # for the line filtered_lines[i] the original line index is line_indices[i]
    return filtered_lines, line_indices


def load_grogu(filename, save_filtered=False, verbose=False) -> SpinHamiltonian:
    r"""
    Load a SpinHamiltonian object from a .txt file produced by GROGU.

    Parameters
    ----------
    filename : str
        Filename to load SpinHamiltonian object from.
    save_filtered : bool
        Whether to save the pre-processed file.
    verbose : bool, default False
        Whether to output verbose comments on the progress.

    Returns
    -------
    spinham :py:class:`.SpinHamiltonian`
        SpinHamiltonian object loaded from file.
    """

    # Read the content of the file
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines, indices = _filter_txt_file(filename=filename, save_filtered=save_filtered)

    # Verify input
    sections = verify_model_file(
        lines, indices, raise_on_fail=True, return_sections=True
    )

    # Read notation
    notation = _read_notation(lines=lines[slice(*sections["notation"])])

    # Read the cell
    cell, scale = _read_cell(lines=lines[slice(*sections["cell"])])

    # Read atoms
    atoms = _read_atoms(lines=lines[slice(*sections["atoms"])], scale=scale, cell=cell)

    # Construct spin Hamiltonian:
    spinham = SpinHamiltonian(notation=notation, cell=cell, atoms=atoms)

    # If present read on-site parameters
    if "on-site" in sections:
        _read_on_site(lines=lines[slice(*sections["on-site"])], spinham=spinham)

    # If present read exchange parameters
    if "exchange" in sections:
        _read_exchange(lines=lines[slice(*sections["exchange"])], spinham=spinham)

    return spinham


# Populate __all__ with objects defined in this file
__all__ = list(set(dir()) - old_dir)
# Remove all semi-private objects
__all__ = [i for i in __all__ if not i.startswith("_")]
del old_dir
