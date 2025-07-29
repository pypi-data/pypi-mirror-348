#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-05-31 12:18:14.567090"
__version__ = "@COSTO_VERSION@"
# **************************************************
from . import utils as COUT
from . import pipeline as COPI
from . import connectors as COCO
from . import timeManager as COTI
from . import couplingData as CODA
import numpy as np
import inspect


class coupling(COUT.utils, ):

    def __init__(self, code_name="codex" ):
        super().__init__()
        self.code_name = code_name
        self.c_data = CODA.couplingData(self.code_name)
        self.printer = self.c_data.printer
        self.mesh = None
        self.connector_type = None
        self.connector:  COCO.Iconnector = None
        self.other_code_ranks = None
        self.others_code_ID = None
        self.same_code_ranks = None
        self.timeStepComputer = COTI.TimeStepComputer(self)

    def initialize(self):
        COPI.init_MPI_and_build_local_communicator(self.c_data)
        codes_ID = np.ones(self.c_data.size_w, dtype=np.int32)*-1
        color = np.ones(1, dtype=np.int32)*self.c_data.color
        self.c_data.comm_w.Allgather(color, codes_ID)
        self.other_code_ranks = np.argwhere(codes_ID != self.c_data.color).flatten()
        self.other_code_ranks.sort()
        self.others_code_ID = np.array(codes_ID[self.other_code_ranks])
        self.same_code_ranks = np.argwhere(codes_ID == self.c_data.color).flatten()
        self.same_code_ranks.sort()

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def set_connector_type(self, connector_type):
        self.connector_type = connector_type
        assert(self.connector_type != None)

    def set_mesh(self, mesh):
        if self.connector_type is None:
            raise NotImplementedError("You must set your a connector type before calling set_mesh")
        self.mesh = mesh
        assert(self.mesh != None)
        self.connector = self.connector_type(univers=self.c_data.comm_w, mesh=self.mesh)

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing

    def build_graph(self, *args, **kwds):
        if self.connector is None:
            raise NotImplementedError("You must set your mesh before calling build_graph")
        self.connector.compute_graph(*args, **kwds)

    def build_graph_based_on_skin_points(self, mesh):
        self.set_connector_type(COCO.connect_skin_points)
        self.set_mesh(mesh)
        self.build_graph(fields_racine="graph", add_individual_graphs=False, build_nodal_graph=True)
        res = self.connector.get_traces_and_map()
        return res

    def build_graph_based_on_cloud_points(self, mesh):
        self.set_connector_type(COCO.connect_points)
        self.set_mesh(mesh)
        self.build_graph(fields_racine="graph", add_individual_graphs=False, build_nodal_graph=True)
        res = self.connector.get_traces_and_map()
        return res

    def finalize(self):
        COPI.finalize_MPI()

    def __repr__(self):
        to_ret = ""
        to_ret += self.c_data.__repr__()
        return to_ret
