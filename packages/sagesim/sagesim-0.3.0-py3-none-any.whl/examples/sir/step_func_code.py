from cupyx import jit
import os
import sys
module_path = os.path.abspath('/home/co1/sagesim_github/sagesim_sfr/SAGESim/examples/sir/sir_step_func.py')
if module_path not in sys.path:
	sys.path.append(module_path)
from sir_step_func import *


@jit.rawkernel(device='cuda')
def stepfunc(
device_global_data_vector,
a0,a1,a2,a3,
sync_workers_every_n_ticks,
num_rank_local_agents,
agent_ids,
):
	thread_id = jit.blockIdx.x * jit.blockDim.x + jit.threadIdx.x
	agent_index = thread_id
	if agent_index < num_rank_local_agents:
		breed_id = a0[agent_index]
		for tick in range(sync_workers_every_n_ticks):

			if breed_id == 0:
				step_func(
					agent_index,
					device_global_data_vector,
					agent_ids,
					a0,a1,a2,a3,
				)
			if agent_index == 0:
				device_global_data_vector[0] += 1