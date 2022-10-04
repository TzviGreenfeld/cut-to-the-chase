import os
import time
from tqdm import tqdm

in_path = "../../../mnt/c/Users/tzvig/Downloads/season1/"
out_path = "/home/tzvigr/chaser/test/s1_test/"

for episode in tqdm(os.listdir(in_path)):
    start_time = time.time()
    os.system(f"python3 main.py {in_path + episode} {out_path + episode}")
    total_time = time.time() - start_time
    os.system(f'echo "{episode}, {total_time}," >> {out_path + "time.csv"}')
