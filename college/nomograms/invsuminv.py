### invsuminv.py
### Adopted from http://www.myreckonings.com/pynomo11/Type7-Isopleths.py

from pynomo.nomographer import *
 
R1_params={
      'u_min':0.0,
      'u_max':10.0,
      'function':lambda u:u,
      'title':r'\Large $x_{(1,6,10\ldots)}$',
      'text_format':r"$%4.2f$",
      'title_x_shift':-0.9,
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
R2_params={
     'u_min':0.005,
      'u_max':10.0,
      'function':lambda u:u,
      'title':r'\Large $x_{(2,5,9\ldots)}$',
      'text_format':r"$%4.2f$",
      'title_x_shift':-0.5,
      'title_y_shift':0.4,
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
R1R2_params_1={
      'tag':'r1r2',
      'u_min':0.005,
      'u_max':10.0,
      'function':lambda u:u,
      'title':r'\Large $x_{(3,7,11\ldots)}$',
      'text_format':r"$%4.2f$",
      'title_x_shift':1.0,
      'title_y_shift':0.1,
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
 
block_1_params={
      'block_type':'type_7',
      'width':20.0,
      'height':20.0,
      'angle_u':60,
      'angle_v':60,
      'f1_params':R1_params,
      'f2_params':R2_params,
      'f3_params':R1R2_params_1,
      'isopleth_values':[[6.50,9.00,'x']],
             }

R1R2_params_2={
      'tag':'r1r2',
      'u_min':0.0,
      'u_max':10.0,
      'function':lambda u:u,
      'title':r'',
      'text_format':r"$%4.2f$",
      'tick_levels':0,
      'tick_text_levels':0,
             }
 
R3_params={
      'u_min':0.0,
      'u_max':10.0,
      'function':lambda u:u,
      'title':r'\Large $x_{(4,8,12\ldots)}$',
      'text_format':r"$%4.2f$",
      'title_x_shift':-9.1,
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
R1R2R3_params={
      'u_min':0.0,
      'u_max':10.0,
      'function':lambda u:u,
      'title':r'',
      'text_format':r"$%4.1f$",
      'title_x_shift':0.5,
      'title_y_shift':-4.0,
      'tick_levels':0,
      'tick_text_levels':0,
             }
 
 
block_2_params={
      'block_type':'type_7',
      'width':20.0,
      'height':20.0,
      'angle_u':60,
      'angle_v':60,
      'f1_params':R1R2_params_2,
      'f2_params':R3_params,
      'f3_params':R1R2R3_params,
      'isopleth_values':[['x',6.00,'x']],
             }
 
main_params={
      'filename':'invsuminv.eps',
      'paper_height':20.0,
      'paper_width':20.0,
      'block_params':[block_1_params,block_2_params],
      'transformations':[('rotate',0.01)],
      'title_x': 0.0,
      'title_y': -3.0,
      'title_box_width': 12,
      'title_str':r'\Large $1/x_{(1,6,10\ldots)} + 1/x_{(2,5,9\ldots)} = \
      1/x_{(3,7,11\ldots)}$',
      'extra_texts':[
            {'x':-4.9,
             'y':-3.7,
             'text':r'Useful for such calculations as \
             resistors in parallel, capacitors in series, or thermal \
             insulators (R-values) in parallel.',
             'width':10.0,
            }],
      #'isopleth_params':[
      #     {'color':'Red',
      #      'linewidth':'thin',
      #      'linestyle':'dashed',
      #      'circle_size':0.0,
      #      'transparency':0.0,
      #     },
      #     ],
              }

Nomographer(main_params)
