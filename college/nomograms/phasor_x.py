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

#x_1
N_params_1={
        'u_min':0.1,
        'u_max':1.0,
        'function':lambda u:u**2,
        'title':r'$|\Re|$',
        'tick_levels':4,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }
#x_3 
N_params_2={
        'u_min':0.1,
        'u_max':sqrt(2),
        'function':lambda u:-u**2,
        'title':r'$X$',
        'tick_levels':4,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }
#x_2
N_params_3={
        'u_min':0.1,
        'u_max':1.0,
        'function':lambda u:u**2,
        'title':r'$|\Im|$',
        'tick_levels':4,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }
 
 
block_1_params={
             'block_type':'type_1',
             'width':10.0,
             'height':11.0,
             'f1_params':N_params_1,
             'f2_params':N_params_2,
             'f3_params':N_params_3,
             #'isopleth_values':[[0.5,0.5,'x']],
             }
 
main_params={
              'filename':'phasor_x.eps',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[block_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              'title_str':r'\Large$X(|\Re|,|\Im|)$',
              'title_box_width': 4,
              'title_x':3.0,
              'title_y':11.0,
              'debug':False,
              }

Nomographer(main_params)
