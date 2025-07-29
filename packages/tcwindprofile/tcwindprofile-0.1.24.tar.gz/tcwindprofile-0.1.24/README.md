# TCWindProfile

A package that creates fast and robust radial profiles of the tropical cyclone rotating wind and pressure from inputs Vmax, R34kt, and latitude. Based on the latest observationally-validated science on the structure of the wind field and pressure.

#### Cite this code:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15442673.svg)](https://doi.org/10.5281/zenodo.15442673)
Also paper in prep with co-authors Dandan Tao and Robert Nystrom

Full modeling pipeline:
- Estimate Rmax from R34kt: ref Chavas and Knaff 2022 WAF "A Simple Model for Predicting the Tropical Cyclone Radius of Maximum Wind from Outer Size" https://doi.org/10.1175/WAF-D-21-0103.1
- Estimate R0 from R34kt: analytic approximate solution, from model of ref Emanuel 2004 / Chavas et al. 2015 JAS / Chavas and Lin 2016 JAS ("Tropical cyclone energetics and structure" https://doi.org/10.1017/CBO9780511735035.010 / "A model for the complete radial structure of the tropical cyclone wind field. Part I: Comparison with observed structure" https://doi.org/10.1175/JAS-D-15-0014.1 / "Part II: Wind field variability" https://doi.org/10.1175/JAS-D-15-0185.1)
- Generate outer wind profile R34kt to R0: same refs as previous
- Generate inner wind profile inside R34kt: mod rankine, ref Fig 8 of Klotzbach et al. 2022 JGR-A ("Characterizing continental US hurricane risk: Which intensity metric is best?" https://doi.org/10.1029/2022JD037030)
- Generate complete wind profile: merge inner and outer
- Estimate Pmin: ref Chavas Knaff Klotzbach 2025 WAF ("A simple model for predicting tropical cyclone minimum central pressure from intensity and size" https://doi.org/10.1175/WAF-D-24-0031.1)
- Generate pressure profile that matches Pmin: same ref as previous

Currently, this code uses a quadratic profile inside the eye (r<Rmax), a modified‐Rankine vortex between Rmax and R34kt (inner model), and the E04 model beyond R34kt. It is very similar to the full physics-based wind profile model of Chavas et al. (2015) ([code here](http://doi.org/10.4231/CZ4P-D448)), but is simpler and much faster, and also includes a more reasonable eye model.

The model starts from the radius of 34kt, which is the most robust measure of size we have: it has long been routinely-estimated operationally; it is at a low enough wind speed to be accurately estimated by satellites over the ocean (higher confidence in data); and it is less noisy because it is typically outside the convective inner-core of the storm. The model then encodes the latest science to estimate 1) Rmax from R34kt (+ Vmax, latitude), 2) the radius of vanishing wind R0 from R34kt (+ latitude, an environmental constant), and 3) the minimum pressure Pmin from Vmax, R34kt, latitude, translation speed, and environmental pressure. Hence, it is very firmly grounded in the known physics of the tropical cyclone wind field while also matching the input data. It is also guaranteed to be very well‐behaved for basically any input parameter combination.

