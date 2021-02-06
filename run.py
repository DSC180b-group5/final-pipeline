#!/usr/bin/env/python

import yaml
import argparse
import sys
import os
from pathlib import Path


PAGES_ARGS_PATH = 'config/pages-param.yml'
SENT_ARGS_PATH = 'config/sentiment-param.yml'
RESULTS_ARGS_PATH = 'config/results-param.yml'

def read_yml(path):
    with open(path, 'r') as ymlfile:
        return yaml.load(ymlfile, Loader=yaml.SafeLoader)

def run_pages(argpath):
    args = read_yml(argpath)
    #TODO actually do the thing

def run_sentiment(argpath):
    args = read_yml(argpath)
    #TODO actually do the thing

def run_model(argpath):
    args = read_yml(argpath)
    #TODO actually do the thing

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', 
        '--pages', 
        help='obtain list of pages to analyze from wikipedia', 
        action='store_true'
    )
    parser.add_argument(
        '-s', 
        '--sentiment', 
        help='run sentiment analysis on pages from list', 
        action='store_true'
    )
    parser.add_argument(
        '-r', 
        '--results', 
        help='stats and visuals from sentiment analysis', 
        action='store_true'
    )

    args = parser.parse_args()
    if args.pages:
        run_pages(PAGES_ARGS_PATH)
    if args.sentiment:
        run_sentiment(SENT_ARGS_PATH)
    if args.results:
        run_results(RESULTS_ARGS_PATH)
