# pmv-comfort-map

PMV thermal comfort map recipe for Pollination.

Compute spatially-resolved operative temperature and PMV thermal comfort from
a Honeybee model and EPW. This recipe can also (optionally) compute Standard
Effective Temperature (SET).

This recipe uses EnergyPlus to obtain longwave radiant temperatures and indoor air
temperatures. The outdoor air temperature and air speed are taken directly from the EPW.
A Radiance-based enhanced 2-phase method is used for all shortwave MRT calculations,
which includes an accurate direct sun calculation using precise solar positions. The
energy properties of the model geometry are what determine the outcome of the
simulation and the model's SensorGrids are what determine where the comfort
mapping occurs.
