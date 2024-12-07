#!/usr/bin/env python3

import importlib.util
import argparse

parser = argparse.ArgumentParser(description="Run advent of code days in an automated fashion.")

parser.add_argument('-y', '--year', type=str, help="Year")
args = parser.parse_args()

years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
if args.year: years = [args.year]

for year in years:
  print(f'Year {year}')
  for i in range(1, 26):
    print(f'Day {i}')
    file_path = f'{year}/{i}.py'
    module_name = f'day'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    day = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(day)
    