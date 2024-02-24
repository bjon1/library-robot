import os
import multiprocessing

print("Number of CPU cores:", multiprocessing.cpu_count())
print("Number of threads your CPU can run concurrently:", os.cpu_count())