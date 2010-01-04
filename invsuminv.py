### Type7-Isopleths.py ###

from pynomo.nomographer import *
 
R1_params={
      'u_min':0.0,
      'u_max':1000.0,
      'function':lambda u:u,
      'title':r'\Large $R_1$',
      'text_format':r"$%4.0f$",
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
R2_params={
      'u_min':5.0,
      'u_max':1000.0,
      'function':lambda u:u,
      'title':r'\Large $R_2$',
      'text_format':r"$%4.0f$",
      'title_y_shift':0.5,
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
R1R2_params_1={
      'tag':'r1r2',
      'u_min':5.0,
      'u_max':1000.0,
      'function':lambda u:u,
      'title':r'\Large $R_1 \parallel R_2$',
      'text_format':r"$%4.0f$",
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
      'isopleth_values':[[650,900,'x']],
             }

R1R2_params_2={
      'tag':'r1r2',
      'u_min':0.0,
      'u_max':1000.0,
      'function':lambda u:u,
      'title':r'',
      'text_format':r"$%4.0f$",
      'tick_levels':0,
      'tick_text_levels':0,
             }
 
R3_params={
      'u_min':0.0,
      'u_max':1000.0,
      'function':lambda u:u,
      'title':r'\Large $R_3$',
      'text_format':r"$%4.0f$",
      'title_x_shift':-10.0,
      'tick_levels':4,
      'tick_text_levels':2,
             }
 
R1R2R3_params={
      'u_min':0.0,
      'u_max':1000.0,
      'function':lambda u:u,
      'title':r'\Large $R_1 \parallel R_2 \parallel R_3$',
      'text_format':r"$%4.0f$",
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
      'isopleth_values':[['x',600,'x']],
             }
 
main_params={
      'filename':'Type7-Isopleths.pdf',
      'paper_height':20.0,
      'paper_width':20.0,
      'block_params':[block_1_params,block_2_params],
      'transformations':[('rotate',0.01)],
      'title_x': 0.0,
      'title_y': -3.0,
      'title_box_width': 12,
      'title_str':r'\Large Equivalent Resistance of 3\
                    Resistors in Parallel',
      'extra_texts':[
            {'x':-3.5,
             'y':-3.7,
             'text':r'\large $1/R = 1/R_1 + 1/R_2 + 1/R_3$',
             'width':12.0,
            }],
      'isopleth_params':[
           {'color':'Red',
            'linewidth':'thin',
            'linestyle':'dashed',
            'circle_size':0.0,
            'transparency':0.0,
           },
           ],
              }

Nomographer(main_params)