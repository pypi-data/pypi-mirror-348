#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-11-09 17:39:32.284214"
__version__ = 1.0

import costo.utils as  COUL
import os
import pyvista as pv
import numpy as np

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

class test_class_A():

    def __init__(self):
        self.a = 0

class test_class_B(test_class_A):

    def __init__(self):
        self.b = 0

class test_class_C(test_class_B):

    def __init__(self):
        self.c = 0

def read(fn, verbose=False):
    full_fn = os.path.join(src_dir, fn)
    if verbose:
        print(full_fn)
    return pv.read(full_fn)

def test_check_input():
    dic = {"k1": "a",
           "k2": "a"}
    COUL.check_inputs(dic, "k1")
    COUL.check_inputs(dic, "k2")
    try:
        COUL.check_inputs(dic, "k3")
    except:
        print("undifined key")
    return

def test_class_printer():
    p = COUL.printer()
    p.print("COUCOU BLUE")

    p.color  = p.Fore.GREEN
    p.print("COUCOU GREEN")
    return

def test_class_utils():
    class test_utils(COUL.utils):
        def __init__(self):
            return

    ult = COUL.utils()

    c = test_utils()
    c.do_nothing()
    c.do_nothing(1., 20, True)

    def fct_test():
        print("call fct test")

    f = test_utils.call_only_once(fct_test)
    f()
    return


def test_FindAllSubClasses():
    res = COUL.FindAllSubclasses(test_class_A)
    print(res)
    className = list(ires[1] for ires in res)
    className.sort()
    assert className == ['test_class_B', 'test_class_C']

def test_compare_mesh():
    m = read("00-DATA/first_order_elements.vtu", verbose=True)
    mp1 = pv.PolyData([[0, 0., 0.]])
    mp1.point_data["a"] = [0]
    mp1.cell_data["a"] = [0]
    COUL.compare_mesh(mp1, mp1)

    mp2 = pv.PolyData([[0, 0., 0.],
                       [1.,0.,0.]])

    mp3 = pv.PolyData([[1e-5, 0., 0.]])
    mp3.point_data["a"] = [0]
    mp3.cell_data["a"] = [0]

    mp4 = pv.PolyData([[0., 0., 0.]])
    mp4.cell_data["a"] = [0]

    mp7 = pv.PolyData([[0., 0., 0.]])
    mp7.point_data["a"] = [0]

    try:
        COUL.compare_mesh(m, mp1)
    except:
        print("Try to compare different mesh types")


    try:
        COUL.compare_mesh(None, None)
    except:
        print("Mesh type out of availlable mesh types")

    try:
        COUL.compare_mesh(mp1, mp2)
    except:
        print("Number of point are differents")

    try:
        COUL.compare_mesh(mp1, mp3)
    except:
        print("Try to compare meshs with differents Points")

    try:
        COUL.compare_mesh(mp1, mp4)
    except:
        print("Try to compare meshs with different number of point_data")


    mp5 = pv.PolyData([[0., 0., 0.],
                       [1., 0., 0.],
                       [2., 0., 0.]],lines=[2,0,1,
                                            2,1,2]
                      )
    mp6 = pv.PolyData([[0., 0., 0.],
                       [1., 0., 0.],
                       [2., 0., 0.]],lines=[2,0,1,
                                            2,1,2,
                                            2,0,2]
                      )

    try:
        COUL.compare_mesh(mp5, mp6)
    except:
        print("Try to compare mesh polydata with different number of cell")

    try:
        COUL.compare_mesh(mp1, mp7)
    except:
        print("Différent number of cell_data")


    cells = np.array([[4, 0, 1, 2, 3],
                      [4, 4, 5, 6, 7]])
    celltypes = [pv.CellType.TETRA,
                 pv.CellType.TETRA]
    points = np.array([
        [1.0, 1.0, 1.0],
        [1.0, -1.0, -1.0],
        [-1.0, 1.0, -1.0],
        [-1.0, -1.0, 1.0],
        [2.0, 1.0, 1.0],
        [2.0, -1.0, -1.0],
        [0.0, 1.0, -1.0],
        [0.0, -1.0, 1.0],
    ])

    mu1 = pv.UnstructuredGrid(cells.flatten(), celltypes, points)

    cells2 = np.array([[4, 0, 1, 2, 3],
                       [4, 4, 5, 6, 7],
                       [4, 1, 2, 3, 4]])
    celltypes2 = [pv.CellType.TETRA,
                  pv.CellType.TETRA,
                  pv.CellType.TETRA]
    mu2 = pv.UnstructuredGrid(cells2.flatten(), celltypes2, points)

    try:
        COUL.compare_mesh(mu1, mu2)
    except:
        print("Try to compare mesh unstructured with différent number of cell")

    COUL.compare_mesh(mu1, mu1)

    filed_c_1 = np.arange(mu1.number_of_cells, dtype=np.int32)
    filed_p_1 = np.arange(mu1.number_of_points, dtype=np.int32)
    mu1.cell_data["f_1"] = filed_c_1
    mu1.point_data["f_1"] = filed_p_1

    trace_c = [1, 0]
    trace_p = [4, 5, 6, 7,
               0, 1, 2, 3]

    new_pts = points[trace_p]
    new_cells = cells[trace_c]
    mu3 = pv.UnstructuredGrid(new_cells.flatten(), celltypes, new_pts)
    mu3.cell_data["f_1"] = filed_c_1[trace_c]
    mu3.point_data["f_1"] = filed_p_1[trace_p]

    COUL.compare_mesh(mu1, mu3,
                      trace_cell_m1_to_m2=trace_c,
                      trace_point_m1_to_m2=trace_p,
                      verbose=True)
    new_printer = COUL.printer()
    new_printer.mention =  "-->"
    new_printer.color = new_printer.Fore.BLUE
    new_printer.print("Coucou")

    return
