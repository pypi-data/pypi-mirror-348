#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-05-31 13:47:33.801361"
__version__ = "@COSTO_VERSION@"
# **************************************************
import pyvista as pv
import numpy as np
import mpi4py.MPI as MPI
from scipy.spatial import KDTree
import inspect
from .mesh import Imesh
from . import utils as COUT


class Iconnector(COUT.utils):
    """
    Generique connector interface
    define the methode compute_graph that is calablel only once by construction
    All child class must overwrite the _build_graph methode
    """
    def __init__(self, univers: MPI.Comm, *args, **kwds):
        super().__init__(*args, **kwds)
        self.univers = univers
        self.neibors = []
        self._is_graph_computed = False

    # @utils.call_only_once
    def compute_graph(self, *args, **kwds):
        self._build_graph(*args, **kwds)
        self._is_graph_computed = True

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def _build_graph(self, *args, **kwds):
        raise RuntimeError("Must be overide!")


class Iconnector_using_a_mesh(Iconnector):
    """
    Connector using a mesh.
    It define its dimenions, its bounding box and its center
    """
    def __init__(self,  *args, mesh: pv.UnstructuredGrid = None,  **kwds):
        super().__init__(*args, **kwds)
        self._imesh = mesh
        self.mesh: Imesh = None
        self._init_mesh()

    def _init_mesh(self):
        self._check_input_mesh_type()

    def _check_input_mesh_type(self):

        match type(self._imesh).__name__:
            case  "UnstructuredGrid":
                self.mesh = Imesh(self._imesh)
            case  "Imesh":
                self.mesh = self._imesh
            case _:
                try:
                    self.mesh = Imesh(self._imesh)
                except:
                    raise NotImplementedError("Mesh types {} is not implemented".format(type(self._imesh)))
        return


class Iconnector_using_points(Iconnector):
    """
    Connector using points and build graphe using mathcing poitns
    """
    def __init__(self,  *args, **kwds):
        super().__init__(*args, **kwds)
        self._pts = None
        self._idx_in_local_pts = {}
        self._idx_in_neibor_pts = {}

    def _set_points(self):
        raise NotImplementedError("Must be overwrited")

    def build_base(self, graph_at_node):
        un = np.unique(graph_at_node)
        un = un[un > 0].tolist()
        res = [np.binary_repr(i) for i in un]
        lst = []
        for i in res:
            lst.append(list())
            ct = len(i)-1
            for c in i:
                if int(c) > 0:
                    lst[-1].append(ct)
                ct-=1
        base = dict(zip(un, lst))
        return base


    def _exchange_points(self):
        n_proc = self.univers.Get_size()
        rank = self.univers.Get_rank()

        pts = self._pts.flatten()

        size = np.zeros(1, dtype=np.int32)
        size[0] = pts.shape[0]
        sizes = np.empty(n_proc, dtype=np.int32)
        self.univers.Allgather(size, sizes)
        max_size = np.max(sizes)

        self.all_points = self.univers.allgather(pts)
        for i, size in enumerate(sizes):
            self.all_points[i].shape = (-1, 3)

    def _compute_intersections(self):
        m_rank = self.univers.Get_rank()
        self._set_points()
        self._exchange_points()
        kdt = KDTree(self._pts)
        # TO DO UTILISER UNE BOUNDING BOX
        for rk, interf_pts in enumerate(self.all_points):
            if rk != m_rank:
                idx_in_neibors_pts, local_trace = self._compute_pts_intersection(kdt, interf_pts)

                # a sort is needed to identically  order points in each side
                to_sort = None
                if rk < m_rank:
                    to_sort = idx_in_neibors_pts
                else:
                    to_sort = local_trace
                trace_common_order = np.argsort(to_sort)

                if local_trace.shape[0] > 0:
                    self.neibors.append(rk)
                    self._idx_in_neibor_pts[rk] = idx_in_neibors_pts[trace_common_order]
                    self._idx_in_local_pts[rk] = local_trace[trace_common_order]

    def _compute_pts_intersection(self, kdt, pts):
        dist, local_trace = kdt.query(pts, eps=1e-7, distance_upper_bound=1e-3)
        idx_in_pts = np.argwhere(local_trace < kdt.n).flatten()
        local_trace = local_trace[idx_in_pts].flatten()
        return idx_in_pts, local_trace

    def _build_graph(self, *args, **kwds):
        self._compute_intersections()
        self._add_graph_fields(*args, **kwds)

    def _add_graph_fields(self, *args, **kwds):
        raise NotImplementedError("Must be overwrited")




