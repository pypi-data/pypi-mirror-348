#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-05-31 09:39:36.902967"
__version__ = "@COSTO_VERSION@"
# **************************************************
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import numpy as np
import pyvista as pv

colorama_init()

def my_fct_decorer(fct):
    def new_fct(*args, **kwds):
        print("(inspect) -> call function", fct.__name__)
        return fct(*args, **kwds)
    return new_fct


def fct_tracer(cls):

    att_idct = cls.__dict__.items()
    fct_to_decorate = {}
    # print(list(cls.__dict__["__dict__"].items()))
    for name,val in att_idct:
        if not name.startswith("__"):
            fct_to_decorate[name] = my_fct_decorer(val)
            setattr(cls, name, my_fct_decorer(val))
    print(fct_to_decorate)
    return cls

def check_inputs(c_data, used_keys):
    """
    Check that keys exist in a dictionnray.
    A ValueError is raise if its not the case.

    Inputs:
       - c_data (dict) dictionnary in which to make the check
       - used_kyes (list) list of (potential) keys in c_data
    """
    assert type(c_data) == dict
    used_keys_ok = used_keys

    if type(used_keys) != list:
        used_keys_ok = [used_keys]

    input_keys = c_data.keys()
    for k in used_keys_ok:
        if not k in input_keys:
            raise ValueError("keys: {} is required, but not provied".format(k))
    return


class printer():
    """
    Usefull class to make beautifull print.

    Members ares:
       - mention: some additional mention in the begining of the print
       - color: the color
       - Fore: the containre of color (from colorama module)
       - print: the new print methode to use.

    Example:
    new_printer = printer()
    new_printer.mention =  "-->"
    new_printer.color = new_printer.Fore.BLUE
    new_printer.print("Coucou")
    """
    def __init__(self, mention: str =""):
        self.old_print = print
        self.mention = mention
        self.Fore = Fore
        self.color = Fore.BLUE
        self.print = self._new_print

    def _new_print(self, *args, **kwargs):
        new_args = [self.color+str(self.mention)]
        for arg in args:
            new_args.append(arg)
        new_args.append(""+Fore.RESET)
        return self.old_print(*new_args, **kwargs)


class utils():
    """
    Usefull class to drevive from that contain a do_nothing method.
    """

    def call_only_once(fct):
        """
        Use at decorer to make a function callable only once.
        """
        def new_fct(*args, **kwds):
            print("Call function", fct.__name__)
            fct(*args, **kwds)
            return
        return new_fct
        # # mecanisme to call only once this fonction
        # self_fct_name = inspect.currentframe().f_code.co_name
        # self.__dict__[self_fct_name] = self.do_nothing

    def __init__(self):
        return

    def do_nothing(self, *args, **kwds):
        """
        Methode that does nothing
        """
        return



def map_data_on_local_BC(kdt, interface, fields_to_transfert: list=[None]):
    pts = interface.cell_centers().points

    dd, ii = kdt.query(pts, eps=1e-3)
    # print(kdt.n)
    # print(dd)
    # print(pts.shape[0])
    # print(ii)
    # trace = np.argwhere( ii != kdt.n).flatten()
    trace = np.argwhere(dd < 1e-7).flatten()
    ii = ii[trace]
    for ifiled in fields_to_transfert["cell"]:
        test = np.ones(interface.number_of_cells, dtype=np.int32) * -1
        test[trace] = ifiled[1][ii]
        interface.cell_data[ifiled[0]] = test


def FindAllSubclasses(classType):
    """
    Build a list of tuple wich contain className and Class instance for each child Class of classType.

    Input:
       - classType: The mother class whose child are looked.
    """
    import sys
    import inspect
    subclasses = []
    callers_module = sys._getframe(1).f_globals['__name__']
    classes = inspect.getmembers(sys.modules[callers_module], inspect.isclass)
    for name, obj in classes:
        if (obj is not classType) and (classType in inspect.getmro(obj)):
            subclasses.append((obj, name))
    return subclasses


