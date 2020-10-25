from numpy import arange,array
from pylab import *

c_c=arange(1.0,10.0,0.1) #critical damping (x)

figure(figsize = (4,8) )
plot(1.0/c_c, c_c,  'k', \
     2.0/c_c,c_c,   'k', \
     3.0/c_c, c_c,  'k', \
     4.0/c_c, c_c,  'k', \
     5.0/c_c, c_c,  'k', \
     6.0/c_c, c_c,  'k', \
     7.0/c_c, c_c,  'k', \
     8.0/c_c, c_c,  'k', \
     9.0/c_c, c_c,  'k', )

#text(3.5,0.65,r'$\omega_n$',fontsize=24)
xlim(0.0,1.0)
grid(True)
ylabel(r'$c_c$')
xlabel(r'$\zeta$')
subplot(111)
twinx()
ylim(1.0,10.0)
savefig('vibes2.eps')

########################


#damped frequency (y)
def wd_pts(wn,dr_pts):
    return wn*sqrt(1-dr_pts**2)

figure()
dr_pts=arange(0.0,1,0.01) #damping ratio (x)

semilogx(wd_pts(0.3,dr_pts),dr_pts,  'k', \
     wd_pts(0.5,dr_pts),dr_pts,  'k', \
     wd_pts(1.0,dr_pts),dr_pts,  'k', \
     wd_pts(1.5,dr_pts),dr_pts,  'k', \
     wd_pts(2.0,dr_pts),dr_pts,  'k',\
     wd_pts(2.5,dr_pts),dr_pts,  'k', \
     wd_pts(3.0,dr_pts),dr_pts,  'k', \
     wd_pts(3.5,dr_pts),dr_pts,  'k', \
     wd_pts(4.0,dr_pts),dr_pts,  'k',)

xlim(0.1,10)
text(0.25,0.17,r'0.3')
text(0.5,0.17,r'0.5')
text(1.0,0.18,r'1.0')
text(1.5,0.2,r'1.5')
text(2.0,0.25,r'2.0')
text(2.4,0.31,r'2.5')
text(2.8,0.41,r'3.0')
text(3.1,0.51,r'3.5')
text(3.3,0.6,r'4.0')
text(3.5,0.65,r'$\omega_n$',fontsize=24)
grid(True)
xlabel(r'$\omega_d$')
ylabel(r'$\zeta$')
savefig('vibes3.eps')

#########################'''
