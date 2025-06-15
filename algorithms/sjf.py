def sjf(processes):
    time = 0
    timeline = []
    remaining_processes = [p.copy() for p in processes]
    rem_bt = {p['pid']: p['burst'] for p in processes}
    execution_log = []
    completed = []
    
    while len(completed) < len(processes):
        arrived = [p for p in remaining_processes if p['arrival'] <= time and rem_bt[p['pid']] > 0]
        
        if not arrived:
            time += 1
            continue
        
        
        current = min(arrived, key=lambda x: (rem_bt[x['pid']], x['arrival']))
        
        rem_bt[current['pid']] -= 1
        execution_log.append((current['pid'], time, time + 1))
        time += 1

        if rem_bt[current['pid']] == 0:
            current['end'] = time
            completed.append(current)
    
    
    for p in processes:
        p_exec = [entry for entry in execution_log if entry[0] == p['pid']]
        p['start'] = p_exec[0][1]
        p['end'] = p_exec[-1][2]
        p['tat'] = p['end'] - p['arrival']
        p['wt'] = p['tat'] - p['burst']
    
    
    for pid, start, end in execution_log:
        if not timeline or timeline[-1][0] != pid:
            timeline.append((pid, start, end))
        else:
            timeline[-1] = (pid, timeline[-1][1], end)

    return timeline