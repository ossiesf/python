import random, time
from functools import reduce
from collections import namedtuple

'''
Code and set up config for Monte Carlo method
size = Size of square (imagine a graph for x and y coordinates)
radius = half the width of the circle and half the width of the square
pi_upper and pi_lower = the upper and lower bounds to check pi is accurate +- .001 (one thousandth)

Config keeps a central place for our constants that can easily be passed between functions,
so that they are not dependent on hidden state, and avoids using global scope constants in a functional style
'''
Config = namedtuple('Config', ['size', 'radius', 'pi_upper', 'pi_lower'])
config = Config(size=100, radius=50, pi_upper=3.143, pi_lower=3.140)

def coord_generator(size):
    while True:
            yield random.randint(1, size), random.randint(1, size)

'''
Create a point and check if it's inside the circle or not
General formula for Monte Carlo method is:
Check if the coordinate is inside the circle (should be counted):
(x-center)**2 + (y-center)**2 <= radius**2; Where center is equivalent to the radius
Then take the proportion of num_inside_circle / total_points_plotted and multiply by 4
'''
def plot_point(config):
    x, y = next(coord_generator(config.size))
    return (x-config.radius)**2 + (y-config.radius)**2 <= config.radius**2
    
'''
Generator for pi that stops when within 1/1_000th of actual pi (3.1415)
'''
def calculate_pi(config):
    num_inside = 0
    total_runs = 0
    while True:
        if plot_point(config):
            num_inside += 1
        total_runs += 1
        pi = 4 * (num_inside/total_runs)
        if pi <= config.pi_upper and pi >= config.pi_lower:
            yield pi
            break
        else:
            yield pi

'''
Run the necessary simuations for monte carlo
'''
def monte_carlo(config):
    return round(reduce(lambda _, x: x, calculate_pi(config)), 5)

'''
Code for leibniz formula
'''
def leibniz():
    return round(list(map(lambda x: x, get_pi()))[-1], 5)

def get_pi():
    pi, denominator, sign = 0, 1, 4
    while True:
        pi += sign * (1/denominator)
        denominator += 2
        sign = -sign
        yield pi
        if pi <= config.pi_upper and pi >= config.pi_lower:
            break
        
'''
General execution
'''
# Run and time each generator, accumulate # of times mc < leibniz
def is_monte_carlo_faster():
    start = time.time()
    monte_carlo_time = (time.time() - start) * 1e6
    start = time.time()
    leibniz_time = (time.time() - start) * 1e6
    
    if leibniz_time > monte_carlo_time:
        return True
    else:
        return False

'''
All numbers are rounded to the nearest 10_000th
'''
def main():
    start = time.time()
    print('Monte Carlo Estimate: ' + str(monte_carlo(config)))
    monte_carlo_time = round((time.time() - start) * 1e6, 4)
    print('Monte Carlo Execution Time: ' + str(monte_carlo_time) + ' microseconds')
    start = time.time()
    print('Leibniz Formula: ' + str(leibniz()))
    leibniz_time = round((time.time() - start) * 1e6, 4)
    print('Leibniz Formula Execution Time: ' + str(leibniz_time) + ' microseconds')
    
    if leibniz_time > monte_carlo_time:
        print('Monte Carlo was faster by: ' + str(leibniz_time - monte_carlo_time) + ' microseconds')
    else:
        print('Leibniz was faster by: ' + str(round(monte_carlo_time - leibniz_time, 4) + ' microseconds'))
        
    monte_carlo_wins = reduce(lambda acc, x: acc + is_monte_carlo_faster(), range(1000))
    print('In 1_000 iterations, monte carlo was faster ' + str(monte_carlo_wins) + ' times')
    
if __name__ == '__main__':
    main()