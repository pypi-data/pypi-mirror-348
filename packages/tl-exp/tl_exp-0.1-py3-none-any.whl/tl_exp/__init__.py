from .experiments import exp1

def tl_exp(n):
    if n == 1:
        exp1.run()
    else:
        raise ValueError(f"Experiment {n} not implemented yet.")
