from Operations import getNPArrayGPU, getNPArrayCPU
from collections import namedtuple
from timeit import default_timer as timer


raw_data_list = []

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])

for index in range(1000000):
    to_add = DataPoint(float(index), float(index))
    raw_data_list.append(to_add)

start = timer()
getNPArrayCPU(raw_data_list)
print("without GPU:", timer() - start)

start = timer()
getNPArrayGPU(raw_data_list)
print("with GPU:", timer() - start)