class connect_skin_centers(Iconnector_using_points, Iconnector_using_a_mesh):
    """
    build the connection between meshes  based on the skin centers of each meshs
    To establish it, the interface of the mesh is build and its cell center are use to
    find matching element
    """
    def __init__(self,  *args, **kwds):
        super().__init__(*args, **kwds)
        self._pts = None
        self.interface = None
        self.trace_cell_centers = {}

    def _set_points(self):
        self.mesh.compute_interface_cell_centers()
        self.interface = self.mesh.interface
        self._pts = self.mesh.interface_pts

    def _add_graph_fields(self, *args, fields_racine="graph", add_individual_graphs=False,
                          build_nodal_graph=False, **kwds):

        # check that the new fields name (@cell and @ point) is not already exists
        c_keys = list(self.interface.cell_data.keys())
        p_keys = list(self.interface.point_data.keys())

        if (fields_racine in c_keys) or (fields_racine in p_keys):
            raise RuntimeError("{} already exists in the interface mesh\n\
            Known fileds are:\n\
            @cell:\n{}\n\
            @node:\n{}\n".format(fields_racine, c_keys, p_keys))

        # add a temporary field @ nodes for index
        tmp_index_name = "tmp_index"
        while tmp_index_name in p_keys:
            tmp_index_name += "_tmp"
        tmp_idx = np.arange(self.interface.number_of_points, dtype=np.int32)
        self.interface.point_data[tmp_index_name] = tmp_idx

        if build_nodal_graph:
            add_individual_graphs = True
        # add the individual and global interface connexion field @cell
        glob_connection = np.zeros(self.interface.number_of_cells, dtype=np.int32)
        for rk, idx in self._idx_in_local_pts.items():
            glob_connection[idx] += 2**rk
            if add_individual_graphs:
                connection = np.zeros(self.interface.number_of_cells, dtype=np.int32)
                connection[idx] = 1
                field_name = fields_racine+"_{}".format(rk)
                self.interface.cell_data[field_name] = connection
            self.trace_cell_centers[rk] = self.interface.cell_data[self.mesh._field_ids_name][idx]
        self.interface.cell_data[fields_racine] = glob_connection

        if build_nodal_graph:
            self._build_nodal_graph(tmp_index_name, fields_racine)

        del self.interface.point_data[tmp_index_name]
        del self.interface.cell_data[self.mesh._field_ids_name]
        del self.interface.point_data[self.mesh._field_ids_name]

        del self.mesh.cell_data[self.mesh._field_ids_name]
        del self.mesh.point_data[self.mesh._field_ids_name]

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def _build_nodal_graph(self, tmp_index_name="tmp_index", fields_racine="graph"):
        # add the global connexion field @point
        connexion_at_pts = np.zeros(self.interface.number_of_points, dtype=np.int32)
        eps = 1e-7
        for rk in self._idx_in_neibor_pts.keys():
            c_field_name = fields_racine+"_{}".format(rk)
            interf = self.interface.threshold(value=[1-eps, 1+eps], scalars=c_field_name)
            idx = interf.point_data[tmp_index_name]
            connexion_at_pts[idx] += 2**rk
        self.interface.point_data[fields_racine] = connexion_at_pts

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing


