#!/usr/bin/env python3

import collections
from functools import wraps

def log_and_count(key=None, counts=None):   #"decorator factory", funkce, ktera vytvari samostatny dekorator 
    #Dekorator bere 2 klicove argumenty (key, counts)
    #counts je struktura Counter (my_counter), ktera uklada pocty volani funkci 
    def decorator(func):       #samotny dekorator
        @wraps(func)        #vytvori funkci wrapper
        #Pouzitim @wraps(func) zajistime, ze nova funkce wrapper ma stejne jmeno jako puvodni funkce
        def wrapper(*args, **kwargs):
            func_name = key or func.__name__  #Pokud je key != None, pouzije se jako klic pro strukturu counts, v opacnem pripade pouzijeme nazev funkce,e ke ktere je dekorator aplikovan
            counts[func_name] += 1  #Zaznam poctu volani dekorovane funkce pod zadanym klicem 
            print(f"called {func.__name__} with {args} and {kwargs}")   #Zobrazeni zaznamu o zavolani funkce
            return func(*args, **kwargs)
        return wrapper
    return decorator


my_counter = collections.Counter()

@log_and_count(key = 'basic functions', counts = my_counter)
def f1(a, b=2):
    return a ** b

@log_and_count(key = 'basic functions', counts = my_counter)
def f2(a, b=3):
    return a ** 2 + b

@log_and_count(counts = my_counter)
def f3(a, b=5):
    return a ** 3 - b

f1(2)
f2(2, b=4)
f1(a=2, b=4)
f2(4)
f2(5)
f3(5)
f3(5,4)

print(my_counter)
