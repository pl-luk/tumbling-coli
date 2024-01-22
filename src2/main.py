import numpy as np
import matplotlib.pyplot as plt
import os
import tracemalloc
import linecache
import time

# Just a helper function to analyse memory consumption
def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

def plot_traj(pos):
    fig, ax = plt.subplots()
    pp = pos.transpose(1, 0, 2)

    for b in pp:
        plt.plot(b[:, 0], b[:,1])

    plt.show()

def remap(arr, path):
    np.save(path, arr)
    del arr
    r = np.load(path, mmap_mode="r+")
    return r


# Input:
# N: Number of bacteria
# t: Simulation time in seconds
# v: Bacteria velocity in micrometers / seconds
# tau: Mean runtime in seconds
# alpha: Mean tumble angle in rad
# chunk_size: Size of time chunks generated
# out: Path where all the data is stored
# dtype: One of numpy float variants
def sim(N, t, chunk_size, v = 20, tau = 1, alpha = 70 / 180 * np.pi, angle_variance = 1,
        out = "./data", dtype = np.float64):

    # make sure out path exists
    out = os.path.abspath(out)

    if os.path.isdir(out):
        print(f">>> {out} is not empty! Exiting...")
        return
    else:
        os.mkdir(out)

    tracemalloc.start()
    tA1 = time.time()
    ##################################
    # Draw run times
    ##################################
    print(">>> Calculating runtimes...")
    t1 = time.time()
    time_blocks = []
    cum_time = np.zeros(N, dtype=dtype)
    shortest_time = 0

    # Generate time blocks until every bacteria has run at least t seconds
    while shortest_time < t:

        time_chunk = np.random.exponential(alpha, size = (chunk_size, N))
        time_blocks.append(time_chunk)
        cum_time += time_chunk.sum(axis=0)

        shortest_time = min(cum_time)

    # now we have enough run time to complete the simulation
    times = np.vstack(time_blocks)

    # save the times on disk and reread for memory efficiency reasons
    times = remap(times, os.path.join(out, "times.npy"))
    t2 = time.time()
    print(f">>> Took {np.round(t2 - t1, 2)} seconds")

    #################################
    # Draw angles
    #################################
    print(">>> Calculating tumble angles...")
    t1 = time.time()
    angles = np.memmap(os.path.join(out, "angles.npy"), mode="w+", dtype = dtype, shape = times.shape)
    angles += np.random.normal(loc = alpha, scale = angle_variance, size = times.shape)
    t2 = time.time()
    print(f">>> Took {np.round(t2 - t1, 2)} seconds")

    ################################
    # Looking at's
    ################################
    print(">>> Calculating looking vectors...")
    t1 = time.time()

    # every bacteria looks in direction (1, 0) initially
    looking_ats = np.memmap(os.path.join(out, "looking_ats.npy"), mode="w+", dtype = dtype, shape = (len(angles), N, 2))
    looking_ats += np.array([1, 0])

    # we start with a tumble
    r = np.array([[np.cos(angles[0]), -np.sin(angles[0])],
                      [np.sin(angles[0]), np.cos(angles[0])]]).transpose(2, 0, 1)

    for j in range(len(r)):
        looking_ats[0][j] = r[j] @ looking_ats[0][j]

    # now let the bacteria tumble
    for i in range(1, len(angles)):
        
        # r is a vector of rotation matrizes
        r = np.array([[np.cos(angles[i]), -np.sin(angles[i])],
                      [np.sin(angles[i]), np.cos(angles[i])]]).transpose(2, 0, 1)
        
        # This:
        # for j in range(len(r)):
        #     looking_ats[i][j] = np.dot(r[j], looking_ats[i - 1][j])
        # takes twice as long as:
        t = np.tensordot(r, looking_ats[i], axes=(1, 1)).transpose(0, 2, 1)
        for j in range(len(t)):
            looking_ats[i][j] = t[j][j]
    
    # normalize looking_ats
    looking_ats_normalized = np.memmap(os.path.join(out, "looking_ats_normalized.npy"), mode="w+", dtype = dtype, shape = (len(angles), N, 2))
    looking_ats_norm = np.linalg.norm(looking_ats, 1, axis=2, keepdims=True)
    looking_ats_normalized += looking_ats / looking_ats_norm
    t2 = time.time()
    print(f">>> Took {np.round(t2 - t1, 2)} seconds")

    ################################
    # Bacteria positions
    ################################
    print(">>> Calculating positions...")
    t1 = time.time()
    
    # every bacteria starts at (0, 0)
    pos = np.memmap(os.path.join(out, "positions.npy"), mode="w+", dtype = dtype, shape = looking_ats.shape)
    
    # now let the bacteria run
    for i in range(1, len(angles)):
        pos[i] = np.einsum('ij,i->ij', looking_ats[i - 1], times[i - 1]) * v + pos[i - 1]
    t2 = time.time()
    print(f">>> Took {np.round(t2 - t1, 2)} seconds")

    print(">>> All done!")
    tA2 = time.time()
    print(f">>> Simulation took {np.round(tA2 - tA1, 2)} seconds")

    s = tracemalloc.take_snapshot()

    print("=============================================================================")
    print(">>> Overall Memory usage:")
    display_top(s, limit = 5)
