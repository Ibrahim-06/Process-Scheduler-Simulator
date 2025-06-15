from collections import deque

def round_robin(processes, quantum):
    queue = deque()
    time = 0
    timeline = []
    rem_bt = {p['pid']: p['burst'] for p in processes}
    arrived = []
    execution_log = []

    while True:
        for p in processes:
            if p['arrival'] <= time and p not in arrived:
                queue.append(p)
                arrived.append(p)

        if not queue:
            if len(arrived) == len(processes):
                break
            time += 1
            continue

        p = queue.popleft()
        start = time
        bt = min(quantum, rem_bt[p['pid']])
        time += bt
        rem_bt[p['pid']] -= bt
        timeline.append((p['pid'], start, time))
        execution_log.append((p['pid'], start, time))

        for q in processes:
            if q['arrival'] <= time and q not in arrived:
                queue.append(q)
                arrived.append(q)

        if rem_bt[p['pid']] > 0:
            queue.append(p)
        else:
            p['end'] = time

    for p in processes:
        p['start'] = next(start for pid, start, end in execution_log if pid == p['pid'])
        p['tat'] = p['end'] - p['arrival']
        p['wt'] = p['tat'] - p['burst']

    return timeline