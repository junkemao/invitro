from util import *
import os
import pandas as pd
import numpy as np
import string
import random


def hash_generator(size):
    chars=string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def generate(functions, beginning, target, step, duration, execution, memory, output_path, save):
    inv_df = load_data("base_traces/inv.csv")
    mem_df = load_data("base_traces/mem.csv")
    run_df = load_data("base_traces/run.csv")

    hashFunction = []
    hashOwner = []
    hashApp = []

    lenHashes = 64
    sampleC = 10000  # doesn't matter for synthetic traces
    for i in range(functions):
        hashFunction.append(hash_generator(lenHashes))
        hashOwner.append(hash_generator(lenHashes))
        hashApp.append(hash_generator(lenHashes))

    mem = [memory]
    mem = np.repeat(mem, len(mem_df.columns) - 3)
    run = [execution]
    run = np.repeat(run, len(run_df.columns) - 5)
    rps = [*range(beginning, target+1, step)]
    ipm = [60*x for x in rps]  # convert rps to invocations per minute
    ipm = np.repeat(ipm, duration)
    # pad with zeros to get trace that is 1440 minutes
    ipm = np.pad(ipm, (0, 1440 - len(ipm)), 'constant')

    for i in range(functions):
        memArr = [hashApp[i], hashOwner[i], sampleC]
        memArr.extend(mem)
        mem_df.loc[len(mem_df)] = memArr
        runArr = [hashFunction[i], hashOwner[i], hashApp[i], execution, sampleC]
        runArr.extend(run)
        run_df.loc[len(run_df)] = runArr 
        invArr = [hashApp[i], hashFunction[i], hashOwner[i]]
        invArr.extend(ipm)
        inv_df.loc[len(inv_df)] = invArr
    

    if save:
        save_data(inv_df, f"{output_path}/{functions}_inv.csv")
        save_data(mem_df, f"{output_path}/{functions}_mem.csv")
        save_data(run_df, f"{output_path}/{functions}_run.csv")

    return inv_df, mem_df, run_df
