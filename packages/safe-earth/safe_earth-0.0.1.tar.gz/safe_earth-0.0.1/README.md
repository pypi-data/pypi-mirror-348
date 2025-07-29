# SAFE
Stratified Assessment of Forecasts over Earth

To unify the coordinate system across all integrated data sources, latitude ranges [-90, 90] with index 0 at -90, and longitude [-180, 180) but with index 0 at 0 and a wraparound from 180 to -180 in the middle. This is because metadata sourced from pygeoboundaries_geolab follows this coordinate system, and it is easiest to bring tabular data into conformance.

### Testing

Run `pytest` in the terminal
