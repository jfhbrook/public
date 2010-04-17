#!/usr/bin/env python

from math import log

class heatexchanger():
    def __init__(self,T_h_in,T_h_out,T_c_in,T_c_out):
        self.T_h_in = T_h_in
        self.T_h_out = T_h_out
        self.T_c_in = T_c_in
        self.T_c_out = T_c_out

    def LMTD(self):
        delT_a = self.T_h_in-self.T_c_out
        delT_b = self.T_c_out-self.T_h_in
        return (delT_a-delT_b)/log(delT_a/delT_b)
