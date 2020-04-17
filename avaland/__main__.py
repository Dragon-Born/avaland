from avaland.manager import SourceManager
from avaland.sources import *
import argparse

parser = argparse.ArgumentParser(description='Avaland Music Downloader')
parser.add_argument("query", type=str,
                    help='an integer for the accumulator')

args = parser.parse_args()

