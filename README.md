# SIRANE-short-term-forecasting-of-nitrogen-dioxide-concentrations-in-Brussels

Welcome to this GitHub repository, which provides various codes for my thesis. Python codes here show how I automated the simulation launch process with SIRANE (auto_sim.py) and then concatenated the output files for a clearer view of the results.
The files output by SIRANE are in the form of simulations starting every 12 hours and lasting 48 hours. The files then start either at midnight or at noon. The first concatenation step was to group the data into 2 excel files according to whether the simulation started at midnight or noon (concat_results.py). Then, the 2 files were concatenated to have a 12h time step (concat_12h.py).
