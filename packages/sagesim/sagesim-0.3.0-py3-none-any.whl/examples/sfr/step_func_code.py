
    
from random import random
    
from cupyx import jit
    



import cupy as cp
import math
import bisect

@jit.rawkernel(device='cuda')
def step_func(
    agent_ids,
    agent_index,
    globals,
    breeds,
    locations,
    popularities,
    vehicle_nums,
):

    # Get agent's vehicle number and neighbors' locations
    agent_vehicle_num = vehicle_nums[agent_index]
    # Zero out agent's vehicle count
    vehicle_nums[agent_index] = agent_vehicle_num
    neighbor_ids = locations[agent_index]

    # find total popularity of all neighbors
    total_popularity = cp.float64(0)
    neighbor_i = 0
    while not cp.isnan(neighbor_ids[neighbor_i]) and neighbor_i < len(neighbor_ids):
        neighbor_id = neighbor_ids[neighbor_i]
        # Find the index of the neighbor_id in agent_ids
        neighbor_index = -1
        i = 0
        while i < len(agent_ids) and agent_ids[i] != neighbor_id:
            i += 1
        if i < len(agent_ids):
            neighbor_index = i
            neighbor_popularity = popularities[int(neighbor_index)]
            total_popularity += neighbor_popularity
        neighbor_i += 1

    remainder = agent_vehicle_num
    largest_alloc = 0

    if total_popularity > 0:
        remainder_alloc_index = -1
        neighbor_i = 0
        while not cp.isnan(neighbor_ids[neighbor_i]) and neighbor_i < len(neighbor_ids):
            neighbor_id = neighbor_ids[neighbor_i]
            # Find the index of the neighbor_id in agent_ids
            neighbor_index = 0
            while (
                neighbor_index < len(agent_ids)
                and agent_ids[neighbor_index] != neighbor_id
            ):
                neighbor_index += 1
            if (neighbor_index < len(agent_ids)) and (agent_ids[i] != neighbor_id):
                neighbor_popularity = popularities[int(neighbor_index)]

                neighbor_allocation = int(
                    agent_vehicle_num * neighbor_popularity / total_popularity
                )
                # find the top popularity neighbor
                if neighbor_allocation > largest_alloc:
                    remainder_alloc_index = neighbor_index
                    largest_alloc = neighbor_allocation

                remainder -= neighbor_allocation
            neighbor_i += 1

        # Distribute the remainder (due to rounding) to top contributors
        if remainder > 0 and remainder_alloc_index >= 0:
            vehicle_nums[int(remainder_alloc_index)] += remainder

    

@jit.rawkernel()
def stepfunc(
    device_global_data_vector,
    a0,a1,a2,a3,
    sync_workers_every_n_ticks,
    num_rank_local_agents,
    agent_ids,
    ):
        thread_id = jit.blockIdx.x * jit.blockDim.x + jit.threadIdx.x
        #g = cuda.cg.this_grid()
        agent_index = thread_id        
        if agent_index < num_rank_local_agents:
            breed_id = a0[agent_index]                
            for tick in range(sync_workers_every_n_ticks):
                
            
                if breed_id == 0:
                    step_func(
                        agent_ids,
                        agent_index,
                        device_global_data_vector,
                        a0,a1,a2,a3,
                    )
            #cuda.syncthreads()

                            
                if agent_index == 0:
                    device_global_data_vector[0] += 1
    