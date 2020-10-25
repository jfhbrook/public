from pynomo.nomographer import *
from math import log

#xlna
this={
        'tag':'xlna',
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$x\ln(a)$',
        'tick_levels':3,
        'tick_text_levels':1,
                }
#x
isthis={
        'u_min':1,
        'u_max':10.0,
        'function':lambda u:log(u),
        'title':r'$x$',
        'tick_side':'left',
        'tick_levels':3,
        'tick_text_levels':2,
        #'scale_type':'linear smart',
                }
#a
timesthis={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:u,
        'title':r'$a$',
        'tick_levels':3,
        'tick_text_levels':1,
                }

block_1_params={
             'block_type':'type_2',
             'width':6.0,
             'height':10.0,
             'f1_params':this,
             'f3_params':isthis,
             'f2_params':timesthis,
             'mirror_y':True,
             #'mirror_x':True,
             #'isopleth_values':[[5,'x',4]],
             }
 
first={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:1+u,
        'title':r'$x\ln(a)$',
        #'title':r'',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }

second={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:(u**2.0)/2.0,
        'title':r'$x\ln(a)$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }

third={
        'u_min':0.0,
        'u_max':10.0,
        'function':lambda u:(u**3.0)/6.0,
        'title':r'$x\ln(a)$',
        'tick_levels':3,
        'tick_text_levels':2,
        'tag':'xlna',
        'scale_type':'linear smart',
                }

fourth={
        'u_min':1.0,
        'u_max':10.0,
        'function':lambda u:(u**3.0)/24.0,
        'title':r'$x\ln(a)$',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',
                }

result={
        'u_min':0.0,
        'u_max':100.0,
        'function':lambda u:-u,
        'title':r'$a^x$ (about)',
        'tick_levels':3,
        'tick_text_levels':2,
        'scale_type':'linear smart',

                }

block_2_params={
             'block_type':'type_3',
             'width':20.0,
             'height':50.0,
             'reference_titles':[r'',r''],
             'f_params':[second,third,fourth,result,first],
             'reference_padding':0.0,
             #'f_params':[first,third,result,fourth,second],
             #'f_params':[result,third,first,second,fourth],
             #'isopleth_values':[[1,4,'x']],
             }



main_params={
              'filename':'exponentiator.eps',
              'paper_width':30.0,
              'paper_height':15.0,
              'block_params':[block_1_params,block_2_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              #'title_str':r'$x\ln(a)$',
              #'title_x':4.0,
              #'title_y':2.5
              }

main_params_2={
              'filename':'exponentiator2.eps',
              'paper_width':15.0,
              'paper_height':15.0,
              'block_params':[block_2_params],
              'transformations':[('rotate',0.01),('scale paper',)],
              #'title_str':r'$x\ln(a)$',
              #'title_x':4.0,
              #'title_y':2.5
              }

Nomographer(main_params)
#Nomographer(main_params_2)
