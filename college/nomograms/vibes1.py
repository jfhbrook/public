#free vibes w/ viscous damping, underdamped

from pynomo.nomographer import *

spr_const={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:sqrt(u),
        'title':r'$k$',
        'tick_levels':3,
        'tick_text_levels':1,
                }

mass_1={
        'tag': 'mass_1',
        'u_min':0.3,
        'u_max':4.0,
        'function':lambda u:sqrt(u),
        'title':r'$m$',
        'tick_side':'left',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }

mass_2={
        'u_min':0.3,
        'u_max':4.0,
        'function':lambda u:2*u,
        'title':r'$m$',
        'title':r'',
        'tick_side':'right',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }

omega_n_1={
        'tag':'omega_n',
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$\omega_n$',
        'tick_levels':3,
        'tick_text_levels':2,
                }

omega_n_2={
        'tag':'omega_n',
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'',
        'tick_levels':0,
        'tick_text_levels':0,
                }

c_crit_1={
        'tag':'ccrit',
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$c_{c}$',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side': 'left'
                }

block_omega_n_params={
             'block_type':'type_2',
             'width':10.0,
             'height':10.0,
             'f1_params':spr_const,
             'f2_params':mass_1,
             'f3_params':omega_n_1,
             'isopleth_values':[[9,1.5,'x']],
             }

block_c_crit_params={
             'block_type':'type_2',
             'width':16.0,
             'height':10.0,
             'f1_params':c_crit_1,
             'f2_params':mass_2,
             'f3_params':omega_n_2,
             'mirror_y': True,
             'isopleth_values':[['x',1.5,2.45]],
             }

main_params_1={
              'filename':'vibes1.eps',
              'paper_height':8.0,
              'paper_width':10.5,
              'block_params':[block_omega_n_params,
                              block_c_crit_params,
                             ],
              'transformations':[('rotate',0.0),('scale paper',)],
              #'title_str':r'Free Vibration with Viscous Damping',
              #'title_x':7.0,
              #'title_y':2.5
              }

#Nomographer(main_params_1)

#########################

ratio={
        'u_min':0.1,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'the ratio',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'log smart'
                }

xnot={
        'u_min':0.1,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'$x_0$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'log smart'
                }

xdotnot={
        'u_min':0.1,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'$\dot{x_0}$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'log smart'
                }
 
 
ratio_1_params={
             'block_type':'type_1',
             'width':10.0,
             'height':10.0,
             'f3_params':ratio,
             'f1_params':xnot,
             'f2_params':xdotnot,
             'isopleth_values':[[1.0,'x',1.5]],
             }
 
main_params_2={
              'filename':'vibes4.eps',
              'paper_height':10.0,
              'paper_width':5.0,
              'block_params':[ratio_1_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              #'title_str':r'$x_1+x_2=x_3$ ($x_3-x_1=x_2$)',
              #'title_x':3.0,
              #'title_y':7.9,
              }

#Nomographer(main_params_2)

#########################

ratio_2={
        'tag':'ratio_2',
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'',
        'tick_levels':0,
        'tick_text_levels':0,
        'scale_type':'manual line',
        'reference': True
                }

omega_d={
        'u_min':0.1,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'$\omega_d$',
        'tick_levels':3,
        'tick_text_levels':2,
        'tick_side':'left',
        'scale_type':'log smart'
                }

omega_n_3={
        'u_min':0.1,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'$\omega_n$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'log smart'
                }
 
 
ratio_2_params={
             'block_type':'type_1',
             'width':10.0,
             'height':10.0,
             'f3_params':ratio_2,
             'f1_params':omega_d,
             'f2_params':omega_n_3,
             'isopleth_values':[[1.0,0.6,'x']],
             'mirror_x':True,
             'mirror_y':True
             }

ratio_2_2={
        'tag':'ratio_2',
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'',
        'tick_levels':0,
        'tick_text_levels':0,
        'scale_type':'manual line',
        'reference': True
                }

damping_ratio_2={
        'u_min':0.01,
        'u_max':1.0,
        'function':lambda u:log(u),
        'title':r'$\zeta$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'log smart'
                }

ratio_3={
        'u_min':0.01,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'',
        'tick_levels':2,
        'tick_text_levels':1,
        'scale_type':'log smart'
                }

ratio_3_params={
             'block_type':'type_1',
             'width':10.0,
             'height':10.0,
             'f3_params':ratio_2_2,
             'f1_params':damping_ratio_2,
             'f2_params':ratio_3,
             'isopleth_values':[[1.0,0.6,'x']],
             'mirror_x':True,
             'mirror_y': False #True
             }

 
main_params_3={
              'filename':'vibes4.eps',
              'paper_height':10.0,
              'paper_width':10.0,
              'block_params':[ratio_2_params,ratio_3_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              #'title_str':r'$x_1+x_2=x_3$ ($x_3-x_1=x_2$)',
              #'title_x':3.0,
              #'title_y':7.9,
              }

Nomographer(main_params_3)