class connect_skin_points(Iconnector_using_points, Iconnector_using_a_mesh):
    """
    build the connection between meshes  based on the skin centers of each meshs
    To establish it, the interface of the mesh is build and its cell center are use to
    find matching element
    """
    def __init__(self,  *args, **kwds):
        super().__init__(*args, **kwds)
        self._pts = None
        self.interface = None
        self.traces_in_local_interface = {}
        self.traces_in_neibor_interfaces = {}
        self.traces_in_mesh = {}
        self.map_mesh_to_interface_node = None
        self.map_interface_to_mesh_node = None
        self._fields_racine = None
        self._ret = None

    def _set_points(self):
        self.mesh.build_skin()
        self.interface = self.mesh.interface
        self._pts = self.interface.points

    def _add_graph_fields(self, *args, fields_racine="graph", add_individual_graphs=False, **kwds):
        # check that the new fields name (@cell and @ point) is not already exists
        c_keys = list(self.interface.cell_data.keys())
        p_keys = list(self.interface.point_data.keys())
        # for rk in self._pts_idx.keys():
        #     field_name = fields_racine+"_{}".format(rk)
        #     if (field_name in c_keys) or (field_name in p_keys):
        #         raise RuntimeError("{} already exists in the interface mesh\n\
        #         Known fileds are:\n\
        #         @cell:\n{}\n\
        #         @node:\n{}\n".format(field_name, c_keys,p_keys))
        self._fields_racine = fields_racine

        if (fields_racine in c_keys) or (fields_racine in p_keys):
            raise RuntimeError("{} already exists in the interface mesh\n\
            Known fileds are:\n\
            @cell:\n{}\n\
            @node:\n{}\n".format(fields_racine, c_keys, p_keys))
        # add a temporary field @ nodes for index
        tmp_index_name = "tmp_index"
        while tmp_index_name in p_keys:
            tmp_index_name += "_tmp"
        tmp_idx = np.arange(self.interface.number_of_points, dtype=np.int32)
        self.interface.point_data[tmp_index_name] = tmp_idx

        mesh_ids_in_interface = self.interface.point_data[self.mesh._field_ids_name]
        # res = pv.convert_array(mesh_ids_in_interface)
        # print(res)
        # print(mesh_ids_in_interface)

        self.map_mesh_to_interface_node = dict(zip(mesh_ids_in_interface, tmp_idx))
        self.map_interface_to_mesh_node = mesh_ids_in_interface

        # # add the individual and global interface connexion field @cell
        # glob_connection = np.zeros(self.interface.number_of_cells, dtype=np.int32)
        # for rk, idx in self._pts_idx.items():
        #     glob_connection[idx] += 2**rk
        #     connection = np.zeros(self.interface.number_of_cells, dtype=np.int32)
        #     connection[idx] = 1
        #     field_name = fields_racine+"_{}".format(rk)
        #     self.interface.cell_data[field_name] = connection
        #     self.trace_cell_centers[rk] = self.interface.cell_data[self.mesh._field_ids_name][idx]

        # self.interface.cell_data[fields_racine] = glob_connection

        # add the global connexion field @point
        connexion_at_pts = np.zeros(self.interface.number_of_points, dtype=np.int32)
        eps = 1e-7
        for rk, idx_in_local_pts in self._idx_in_local_pts.items():
            if add_individual_graphs:
                connection = np.zeros(self.interface.number_of_points, dtype=np.int32)
                connection[idx_in_local_pts] = 1
                field_name = fields_racine+"_{}".format(rk)
                self.interface.point_data[field_name] = connection
            connexion_at_pts[idx_in_local_pts] += 2**rk
            self.traces_in_local_interface[rk] = idx_in_local_pts
            self.traces_in_mesh[rk] = self.interface.point_data[self.mesh._field_ids_name][idx_in_local_pts]
            self.traces_in_neibor_interfaces[rk] = self._idx_in_neibor_pts[rk]

        self.interface.point_data[fields_racine] = connexion_at_pts
        del self.interface.point_data[tmp_index_name]
        if tmp_index_name in self.interface.cell_data.keys():
            del self.interface.cell_data[self.mesh._field_ids_name]
        del self.interface.point_data[self.mesh._field_ids_name]

        if self.mesh._field_ids_name in self.mesh.cell_data.keys():
            del self.mesh.cell_data[self.mesh._field_ids_name]
        del self.mesh.point_data[self.mesh._field_ids_name]


        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def _project_connectivity_graph_by_neibors(self):
        if self._is_graph_computed is False:
            raise RuntimeError("Graph must be computed first")
        self._ret = {}
        graph_at_node = self.interface.point_data[self._fields_racine]
        self._ret["base"] = self.build_base(graph_at_node)
        # for i, trace in self.traces_in_local_interface.items():
        #     print("trace_point in local interface (neibor rank):", i, trace)

        # for i, trace in self.traces_in_neibor_interfaces.items():
        #     print("trace_point in neibor interface (neibor rank):", i, trace)

        # for i, trace in self.traces_in_mesh.items():
        #     print("trace_point in mesh id rank:", i, trace)
        #     print("trace_point in global id rank:", i, self.mesh.point_data["CHECK_GLOBAL_IDS"][trace])
        # print("base:", base)
        # print("graph:\n",graph_at_node)

        trace_in_interface_mesh = {}
        trace_in_neibor_interface = {}
        trace_in_mesh = {}
        for compo, neibors in self._ret["base"].items():
            to_take = np.array(graph_at_node == compo, dtype=bool)
            candidat = None
            if len(neibors) == 1:
                candidat = neibors[0]
            else:
                candidat = min(neibors)
            trace = self.traces_in_local_interface[candidat]
            filtre = to_take[trace]

            trace_in_interface_mesh[compo] = trace[filtre]

            trace = self.traces_in_neibor_interfaces[candidat]
            trace_in_neibor_interface[compo] = trace[filtre]

            trace = self.traces_in_mesh[candidat]
            trace_in_mesh[compo] = trace[filtre]
        self._ret["trace_in_interface_mesh"] = trace_in_interface_mesh
        self._ret["trace_in_neibor_interface"] = trace_in_neibor_interface
        self._ret["trace_in_mesh"] = trace_in_mesh

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def get_traces_and_map(self):
        if self._ret is None:
            self. _project_connectivity_graph_by_neibors()
        return self._ret


