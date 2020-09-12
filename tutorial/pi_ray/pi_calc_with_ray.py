import numpy as np
import math, statistics, time, locale
import ray
from pi_calc import str_large_n
from task_lesson_util import make_dmaps, run_simulations, stop_simulations

num_workers = 4
trials = 20

ray.init(ignore_reinit_error=True)

def estimate_pi(num_samples):
    xs = np.random.uniform(low=-1.0, high=1.0, size=num_samples)   # Generate num_samples random samples for the x coordinate.
    ys = np.random.uniform(low=-1.0, high=1.0, size=num_samples)   # Generate num_samples random samples for the y coordinate.
    xys = np.stack((xs, ys), axis=-1)                              # Like Python's "zip(a,b)"; creates np.array([(x1,y1), (x2,y2), ...]).
    inside = xs*xs + ys*ys <= 1.0                                  # Creates a predicate over all the array elements.
    xys_inside = xys[inside]                                       # Selects only those "zipped" array elements inside the circle.
    in_circle = xys_inside.shape[0]                                # Return the number of elements inside the circle.
    approx_pi = 4.0*in_circle/num_samples                          # The Pi estimate.
    return approx_pi

Ns = [10000, 50000, 100000, 500000, 1000000] #, 5000000, 10000000]  # Larger values take a long time on small VMs and machines!
maxN = Ns[-1]

fmt = '{:10.5f} seconds: pi ~ {:7.6f}, stddev = {:5.4f}, error = {:5.4f}%'
def try_it(n, trials):
    print('trials = {:3d}, N = {:s}: '.format(trials, str_large_n(n, padding=12)), end='')   # str_large_n imported above.
    start = time.time()
    pis = [estimate_pi(n) for _ in range(trials)]
    approx_pi = statistics.mean(pis)
    stdev = statistics.stdev(pis)
    duration = time.time() - start
    error = (100.0*abs(approx_pi - np.pi) / np.pi)
    print(fmt.format(duration, approx_pi, stdev, error))   # str_large_n imported above.
    return trials, n, duration, approx_pi, stdev, error


data_ns = [try_it(n, trials) for n in Ns]