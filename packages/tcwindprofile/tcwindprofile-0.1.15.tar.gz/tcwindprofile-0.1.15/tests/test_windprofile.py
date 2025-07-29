# test_windprofile.py

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


# # Define input parameters
# Vmaxmean_ms = 45.8           # [m/s]
# Rmax_km = 38.1              # [km]
# R34ktmean_km = 228.3        # [km]
# lat = 20                      # [degrees]
############################################################


############################################################
# Unit conversions to MKS
ms_per_kt = 0.5144444   # 1 kt = 0.514444 m/s
km_nautmi = 1.852
VmaxNHC_ms = VmaxNHC_kt * ms_per_kt
Vtrans_ms = Vtrans_kt * ms_per_kt
R34ktNHCquadmax_m_temp = km_nautmi * R34ktNHCquadmax_nautmi * 1000 #[m]

# Additional conversions
fac_R34ktNHCquadmax2mean = 0.85  #Eq 1 of CKK25 -- simple estimate of mean R34kt radius from NHC R34kt (which is maximum radius of 34kt); factor originally from DeMaria et al. (2009)
R34ktmean_km = R34ktNHCquadmax_m_temp * fac_R34ktNHCquadmax2mean / 1000 #[km]

Vmaxmean_ms = VmaxNHC_ms - 0.55 * Vtrans_ms
###############################################################


###############################################################
# Estimate Rmax from Vmax, R34kt, and latitude
### Source: Chavas D.R. and J. A.. Knaff (2022). A simple model for predicting the tropical cyclone radius of maximum wind from outer size. Wea. For., 37(5), pp.563-579
### https://doi.org/10.1175/WAF-D-21-0103.1

from tcwindprofile.tc_rmax_estimatefromR34kt import predict_Rmax_from_R34kt

Rmax_estimate_km = predict_Rmax_from_R34kt(
        VmaxNHC_ms=VmaxNHC_ms,
        R34ktmean_km=R34ktmean_km,
        lat=lat
    )
print(f"Estimated Rmax = {Rmax_estimate_km:.1f} km")
# print(f"Estimated Rmax = {Rmax_estimate_nautmi:.1f} naut mi")
###############################################################

###############################################################
# Estimate Pmin from Vmax, R34kt, latitude, translation speed, Penv
### Source: Chavas D.R., Knaff J.A. and P. Klotzbach  (2025). A Simple Model for Predicting Tropical Cyclone Minimum Central Pressure from Intensity and Size. Wea. For., 40(2), pp.333-346
### https://doi.org/10.1175/WAF-D-24-0031.1

from tcwindprofile.tc_pmin_estimatefromR34kt import predict_Pmin_from_R34kt

Pmin_estimate_mb, dP_estimate_mb = predict_Pmin_from_R34kt(
        VmaxNHC_ms=VmaxNHC_ms,
        R34ktmean_km=R34ktmean_km,
        lat=lat,
        Vtrans_ms=Vtrans_ms,
        Penv_mb=Penv_mb
    )
print(f"Estimated Pmin = {Pmin_estimate_mb:.1f} mb")
print(f"Estimated dP = {dP_estimate_mb:.1f} mb")
###############################################################


###############################################################
# Retrieve estimated outer radius R0 ONLY
# (If you dont need the entire wind profile)

from tcwindprofile.tc_outer_radius_estimate import estimate_outer_radius

V34kt_ms = 34 * ms_per_kt           # [m/s]; outermost radius to calculate profile
R34ktmean_m = R34ktmean_km * 1000
omeg = 7.292e-5  # Earth's rotation rate
fcor = 2 * omeg * math.sin(math.radians(abs(lat)))  # [s^-1]
R0 = estimate_outer_radius(R34ktmean_m=R34ktmean_m, V34kt_ms=V34kt_ms, fcor=fcor)
print(f"Estimated R0 = {R0/1000:.1f} km")



###############################################################
# Create wind profile
## Create a fast and robust radial profile of the tropical cyclone rotating wind from inputs Vmax, R34kt, Rmax, and latitude.
#### This code uses a modified‐Rankine vortex between Rmax and R34kt and the E04 model beyond R34kt (and a quadratic profile inside the eye). It is very similar to the full physics-based wind profile model of Chavas et al. (2015) ([code here](http://doi.org/10.4231/CZ4P-D448)), but is simpler and much faster.
#### It is designed to guarantee that the profile fits both Rmax and R34kt and will be very close to the true outer radius (R0) as estimated by the full E04 outer solution. Hence, it is very firmly grounded in the known physics of the tropical cyclone wind field while also matching the input data. It is also guaranteed to be very well‐behaved for basically any input parameter combination.
#### Model basis:
#### Modified Rankine profile between Rmax and R34kt was shown to compare very well against high-quality subset of Atlantic Best Track database -- see Fig 8 of [Klotzbach et al. (2022, JGR-A)](https://doi.org/10.1029/2022JD037030)
#### Physics-based non-convecting wind field profile beyond R34kt was shown to compare very well against entire QuikSCAT database -- see Fig 6 of [Chavas et al. (2015, JAS)](https://doi.org/10.1175/JAS-D-15-0014.1)
#### Quadratic in the eye (U-shape is common)

from tcwindprofile import generate_wind_profile

Rmax_km = Rmax_estimate_km
# Rmax_km = 38.1
rr_km, vv_ms, R0_estimate_km = generate_wind_profile(
    Vmaxmean_ms=Vmaxmean_ms,
    Rmax_km=Rmax_km,
    R34ktmean_km=R34ktmean_km,
    lat=lat,
    plot=True
)
print(f"Estimated R0 = {R0_estimate_km:.1f} km")
# No plot
# rr_km, vv_ms, R0_km = generate_wind_profile(Vmaxmean_ms, Rmax_km, R34ktmean_km, lat)
# print(f"Estimated R0 = {R0_estimate_km:.1f} km")
