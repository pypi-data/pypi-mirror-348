#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-07-03 17:28:00.999352"
__version__ = "@COSTO_VERSION@"
# **************************************************
from .timeManager import clock

class IScheduler():
    def __init__(self, dt_seuil=1e-9):
        super().__init__()
        self._its_a_meeting_point = True
        self._dt_to_next_meeting_point = -1
        self._dt_seuil = dt_seuil
        # self.neibor_dt = 0
        # self._dtmax = 0
        # self._dtmin = 0
        self.next_meeting_point = 0
        # self.dt_guest = 0

    @property
    def is_a_meeting_point(self):
        self._dt_to_next_meeting_point = abs(self.next_meeting_point-self.get_current_time())
        if self._dt_to_next_meeting_point < self._dt_seuil:
            self._is_a_meeting_point = True
        else:
            self._is_a_meeting_point = False
        return self._is_a_meeting_point

    @is_a_meeting_point.setter
    def is_a_meeting_point(self, val):
        return

    def do_publish_action(self):
        return self.is_a_meeting_point

    def do_collect_action(self):
        # self._check_schedule()  # par securité le garder?
        return self._is_a_meeting_point

    def get_current_time(self):
        raise NotImplementedError('Must be override')

    def __repr__(self):
        to_ret = ""
        to_ret += "time to next meeting point: " + str(self._dt_to_next_meeting_point) + "\n"
        to_ret += "next meeting point: " + str(self.next_meeting_point) + "\n"
        return to_ret
