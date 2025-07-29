#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-06-28 23:09:27.064258"
__version__ = "@COSTO_VERSION@"
# **************************************************
from . import utils as COUT


class couplingData():
    def __init__(self, code_name):
        __slots__ = ("code_name","color","printer","print","is_initialize","rank_l",
                     "rank_w","size_l","size_w","comm_l","comm_w")
        self.code_name = code_name
        self.color = sum([ord(c) for c in self.code_name])
        self.printer = COUT.printer(mention="({})".format(self.code_name))
        self.print = self.printer.print
        self.is_initialize = False
        self.rank_l = -1
        self.rank_w = -1
        self.size_l = -1
        self.size_w = -1
        self.comm_l = None
        self.comm_w = None

    def __repr__(self):
        to_ret = ""
        to_ret += "code name: {}\n".format(self.code_name)
        to_ret += "associated ID: {}\n".format(self.color)
        if self.is_initialize:
            to_ret += "rank world: {}\n".format(self.rank_w)
            to_ret += "rank local: {}\n".format(self.rank_l)
            to_ret += "size world communicator: {}\n".format(self.size_w)
            to_ret += "size local communicator: {}\n".format(self.size_l)
        return to_ret
