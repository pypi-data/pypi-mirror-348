def tl_exp(experiment_number):
    if experiment_number == 1:
        from .experiments import exp1
        exp1.run()
    else:
        raise ValueError(f"Experiment {experiment_number} not implemented.")
