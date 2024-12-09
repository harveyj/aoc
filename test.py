#!/usr/bin/env python3

import importlib.util
import argparse
import csv
import puzzle
import time

parser = argparse.ArgumentParser(description="Run advent of code days in an automated fashion.")

parser.add_argument('-y', '--year', type=str, help="Year")
parser.add_argument('-d', '--days', type=str, help="Year")
parser.add_argument('-e', '--exclude_days', type=str, help="Year", default=[])
args = parser.parse_args()

years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
days = range(1, 26)
exclude_days = []
if args.year: years = [args.year]
if args.days: days = args.days.split(',')
if args.exclude_days: exclude_days = args.exclude_days.split(',')


for year in years:
  print(f'Year {year}')
  answers = list(csv.reader(open(f'{year}/inputs/answers.txt')))
  answers = {a[0]: [eval(a[1]), eval(a[2])] for a in answers}
  timings = dict()
  for i in days:
    if str(i) in exclude_days: continue
    print(f'Day {i}')
    file_path = f'{year}/{i}.py'
    module_name = f'day'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    day = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(day)
    p = puzzle.Puzzle(f'{year}', f"{i}")
    start_time = time.time()
    one = p.run(day.one, 0) 
    end_time = time.time()
    timings[f'{year}-{i}-1'] = end_time - start_time
    start_time = time.time()
    two = p.run(day.two, 0) 
    end_time = time.time()
    timings[f'{year}-{i}-2'] = end_time - start_time
    if answers[str(i)][0] != str(one):
      print(f'INCORRECT: output - {one} vs correct - {answers[str(i)][0]}')
      continue
    if answers[str(i)][1] != str(two):
      print(f'INCORRECT: output - {two} vs correct - {answers[str(i)][1]}')
      continue
    print('CORRECT')
  for t in timings:
    print(f'{t} {round(timings[t]* 1000000) / 1000} ms')
    
