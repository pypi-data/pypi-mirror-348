# test_windprofile_all.py

## Create a fast and robust radial profile of the tropical cyclone rotating wind from inputs Vmax, R34kt, latitude, and Vtrans.


import os
import sys

# Add parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import math

############################################################
# NHC/Best Track Operational Inputs
VmaxNHC_kt = 100  # [kt]; NHC intensity (point-max wind speed)
Vtrans_kt = 20    # [kt]
lat = 20  # [degN]; default 20N; storm-center latitude;
R34ktNHCquadmax_nautmi = (135 + 150 + 145 + 150) / 4 # average NHC R34kt radius (here 4 quadrants)
                                                        # this is the MAXIMUM radius of this wind speed in each quadrant;
                                                        # value is reduced by 0.85 below to estimate the mean radius
Penv_mb = 1008      #[mb]
## Default values: VmaxNHC_kt=100 kt, R34ktNHCquadmax_nautmi= 145.0 naut mi, lat = 20 --> unadjusted Rmax=38.1 km (sanity check)
############################################################



from tcwindprofile.windprofile_all import run_full_wind_model

tc_wind_and_pressure_profile = run_full_wind_model(
    VmaxNHC_kt=100,
    Vtrans_kt=20,
    R34kt_quad_max_nautmi=145,
    lat=20,
    Penv_mb=1008,
    plot=True
)

print(f"Rmax = {tc_wind_and_pressure_profile['Rmax_km']:.1f} km")
print(f"R0 = {tc_wind_and_pressure_profile['R0_km']:.1f} km")
print(f"Pmin = {tc_wind_and_pressure_profile['Pmin_mb']:.1f} hPa")
