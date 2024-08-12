# SIRANE-short-term-forecasting-of-nitrogen-dioxide-concentrations-in-Brussels

Welcome to this GitHub repository ! Python codes here show how I automated the simulation launch process with SIRANE (auto_sim.py) and then concatenated the output files for a clearer view of the results.

The files output by SIRANE are in the form of simulations starting every 12 hours and lasting 48 hours (can be modified). The files then start either at midnight or at noon. [1] The first concatenation step was to group the data into 2 excel files according to whether the simulation started at midnight or noon (concat_results.py). The time step is 24h. 
[2] Then, the 2 files were concatenated to have a 12h time step (concat_12h.py). The final Excel contains measured and modeled pollutant concentrations for different forecast horizons (0, 12, 24 and 36h).
