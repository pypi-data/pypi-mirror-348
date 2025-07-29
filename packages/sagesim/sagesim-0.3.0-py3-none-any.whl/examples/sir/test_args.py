from cupyx import jit
import cupy as cp


@jit.rawkernel()
def kernel_with_struct(args, output):
    thread_id = jit.blockIdx.x * jit.blockDim.x + jit.threadIdx.x
    if thread_id < len(output):
        # Access arguments from the struct
        arg1 = args[0][thread_id]
        arg2 = args[1][thread_id]
        output[thread_id] = arg1 * arg2  # Example operation


# Example usage
args = [cp.array([1, 2, 3], dtype=cp.float32), cp.array([4, 5, 6], dtype=cp.float32)]
output = cp.zeros(len(args[0]), dtype=cp.float32)

threads_per_block = 32
blocks_per_grid = (len(output) + threads_per_block - 1) // threads_per_block
kernel_with_struct[blocks_per_grid, threads_per_block](args, output)

print(output)  # Output: [4. 10. 18.]
