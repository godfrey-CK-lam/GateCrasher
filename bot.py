
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start', type=str)
parser.add_argument('end', type=str)
args = parser.parse_args()

print(args.start)
print(args.end)