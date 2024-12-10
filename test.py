#!/usr/bin/env python3.13

import importlib.util
import argparse
import csv
import puzzle
import time
from datetime import datetime

parser = argparse.ArgumentParser(description="Run advent of code days in an automated fashion.")

parser.add_argument('-y', '--year', type=str, help="Year")
parser.add_argument('-d', '--days', type=str, help="Year")
parser.add_argument('-e', '--exclude_days', type=str, help="Year", default=[])
parser.add_argument('-l', '--log_file', type=str, help="Log File", default=[])
args = parser.parse_args()

years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
days = range(1, 26)
exclude_days = []
log_file = f'logs/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
if args.year: years = [args.year]
if args.days: days = args.days.split(',')
if args.exclude_days: exclude_days = args.exclude_days.split(',')


for year in years:
  lf = open(log_file, "w")
  lf.write(f'Year {year}\n'); print(year)
  answers = list(csv.reader(open(f'{year}/inputs/answers.txt')))
  answers = {a[0]: [eval(a[1]), eval(a[2])] for a in answers}
  timings = dict()
  for i in days:
    if str(i) in exclude_days: continue
    lf.write(f'Day {i}\n'); print(i)
    file_path = f'{year}/{i}.py'
    module_name = f'day'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    day = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(day)
    p = puzzle.Puzzle(f'{year}', f"{i}")
    start_time = time.time()
    one = p.run(day.one, 0) 
    end_time = time.time()
    timings[f'{year}-{i}-1'] = round((end_time - start_time)*1000000)/1000
    start_time = time.time()
    two = p.run(day.two, 0) 
    end_time = time.time()
    timings[f'{year}-{i}-2'] = round((end_time - start_time)*1000000)/1000
    if answers[str(i)][0] != str(one):
      lf.write(f'INCORRECT: output - {one} vs correct - {answers[str(i)][0]}')
      continue
    if answers[str(i)][1] != str(two):
      lf.write(f'INCORRECT: output - {two} vs correct - {answers[str(i)][1]}')
      continue
    lf.write(f'{timings[f'{year}-{i}-1']} ms\n')
    lf.write(f'{timings[f'{year}-{i}-2']} ms\n')
  for t in timings:
    lf.write(f'{t} {timings[t]} ms\n')
