from .exp import experiment

def tl_code(n):
    code = experiment.get(n)
    if code:
        print(code)
    else:
        print("Sorry Dude wrong exp number. Choose 1-10.")

