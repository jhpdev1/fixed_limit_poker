import itertools
import math
import multiprocessing as mp
import queue
import time
import pandas as pd

from bots import CallBot, PercentBot, FoldBot, RandomBot, CounterBot
from environment.FixedLimitPoker import FixedLimitPoker

PARTICIPANTS = [PercentBot("player1"), CounterBot("player2")]
TOTAL_ROUNDS = 1000
PROCESS_COUNT = mp.cpu_count() - 2

def play(jobQueue: mp.Queue, roundsPerRoom: int, stats):
    while not jobQueue.empty():
        try:
            c = jobQueue.get(block=False)
        except queue.Empty:
            break
        room = FixedLimitPoker(c)
        for _ in range(roundsPerRoom):
            room.reset(rotatePlayers=True)
            p1 = room.players[0]
            p2 = room.players[1]
            k1 = (p1.bot.name, p2.bot.name)
            if k1 not in stats:
                stats[k1] = 0
            stats[k1] += p1.reward
            k2 = (p2.bot.name, p1.bot.name)
            if k2 not in stats:
                stats[k2] = 0
            stats[k2] += p2.reward


def main():
    combinations = list(itertools.combinations(PARTICIPANTS, 2))
    rounds_for_each_pair = math.floor(TOTAL_ROUNDS / len(combinations))

    print(f"There are {len(combinations)} combinations")
    print(f"Each combination will be played: {rounds_for_each_pair} times")

    start_time = time.time()
    manager = mp.Manager()
    stats = manager.dict()
    jobs = mp.Queue()
    for c in combinations:
        jobs.put(c)

    processes = []
    for _ in range(PROCESS_COUNT):
        p = mp.Process(target=play, args=(jobs, rounds_for_each_pair, stats))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    cols = [x.name for x in PARTICIPANTS]
    res = pd.DataFrame(0, columns=cols, index=cols + ["sum"])
    for key in stats.keys():
        res[key[0]]["sum"] += stats[key]
        res[key[0]][key[1]] = stats[key]

    print(res)

    duration = time.time() - start_time
    rounds = rounds_for_each_pair * len(combinations)
    duration_pr_sim = round(duration/rounds, 5)
    print(f"-----------------------------------------")
    print(f"Simulation took {duration_pr_sim} seconds pr. round")
    print(f"Using {PROCESS_COUNT} processes")
    print(f"--- {round(duration, 2)} seconds ---")

    
    #timestamp = round(time.time())
    #with open(f"./results/challenge-{timestamp}.csv", 'wb') as file:
    #    res.to_csv(file)
    #    print("Wrote to file ...")


if __name__ == '__main__':
    main()
