class Tparams():
    def __init__(T_h_in,T_h_out,T_c_in,T_c_out):
        self.T_h_in = T_h_in
        self.T_h_out = T_h_out
        self.T_c_in = T_c_in
        self.T_c_out = T_c_out

    def LMTD_cf(self):
        delT_a = self.T_h_in-self.T_c_out
        delT_b = self.T_c_out-self.T_h_in
        #NOTE: Does not include F!
        return (delT_a-delT_b)/log(delT_a/delT_b)

    def T_h_avg(self):
        return 0.5*(self.T_h_in+self.T_h_out)

    def delT_h(self):
        return self.T_h_in-self.T_h_out

    def T_c_avg(self):
        return 0.5*(self.T_c_in+self.T_c_out)

    def delT_c(self):
        return self.T_c_out-self.T_c_in

    def R(self):
        return (self.T_h_in-self.T_h_out)/(T_c_out-T_c_in)

    def P(self):
        return (self.T_c_out-self.T_c_in)/(self.T_h_in-T_c_in)


def h(cp,density,dvisc,k,l,vel):
    #assumes flat plate
    re = density*vel*l/dvisc
    pr = dvisc*cp/k
    return 0.037*(re**0.8)*(pr**(1./3.))*k/l

def u(h,rsteel,asurf):
    #rsteel is thickness/ksteek
    return (2*/(h) +asurf*rsteel)**-1.
