#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-05-31 09:41:05.625019"
__version__ = "@COSTO_VERSION@"
# **************************************************
from . import couplingData as CODA
import mpi4py.MPI as MPI
import numpy as np


def init_MPI_and_build_local_communicator(c_data:CODA.couplingData=None):
    if not MPI.Is_initialized():
        print("MPI init must be called before")
    # ATTENTION Dup => collective comms
    # c_data.comm_w = MPI.COMM_WORLD.Dup()
    c_data.comm_w = MPI.COMM_WORLD
    c_data.comm_l = c_data.comm_w.Split(c_data.color, key=0)
    c_data.rank_w = c_data.comm_w.Get_rank()
    c_data.size_w = c_data.comm_w.Get_size()
    c_data.rank_l = c_data.comm_l.Get_rank()
    c_data.size_l = c_data.comm_l.Get_size()
    c_data.is_initialize = True
    c_data.print("(global) I m {}/{}".format(c_data.rank_w+1, c_data.size_w))
    c_data.print("(local) I m {}/{}".format(c_data.rank_l+1, c_data.size_l))
    return


def recv_data(comm, src=0, tag=0):
    shape = np.zeros(3, dtype=np.int32)
    comm.Recv(shape, source=src, tag=tag)
    size = shape[0]*shape[1]+shape[2]
    data = np.zeros(size, dtype=np.double)
    comm.Recv(data, source=src, tag=tag+1)
    return data, shape


def send_data(comm, data, shape, dest=0, tag=0):
    comm.Send(shape, dest=dest, tag=tag)
    comm.Send(data, dest=dest, tag=tag+1)
    return


def finalize_MPI():
    MPI.Finalize()
# def recv_points(src=0, tag=100):
#     data, shape = recv_data(src, tag)
#     assert(shape[2] == 0)
#     data.shape = (shape[0], shape[1])

#     pts_IFS_solid = np.zeros((shape[0], 3))
#     for i in range(shape[1]):
#         pts_IFS_solid[:, i] = data[:, i]
#     return pts_IFS_solid
