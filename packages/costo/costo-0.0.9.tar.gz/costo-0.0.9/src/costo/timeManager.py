#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-06-26 08:16:48.772672"
__version__ = "@COSTO_VERSION@"
# **************************************************

import numpy as np
import inspect
from . import utils as COUT
import mpi4py.MPI as MPI

class clock():
    __slots__ = ("_time")

    def __init__(self, *args, t0=0.,**kwds):
        self._time = float(t0)

    @property
    def time(self):
        """
        return the time
        """
        return self._time

    @time.setter
    def time(self, val):
        raise RuntimeError("Time can't be set, use reset or increment")

    def increment(self, dt):
        """
        increment the time
        """
        self._time += float(dt)

    def reset(self, t):
        """
        reset the clock to time t
        """
        self._time = float(t)


class ItimeStepStrategy():
    def __init__(self,  *args, **kwds):
        self.name = self.__class__.__name__
        self.cpl = None

    def set_cpl(self,cpl):
        self.cpl = cpl
        print("cpl:", self.cpl.c_data)

    def get_next_dt(self, *args, **kwds):
        raise NotImplementedError("Must be override")
        # self._max_dt_local = self.c_data.comm_l.allreduce(dt, op=MPI.MIN)

    def __repr__(self):
        to_ret = "Strategy class used is: "+ str(self.name)
        to_ret +="\n "
        return to_ret

class useTheSmallestConstrain(ItimeStepStrategy):
    def __init__(self, *args, **kwds):
        super().__init__(self)
        self._dt = 0

    def get_next_dt(self,  *args, max_dt_local=0, **kwds):
        self._dt = self.cpl.c_data.comm_w.allreduce(max_dt_local, op=MPI.MIN)
        return self._dt


class CoupledTimeStepComputer(ItimeStepStrategy,clock):
    def __init__(self, *args, **kwds):
        ItimeStepStrategy.__init__(self, *args, **kwds)
        clock.__init__(self, *args, **kwds)
        self.next_meeting_point = 0
        self.dt_eps = 1e-9
        self.dt_local_max = 0
        self._delta_close = 0.5
        self.all_dt_max = []
        self.all_other_dt_max = []
        self._is_fist_call = True
        self.dt = 0

    def get_next_dt(self, max_dt_local):
        self.dt = self._compute_dt(max_dt_local)
        self.increment(self.dt)
        return self.dt, self.next_meeting_point

    def _compute_dt(self, max_dt_local):
        self.dt_local_max = self.cpl.c_data.comm_l.allreduce(max_dt_local, op=MPI.MIN)
        if (self._is_fist_call):
            self._is_fist_call = False
            return self._determine_next_meeting_point()

        dt_to_next_meeting_point = self.next_meeting_point - self.time

        if dt_to_next_meeting_point < self.dt_eps:
            # there is a meeting points
            return self._determine_next_meeting_point()
        else:
            # continue until next meeting points

            if self.dt_local_max < dt_to_next_meeting_point:
                # advance with the largest available time step
                return self.dt_local_max
            else:
                # adapt last time step to reach next meeting point
                return dt_to_next_meeting_point


    def _determine_next_meeting_point(self):
        # communication globale possible au début
        self.all_dt_max = self.cpl.c_data.comm_w.allgather(self.dt_local_max)
        self.all_dt_max = np.array(self.all_dt_max)
        self.all_other_dt_max = np.unique(self.all_dt_max[self.cpl.other_code_ranks])
        assert(len(self.all_other_dt_max) == 1)
        all_time_step_ratio = self.all_dt_max/self.dt_local_max
        trace_less_one_ratio = np.argwhere(all_time_step_ratio <= 1)
        unify_time_step = all_time_step_ratio.copy()
        unify_time_step[trace_less_one_ratio] = 1/all_time_step_ratio[trace_less_one_ratio]

        ratio = self.all_other_dt_max[0]/self.dt_local_max
        if ratio <= 1:
            ratio = 1/ratio
        print("time step ratio: ", ratio, ", time: ", self.time)
        rank_close = []
        if (abs(ratio-1) < self._delta_close):
            rank_close = [-1]
        dt = 0
        if len(rank_close) > 0:
            # use same time step
            dt = np.min(self.all_dt_max)
            self.next_meeting_point = dt*1.0 + self.time
        else:
            max_dt = np.max(self.all_dt_max)
            min_dt = np.min(self.all_dt_max)
            if abs(self.dt_local_max - max_dt)/max_dt < self.dt_eps:
                dt = max_dt
            else:
                dt = min_dt
            self.next_meeting_point = max_dt + self.time
        return dt


class TimeStepComputer(COUT.utils):
    def __init__(self, cpl, *args, **kwds):
        self.cpl = cpl
        self.timeStepStrategy: ItimeStepStrategy = None
        self._is_time_step_strategie_set = False

    def get_next_dt(self, *args, **kwds):
        raise RuntimeError("You must set a strategy to compute time step")

    def set_strategy(self, *args, timeStepStrategy:ItimeStepStrategy = None, **kwds):
        subclasses = COUT.FindAllSubclasses(ItimeStepStrategy)
        subclasseNames = [subclasse[1] for subclasse in subclasses]
        if not (timeStepStrategy.__name__ in subclasseNames):
            raise NotImplementedError("Given strategy (class {}) is not available.\nAvailable candidat are:\n--> {}".format(timeStepStrategy.__name__ , "\n--> ".join(subclasseNames)))


        strategies = self.cpl.c_data.comm_w.allgather(timeStepStrategy.__name__)
        uniqueStrategy = np.unique(np.array(strategies))
        if len(uniqueStrategy) > 1:
            raise NotImplementedError("All code must use the same strategy to compute time step\n Current strategies ares {}".format(uniqueStrategy))
        self.timeStepStrategy = timeStepStrategy()
        self.timeStepStrategy.set_cpl(self.cpl)
        self.__dict__["get_next_dt"] = self.timeStepStrategy.get_next_dt
        self._is_time_step_strategie_set = True

        # mecanisme to call only once this fonction
        self_fct_name = inspect.currentframe().f_code.co_name
        self.__dict__[self_fct_name] = self.do_nothing
