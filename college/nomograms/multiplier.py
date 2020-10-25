"""
    ex_type2_nomo_1.py
 
    Simple nomogram of type 2: F1=F2*F3
 
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
 
N_params_1a={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x_1$',
        'tick_levels':3,
        'tick_text_levels':1,
                }

N_params_1b={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x_1$',
        'tick_levels':3,
        'tick_text_levels':1,
                }
 
N_params_2a={
        'u_min':0.3,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x_2$',
        'tick_side':'left',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }

N_params_2b={
        'u_min':-1.0,
        'u_max':-3.0,
        'function':lambda u:u,
        'title':r'$u_2$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }
 
N_params_3a={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x_3$',
        'tick_levels':3,
        'tick_text_levels':1,
                }

N_params_3b={
        'u_min':-10.0,
        'u_max':0.0,
        'function':lambda u:u,
        'title':r'$u_3$',
        'tick_levels':3,
        'tick_text_levels':1,
                }
 

 
block_1_params={
             'block_type':'type_2',
             'width':6.0,
             'height':10.0,
             'f1_params':N_params_1a,
             'f2_params':N_params_2a,
             'f3_params':N_params_3a,
             'isopleth_values':[[9,1.5,'x']],
             }

block_2_params={
             'block_type':'type_2',
             'width':10.0,
             'height':10.0,
             'f1_params':N_params_1b,
             'f2_params':N_params_2b,
             'f3_params':N_params_3b,
             #'isopleth_values':[[9,1.5,'x']],
             }
 
main_params={
              'filename':'multiplier.eps',
              'paper_height':10.0,
              'paper_width':6.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'$x_1=x_2\times x_3$ ($x_1/x_2=x_3$)',
              'title_x':4.0,
              'title_y':2.5
              }
Nomographer(main_params)
