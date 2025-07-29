#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-11-08 08:19:49.161191"
__version__ = 1.0

import costo.mesh as COM
import pyvista as pv
import numpy as np
import os
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def read(fn):
    return pv.read(os.path.join(src_dir, fn))

def test_build_map_eltype_dim():
    omega = read("00-DATA/first_order_elements.vtu")
    dims = COM.build_map_eltype_dim(mesh=omega,
                                    verbose=True)
    REF = {'LINE': {'vtktype': 3, 'dim': 1},
           'TRIANGLE': {'vtktype': 5, 'dim': 2},
           'QUAD': {'vtktype': 9, 'dim': 2},
           'TETRA': {'vtktype': 10, 'dim': 3},
           'HEXAHEDRON': {'vtktype': 12, 'dim': 3},
           'WEDGE': {'vtktype': 13, 'dim': 3}
           }
    assert dims == REF
    return


def test_build_bulk_and_interface_elt_fields():
    omega = read("00-DATA/bulk_int_msh.vtu")
    COM.build_bulk_and_interface_elt_fields(omega=omega,
                                            bulk_elt_name="bulk_elt",
                                            interface_elt_name="interface_elt",
                                            )

    omega.save("omega.vtu")
    ref = read("00-DATA/omega.vtu")
    assert np.allclose(omega.cell_data["interface_elt"],
                       ref.cell_data["interface_elt"])
    assert np.allclose(omega.cell_data["bulk_elt"],
                       ref.cell_data["bulk_elt"])

    inter_elts = omega.threshold(scalars="interface_elt", value=[0.9, 1.1])
    bulk_elts = omega.threshold(scalars="bulk_elt", value=[0.9, 1.1])
    inter_elts.save("interface.vtu")
    bulk_elts.save("tetra.vtu")
    return


def test_build_graph_partitionning():
    omega = read("00-DATA/tetra.vtu")
    COM.build_graph_partitionning(omega=omega,
                                  nb_part=2,
                                  part_name="epart",
                                  part_name_at_node="npart")
    omega.save("split.vtu")
    ref = read("00-DATA/split.vtu")
    assert np.allclose(omega.cell_data["epart"],
                       ref.cell_data["epart"])
    assert np.allclose(omega.point_data["npart"],
                       ref.point_data["npart"])


def test_extract_subdomains():
    omega = read("00-DATA/split.vtu")
    omegas = COM.extract_subdomains(omega=omega,
                                    part_name="epart")
    omegas[0].save("domain_1.vtu")
    omegas[1].save("domain_2.vtu")
    ref_dom1 = read("00-DATA/domain_1.vtu")
    ref_dom2 = read("00-DATA/domain_2.vtu")
    assert np.allclose(ref_dom1.points,
                       omegas[0].points)

    assert np.allclose(ref_dom2.points,
                       omegas[1].points)
