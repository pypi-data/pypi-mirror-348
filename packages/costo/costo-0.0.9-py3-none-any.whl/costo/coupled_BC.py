#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-07-03 19:08:08.435410"
__version__ = "@COSTO_VERSION@"
# **************************************************
import mpi4py.MPI as MPI
import numpy as np
import inspect
from .neibor import *

def do_nothing():
    return

class IBC():
    def __init__(self, *args, name: str = "", trace: np.array = None, **kwds):
        self.name = name
        self._trace = trace

    def _apply_header(self):
        print("apply BC {} (type: {})".format(self.name,
                                              self.__class__.__name__))
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = do_nothing

    def compute_pre_vr(self):
        """
        interface methode
        """
        raise NotImplementedError("Must be override")


    def apply_pre_vr(self):
        """
        apply the boundary condition
        """
        self._apply_header()
        self.compute_pre_vr()

    def compute_post_vr(self):
        """
        interface methode
        """
        return

    def apply_post_vr(self):
        """
        apply the boundary condition
        """
        self.compute_post_vr()

    def __repr__(self):
        to_ret = "-"*50
        to_ret += "\nBC name: " + self.name
        # to_ret += "\nrank: " + str(self._rank)
        # to_ret += "\nneibors: " + str(self.neibors_ranks)
        to_ret += "\n"+"-"*50
        return to_ret


class IInternal_BC():
    def __init__(self, *args, comm: MPI.Comm = MPI.COMM_NULL, neibors: list = None, verbose: int = 1, dim=1, nr=0, **kwds):
        self._comm = comm
        self.neibor_ranks = neibors           # rang MPI dans le comm des voisins
        self._nb_neibors = len(neibors)
        self.dim = dim
        self._nr = nr
        self.Ar = None
        self.Br = None
        self._buff_send = None
        self._buff_recv = None
        self.neibors: list(IInternalNeibor) = []
        self._allocate_arrays()
        self._insert_neibors()

        if verbose > 0:
            print(self.__repr__())
        return

    def _allocate_arrays(self):
        self.Ar = np.zeros((self._nr, self.dim, self.dim), dtype=np.double)
        self.Br = np.zeros((self._nr, self.dim), dtype=np.double)
        self._dimAr = self._nr*self.dim**2
        self._dimBr = self._nr*self.dim
        self._dimArpBr = self._dimAr+self._dimBr
        self._buff_dim_by_neibor = self._nr*(self.dim+self.dim**2) # taille de Ar + Br
        self._buff_send = np.empty((self._buff_dim_by_neibor), dtype=np.double)
        self._buff_recv = np.empty((self._nb_neibors, self._buff_dim_by_neibor), dtype=np.double)

    def _insert_neibors(self):
        for i, rank in enumerate(self.neibor_ranks):
            intNeibor = IInternalNeibor(comm=self._comm,
                                       rank=rank,
                                       # self._nr,
                                       # selfelf.dim,
                                       buff_send=self._buff_send,
                                       buff_recv=self._buff_recv[i])
            self.neibors.append(intNeibor)

    def _publish_data(self):
        for neibor in self.neibors:
            neibor.publish()

    def _collect_data(self):
        for neibor in self.neibors:
            neibor.collect()

    def _update_Ar_Br(self):
        self.cumNeibors = np.sum(self._buff_recv, axis=0)
        self.Br += self.cumNeibors[:self._dimBr].reshape(self._nr, self.dim)
        self.Ar += self.cumNeibors[self._dimBr: self._dimArpBr].reshape(self._nr, self.dim, self.dim)

    def fill_Ar_and_Br(self):
        # self.Ar[:] = self.solver.Ar[self._trace]
        # self.Br[:] = self.solver.Br[self._trace]
        raise NotImplementedError("Must Be ovverride")

    def _extract_data(self):
        self.fill_Ar_and_Br()
        self._buff_send[: self._dimBr] = self.Br.flatten()
        self._buff_send[self._dimBr:self._dimArpBr] = self.Ar.flatten()

    def _do_exchanges(self):
        self._publish_data()     # envoi son Ajr (j = self) à qui de droit (j != 1)
        self._collect_data()  # recoi les Ajr (j != self)
        self._update_Ar_Br()  # somme sur tout les Ajr sur le neoud r

    def set_new_data(self):
        # self.solver.Br[self._trace] = self.Br
        # self.solver.Ar[self._trace] = self.Ar
        raise NotImplementedError("Must Be ovverride")

    def compute_pre_vr(self):
        self._extract_data() # get local Ar and Br and fill the sendding buffer
        self._do_exchanges() # update Ar and Br from neibors and send mines
        self.set_new_data() # Apply the new Ar and Br



class ICoupled_BC(IInternal_BC):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        return

    def _insert_neibors(self):
        for i, rank in enumerate(self.neibor_ranks):
            neibor = INeibor(comm=self._comm,
                             rank=rank,
                             # self._nr,
                             # self.dim,
                             buff_send=self._buff_send,
                             buff_recv=self._buff_recv[i])
            self.neibors.append(neibor)

    def set_new_data(self):
        # self.solver.Br[self._trace] = self.Br
        # self.solver.Ar[self._trace] = self.Ar
        raise NotImplementedError("Must Be ovverride")


    def fill_Ar_and_Br(self):
        # self.Ar[:] = self.solver.Ar[self._trace]
        # self.Br[:] = self.solver.Br[self._trace]
        raise NotImplementedError("Must Be ovverride")
