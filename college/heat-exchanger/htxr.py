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


class Htxrparams():
    def __init__(lx,ly,lz_0,del_lz,As_plate,del_W,density):
        self.lx=lx
        self.ly=ly
        self.lz_0=lz_0
        self.del_lz=del_lz
        self.As_plate=As_plate
        self.del_W=del_W
        self.density=density

    def t_plate(self):
        return self.del_W/density/As_plate

    def t_gap(self):
        return self.del_lz-self.t_plate

    def lz(self,N):
        return self.lz_0+self.del_lz*N
