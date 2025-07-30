import argparse
from pathlib import Path
from antelop.utils.antelop_utils import insert_nwb
import os
from antelop.load_connection import *
import json

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--world")
parser.add_argument("-a", "--animals")
parser.add_argument("-n", "--nwb_path")
args = parser.parse_args()

world = json.loads(args.world)
animals = json.loads(args.animals)
animals = {int(k): v for k, v in animals.items()}
nwb_path = Path(args.nwb_path)

PASSWORD = os.environ.get("DB_PASS")
USER = os.environ.get("DB_USER")

insert_nwb(world, animals, nwb_path, USER, PASSWORD)