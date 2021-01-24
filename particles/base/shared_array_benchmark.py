import fluids_base_ext
from deprecated import fluids
import time

print("__Benchmarking c++-based fluid__")
FF = fluids_base_ext.pyFluidField(128,0.2,0.1,0.0001)

start_time = time.time()
count = 0
for i in range(1000):
    FF.iterate()
    FF.get_density_array()
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