def compare_mesh(m1, m2, trace_cell_m1_to_m2=None, trace_point_m1_to_m2=None, use_fields_from_m1_only=False, verbose=0):
    """
    compare two pyvista meshs (if theirs differt, an assert is raised).

    Availabale mesh types are:
       - pv.core.pointset.UnstructuredGrid
       - pv.core.pointset.StructuredGrid
       - pv.core.pointset.PolyData

    can you cast it ?

    Inputs:
       - m1: mesh 1
       - m2: mesh 2
       - trace_cell_m1_to_m2: optional trace to map cell_data from m1 to m2
       - trace_point_m1_to_m2: optional trace to map poitn_data from m1 to m2
       - use_fields_from_m1_only (bool): active a mode that only check if fields from m1 exits in m2
       - verbose (bool): active / desactive verbosity
    """
    import pyvista as pv
    trace_c_set = False
    trace_p_set = False


    # --------------------------------------------------
    # global checks
    # --------------------------------------------------
    # same mesh type ?
    if not type(m1) == type(m2):
        raise RuntimeError("Mesh type differs.\n \
        \t->type mesh1: {}\n\
        \t->type mesh2: {}".format(type(m1),
                                   type(m2)))

    # type ok?
    if type(m1) not in [pv.core.pointset.UnstructuredGrid,
                        pv.core.pointset.StructuredGrid,
                        pv.core.pointset.PolyData]:
        raise NotImplementedError("Type of m1 is not available ({})\n".format(type(m1))+
        "You can try to cast them into one available type?\n"+
        "see DataSet.cast_to_unstructured_grid()\n"+
        "or DataSet.cast_to_poly_points()\n"+
        "or DataSet.cast_to_pointset() \n"+
        "https://docs.pyvista.org/api/core/_autosummary/pyvista.dataset")

    # same number of point ?
    if not m1.number_of_points == m2.number_of_points:
        raise RuntimeError("Number of point differs.\n \
        \t-> m1: {}\n\
        \t-> m2: {}".format(m1.number_of_points,
                            m2.number_of_points))

    if trace_point_m1_to_m2 is None:
        trace_p_set = True
        trace_point_m1_to_m2 = np.arange(m1.number_of_points, dtype=np.int32)

    # same number of point fields ?
    if not use_fields_from_m1_only:
        if not len(m1.point_data) == len(m2.point_data):
            raise RuntimeError("Number of point data are different\n\
            \t-> m1: {}\n\
            \t-> m2: {}".format(len(m1.point_data),
                                len(m2.point_data)
                                ))

    # same points ?
    if not np.allclose(m1.points[trace_point_m1_to_m2], m2.points):
        raise RuntimeError("Point of the meshs differs")

    # same number of cells ?
    if not m1.number_of_cells == m2.number_of_cells:
        raise RuntimeError("Number of cell are differents\n\
        \t-> m1: {}\n\
        \t-> m2: {}".format(m1.number_of_cells,
                            m2.number_of_cells
                            ))

    # same number of cells data ?
    if not use_fields_from_m1_only:
        if not len(m1.cell_data) == len(m2.cell_data):
            raise RuntimeError("Number of cell data are differents\n\
            \t-> m1: {}\n\
            \t-> m2: {}".format(len(m1.cell_data),
                                len(m2.cell_data)
                                ))


    # --------------------------------------------------

    # --------------------------------------------------
    # specifique checks (mesh type)
    # --------------------- -----------------------------
    if type(m1) is pv.core.pointset.UnstructuredGrid:
        if trace_cell_m1_to_m2 is None:
            trace_c_set = True
            trace_cell_m1_to_m2 = np.arange(m1.number_of_cells, dtype=np.int32)
        if not use_fields_from_m1_only:
            if trace_c_set is True:
                assert np.allclose(m1.cells, m2.cells)
    if type(m1) is pv.core.pointset.PolyData:
        if trace_cell_m1_to_m2 is None:
            trace_cell_m1_to_m2 = np.arange(m1.n_cells, dtype=np.int32)
        assert len(m1.faces) == len(m2.faces)
        if not use_fields_from_m1_only:
            assert np.allclose(m1.faces, m2.faces)

    # --------------------------------------------------
    # checks fields
    # --------------------------------------------------
    # @ cells
    for k in m1.cell_data:
        k1 = k
        if verbose > 0:
            print("compare {} in cell_data".format(k))
        # if k == "rhoc" or k == "F" or k == "W" or k == "M_inv":
        #     continue
        # if k == "E":
        #     k1 = "total-energy"
        assert np.allclose(m1.cell_data[k][trace_cell_m1_to_m2], m2.cell_data[k1])
    # @ points
    for k in m1.point_data:
        if verbose > 0:
            print("compare {} in point_data".format(k))
        assert np.allclose(m1.point_data[k][trace_point_m1_to_m2], m2.point_data[k])
    # --------------------------------------------------
    return
