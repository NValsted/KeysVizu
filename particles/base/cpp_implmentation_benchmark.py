import fluids_base_ext
from deprecated import fluids
import time

N = 128

print("__Benchmarking c++-based fluid__")
print("__Shared array__")
FF = fluids_base_ext.pyFluidField(N,0.2,0.1,0.0001)

start_time = time.time()
count = 0
for i in range(1000):
    FF.iterate()
    d_array_ptr = FF.get_density_array()
    for i in range(N):
        for j in range(N):
            d_array_ptr[i+j*N]
    count += 1
    if time.time() - start_time > 1:
        print(f"iterations per second: {count/(time.time() - start_time)}")
        count = 0
        start_time = time.time()

print("__Without shared array__")
start_time = time.time()
count = 0
for i in range(1000):
    FF.iterate()
    for i in range(N):
        for j in range(N):
            FF.get_density(i,j)
    count += 1
    if time.time() - start_time > 1:
        print(f"iterations per second: {count/(time.time() - start_time)}")
        count = 0
        start_time = time.time()


print("__Benchmarking python-based fluid__")
deprecated_FF = fluids.Fluid(128,0.2,0.1,0.0001)

start_time = time.time()
count = 0
for i in range(15):
    deprecated_FF.iterate()
    deprecated_FF.density
    count += 1
    if time.time() - start_time > 1:
        print(f"iterations per second: {count/(time.time() - start_time)}")
        count = 0
        start_time = time.time()
