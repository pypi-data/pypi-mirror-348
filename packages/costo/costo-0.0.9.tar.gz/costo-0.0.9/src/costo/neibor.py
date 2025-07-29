#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-07-03 18:09:05.044015"
__version__ = "@COSTO_VERSION@"
# **************************************************
import mpi4py.MPI as MPI
import numpy as np
import inspect
from .scheduler import IScheduler

class IInternalNeibor():
    def __init__(self,
                 comm: MPI.Comm = MPI.COMM_NULL,
                 rank: int = 0,
                 # size: int = 0,
                 # dim: int = 0,
                 buff_send: np.array = None,
                 buff_recv: np.array = None,
                 ):
        self._comm = comm
        self.rank = rank
        self.Ar = None
        self.Br = None
        self._tag_send_Ar_Br = 200
        self._tag_recv_Ar_Br = 200
        self._buff_send = buff_send
        self._buff_recv = buff_recv
        self._send_reqs = 0
        self._recv_req = 0

    def _send_Ar_Br(self):
        """
        common send methode
        """
        req = self._comm.Isend(self._buff_send,
                               dest=self.rank,
                               tag=self._tag_send_Ar_Br)
        return req

    def _recv_Ar_Br(self):
        """
        common recv methode
        """
        self._recv_req = self._comm.Recv(self._buff_recv,
                                         source=self.rank,
                                         tag=self._tag_recv_Ar_Br)
        return

    def publish(self):
        self._send_reqs = self._send_Ar_Br()

    def collect(self):
        self._recv_Ar_Br()


class INeibor(IInternalNeibor):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.scheduler:IScheduler = None

    def publish(self,):
        raise NotImplementedError("You must set a scheduler first")

    def collect(self,):
        raise NotImplementedError("You must set a scheduler first")

    def set_scheduler(self, scheduler:IScheduler=None):
        self.scheduler = scheduler
        self.publish = self._publish_ok
        self.collect = self._collect_ok


    def _publish_ok(self):
        if self.scheduler.is_a_meeting_point:
            self._send_reqs = self._send_Ar_Br()

    def _collect_ok(self):
        if self.scheduler.do_collect_action():
            self._recv_Ar_Br()
