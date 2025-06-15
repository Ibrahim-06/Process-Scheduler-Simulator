def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    timeline = []
    for p in processes:
        start = max(time, p['arrival'])
        end = start + p['burst']
        p['start'] = start
        p['end'] = end
        p['tat'] = end - p['arrival']
        p['wt'] = start - p['arrival']
        timeline.append((p['pid'], start, end))
        time = end
    return timeline