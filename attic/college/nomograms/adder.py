"""
    ex_type1_nomo_1.py
 
    Simple nomogram of type 1: F1+F2+F3=0
 
    Copyright (C) 2007-2009  Leif Roschier
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from pynomo.nomographer import *
 
N_params_1={
        'u_min':-10.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x_1$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
 
N_params_2={
        'u_min':-10.0,
        'u_max':10.0,
        'function':lambda u:-u,
        'title':r'$x_3$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
 
N_params_3={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x_2$',
        'tick_levels':2,
        'tick_text_levels':1,
                }
 
 
block_1_params={
             'block_type':'type_1',
             'width':10.0,
             'height':10.0,
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             'isopleth_values':[[1,4,'x']],
             }
 
main_params={
              'filename':'adder.eps',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$x_1+x_2=x_3$ ($x_3-x_1=x_2$)',
              'title_x':3.0,
              'title_y':7.9,
              'debug':False,
              }

Nomographer(main_params)
