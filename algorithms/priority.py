def priority(processes):
    time = 0
    completed = []
    timeline = []
    ready = []
    while len(completed) < len(processes):
        for p in processes:
            if p not in completed and p not in ready and p['arrival'] <= time:
                ready.append(p)
        if ready:
            ready.sort(key=lambda x: (-x['priority'], x['arrival']))
            current = ready.pop(0)
            start = max(time, current['arrival'])
            end = start + current['burst']
            current['start'] = start
            current['end'] = end
            current['tat'] = end - current['arrival']
            current['wt'] = start - current['arrival']
            completed.append(current)
            timeline.append((current['pid'], start, end))
            time = end
        else:
            time += 1
    return timeline