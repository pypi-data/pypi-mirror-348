# TCWindProfile

A package that creates a fast and robust radial profile of the tropical cyclone rotating wind from inputs Vmax, R34kt, Rmax, and latitude.

#### This code uses a modified‐Rankine vortex between Rmax and R34kt and the E04 model beyond R34kt (and a quadratic profile inside the eye). It is very similar to the full physics-based wind profile model of Chavas et al. (2015) ([code here](http://doi.org/10.4231/CZ4P-D448)), but is simpler and much faster.

#### It is designed to guarantee that the profile fits both Rmax and R34kt and will be very close to the true outer radius (R0) as estimated by the full E04 outer solution. Hence, it is very firmly grounded in the known physics of the tropical cyclone wind field while also matching the input data. It is also guaranteed to be very well‐behaved for basically any input parameter combination.

#### Model basis:
#### Modified Rankine profile between Rmax and R34kt was shown to compare very well against high-quality subset of Atlantic Best Track database -- see Fig 8 of [Klotzbach et al. (2022, JGR-A)](https://doi.org/10.1029/2022JD037030)
#### Physics-based non-convecting wind field profile beyond R34kt was shown to compare very well against entire QuikSCAT database -- see Fig 6 of [Chavas et al. (2015, JAS)](https://doi.org/10.1175/JAS-D-15-0014.1)
#### Quadratic in the eye (U-shape is common)

#### Cite this code: DOI forthcoming; paper in prep with co-authors Dandan Tao and Robert Nystrom
