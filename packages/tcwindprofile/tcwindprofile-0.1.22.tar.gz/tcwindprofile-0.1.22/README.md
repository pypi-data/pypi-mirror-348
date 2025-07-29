# TCWindProfile

A package that creates fast and robust radial profiles of the tropical cyclone rotating wind and pressure from inputs Vmax, R34kt, and latitude.

#### Cite this code:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15442673.svg)](https://doi.org/10.5281/zenodo.15442673)
Also paper in prep with co-authors Dandan Tao and Robert Nystrom

Full modeling pipeline:
- Estimate Rmax from R34kt: ref Chavas and Knaff 2022 WAF)
- Estimate R0 from R34kt: approximate version of outer model ref Emanuel 2004 / Chavas et al. 2015 JAS / Chavas and Lin 2016 JAS
- Generate wind profile: merge simple inner + outer models, ref Klotzbach et al. 2022 JGR-A / Chavas and Lin 2016 JAS
- Estimate Pmin: ref Chavas Knaff Klotzbach 2025 WAF
- Generate pressure profile that matches Pmin: ref Chavas Knaff Klotzbach 2025 WAF

Currently, this code uses a quadratic profile inside the eye (r<Rmax), a modified‐Rankine vortex between Rmax and R34kt (inner model), and the E04 model beyond R34kt. It is very similar to the full physics-based wind profile model of Chavas et al. (2015) ([code here](http://doi.org/10.4231/CZ4P-D448)), but is simpler and much faster, and also includes a more reasonable eye model.

The model starts from the radius of 34kt, which is the most robust measure of size we have: it has long been routinely-estimated operationally; it is at a low enough wind speed to be accurately estimated by satellites over the ocean (higher confidence in data); and it is less noisy because it is typically outside the convective inner-core of the storm. The model then encodes the latest science to estimate 1) Rmax from R34kt (+ Vmax, latitude), 2) the radius of vanishing wind R0 from R34kt (+ latitude, an environmental constant), and 3) the minimum pressure Pmin from Vmax, R34kt, latitude, translation speed, and environmental pressure. Hence, it is very firmly grounded in the known physics of the tropical cyclone wind field while also matching the input data. It is also guaranteed to be very well‐behaved for basically any input parameter combination.

