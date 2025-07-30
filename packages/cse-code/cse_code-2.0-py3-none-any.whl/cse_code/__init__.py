from .exp import experiment

def exp_code(n):
    code = experiment.get(n)
    if code:
        print(code)
    else:
        print("Invalid experiment number. Choose 1-10.")