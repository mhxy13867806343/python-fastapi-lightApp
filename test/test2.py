import  random

def bb():
    t=random.sample(range(10000, 999999999999999), k=5000000)
    for i in t:
        print(i)
bb()