class connect_points(Iconnector_using_points):
    """
    build the connection between meshes  based on the skin centers of each meshs
    To establish it, the interface of the mesh is build and its cell center are use to
    find matching element
    """
    def __init__(self,  mesh, *args, **kwds):
        super().__init__(*args, **kwds)
        self.interface = mesh
        self.traces_in_local_interface = {}
        self.traces_in_neibor_interfaces = {}
        self._is_graph_computed = False
        self.traces_in_mesh = {}
        self._ret = None

    def _set_points(self):
        assert(type(self.interface) == pv.PolyData)
        self._pts = self.interface.points


    def _add_graph_fields(self, *args, fields_racine="graph", add_individual_graphs=False, **kwds):
        self.idx_in_neibor_pts = self._idx_in_neibor_pts
        self.idx_in_local_pts = self._idx_in_local_pts


        c_keys = list(self.interface.cell_data.keys())
        p_keys = list(self.interface.point_data.keys())
        # for rk in self._pts_idx.keys():
        #     field_name = fields_racine+"_{}".format(rk)
        #     if (field_name in c_keys) or (field_name in p_keys):
        #         raise RuntimeError("{} already exists in the interface mesh\n\
        #         Known fileds are:\n\
        #         @cell:\n{}\n\
        #         @node:\n{}\n".format(field_name, c_keys,p_keys))
        self._fields_racine = fields_racine

        if (fields_racine in c_keys) or (fields_racine in p_keys):
            raise RuntimeError("{} already exists in the interface mesh\n\
            Known fileds are:\n\
            @cell:\n{}\n\
            @node:\n{}\n".format(fields_racine, c_keys, p_keys))
        # add a temporary field @ nodes for index
        tmp_index_name = "tmp_index"
        while tmp_index_name in p_keys:
            tmp_index_name += "_tmp"
        tmp_idx = np.arange(self.interface.number_of_points, dtype=np.int32)
        self.interface.point_data[tmp_index_name] = tmp_idx

        connexion_at_pts = np.zeros(self.interface.number_of_points, dtype=np.int32)
        eps = 1e-7
        for rk, idx_in_local_pts in self._idx_in_local_pts.items():
            # if add_individual_graphs:
            #     connection = np.zeros(self.interface.number_of_points, dtype=np.int32)
            #     connection[idx_in_local_pts] = 1
            #     field_name = fields_racine+"_{}".format(rk)
            #     self.interface.point_data[field_name] = connection
            connexion_at_pts[idx_in_local_pts] += 2**rk
            self.traces_in_local_interface[rk] = idx_in_local_pts
            self.traces_in_neibor_interfaces[rk] = self._idx_in_neibor_pts[rk]

        self.interface.point_data[fields_racine] = connexion_at_pts
        del self.interface.point_data[tmp_index_name]

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing


    def _project_connectivity_graph_by_neibors(self):
        if self._is_graph_computed is False:
            raise RuntimeError("Graph must be computed first")
        self._ret = {}
        graph_at_node = self.interface.point_data[self._fields_racine]
        self._ret["base"] = self.build_base(graph_at_node)
        trace_in_neibor_interface = {}
        trace_in_mesh = {}
        for compo, neibors in self._ret["base"].items():
            to_take = np.array(graph_at_node == compo, dtype=bool)
            candidat = None
            if len(neibors) == 1:
                candidat = neibors[0]
            else:
                candidat = min(neibors)
            trace = self.traces_in_local_interface[candidat]
            filtre = to_take[trace]
            trace_in_mesh[compo] = trace[filtre]

            trace = self.traces_in_neibor_interfaces[candidat]
            # trace_in_neibor_interface[compo] = trace[filtre]


            # trace_in_mesh[compo] = np.argwhere(graph_at_node == compo).flatten()

        # self._ret["trace_in_interface_mesh"] = trace_in_interface_mesh
        # self._ret["trace_in_neibor_interface"] = trace_in_neibor_interface
        self._ret["trace_in_mesh"] = trace_in_mesh

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def get_traces_and_map(self):
        if self._ret is None:
            self. _project_connectivity_graph_by_neibors()
        return self._ret
