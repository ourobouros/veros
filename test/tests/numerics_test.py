from collections import OrderedDict
import numpy as np
import sys

from test_base import VerosUnitTest
from veros.core import numerics

class NumericsTest(VerosUnitTest):
    nx, ny, nz = 70, 60, 50
    extra_settings = {
                        "enable_cyclic_x": True,
                        "coord_degree": False,
                     }
    def initialize(self):
        m = self.veros_legacy.main_module

        #np.random.seed(123456)
        for a in ("x_origin", "y_origin"):
            self.set_attribute(a,np.random.rand())

        for a in ("dxt","dxu","xt","xu"):
            self.set_attribute(a,1 + 100*np.random.rand(self.nx+4))

        for a in ("dyt","dyu","yt","yu"):
            self.set_attribute(a,1 + 100*np.random.rand(self.ny+4))

        for a in ("dzt","dzw","zw","zt"):
            self.set_attribute(a,np.random.rand(self.nz))

        for a in ("cosu","cost","tantr"):
            self.set_attribute(a,2*np.random.rand(self.ny+4)-1.)

        for a in ("coriolis_t", "area_u", "area_v", "area_t"):
            self.set_attribute(a,np.random.randn(self.nx+4,self.ny+4))

        for a in ("salt", "temp"):
            self.set_attribute(a,np.random.rand(self.nx+4, self.ny+4, self.nz, 3))

        kbot = np.random.randint(0, self.nz, size=(self.nx+4,self.ny+4))
        self.set_attribute("kbot",kbot)

        self.test_module = numerics
        veros_args = (self.veros_new,)
        veros_legacy_args = dict()
        self.test_routines = OrderedDict()
        for r in ("calc_grid", "calc_topo", "calc_beta", "calc_initial_conditions"):
            self.test_routines[r] = (veros_args, veros_legacy_args)


    def test_passed(self,routine):
        all_passed = True
        for f in ("zt","zw","cosu","cost", "tantr", "area_u", "area_v", "area_t",
                  "beta", "xt", "xu", "dxu", "dxt", "yt", "yu", "dyu", "dyt", "dzt",
                  "dzw", "rho", "salt", "temp", "Nsqr", "Hd", "int_drhodT", "int_drhodS",
                  "ht", "hu", "hv", "hur", "hvr", "maskT", "maskW", "maskU", "maskV", "kbot"):
            passed = self.check_variable(f)
            if not passed:
                all_passed = False
        return all_passed

if __name__ == "__main__":
    passed = NumericsTest().run()
    sys.exit(int(not passed))
