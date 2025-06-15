import numpy as np

def generate_processes(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    num_processes = int(lines[0].strip())
    arrival_mean, arrival_std = map(float, lines[1].strip().split())
    burst_mean, burst_std = map(float, lines[2].strip().split())
    priority_lambda = float(lines[3].strip())
    
    processes = []

    for i in range(num_processes):
        arrival_time = max(0, int(np.random.normal(arrival_mean, arrival_std)))
        burst_time = max(1, int(np.random.normal(burst_mean, burst_std)))
        priority = int(np.random.exponential(num_processes/ priority_lambda)) + 1
        processes.append((f'P{i+1}', arrival_time, burst_time, priority))

    with open(output_file, 'w') as f:
        f.write(f"{num_processes}\n")
        for process in processes:
            f.write(" ".join(map(str, process)) + "\n")

    print(f"{num_processes} processes generated and written to {output_file}")

generate_processes("input.txt", "Processes.txt")
