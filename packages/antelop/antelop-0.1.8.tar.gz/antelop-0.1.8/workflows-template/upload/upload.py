import argparse
from pathlib import Path
import os
import zipfile
from antelop.utils.datajoint_utils import get_ephys_extensions
from antelop.load_connection import *
from antelop.connection.transaction import operation_context
import json

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--insert_dict")
parser.add_argument("-t", "--tablename")
args = parser.parse_args()

insert_dict = json.loads(args.insert_dict)
tablename = args.tablename

table = tables[tablename]

with open('debug.json', 'w') as f:
    json.dump(insert_dict, f, indent=4)

# if it's a session, we need to zip the raw data first and update the path
if tablename == "Recording":
    # extract dirpath
    dirpath = insert_dict["recording"]

    # create zipfile name from primary key
    recfile = Path(dirpath).with_suffix(".zip")

    # get files to zip
    extensions = get_ephys_extensions()
    ephys_acquisition = insert_dict["ephys_acquisition"]
    equip_ext = extensions[ephys_acquisition]
    files = []
    for ext in equip_ext:
        if ext == "dir":
            # add all directories
            files.extend([item for item in Path(dirpath).iterdir() if item.is_dir()])
        else:
            files.extend(list(Path(dirpath).glob(f"*.{ext}")))

    # create zipfile
    with zipfile.ZipFile(recfile, "w") as zipf:
        for file in files:
            if file.is_dir():
                # Recursively add all files in the directory
                for root, _, filenames in os.walk(file):
                    for filename in filenames:
                        filepath = Path(root) / filename
                        arcname = filepath.relative_to(dirpath)  # Preserve relative path
                        zipf.write(filepath, arcname=arcname)
            else:
                # Add individual files
                zipf.write(file, arcname=file.name)

    # update dirpath
    insert_dict["recording"] = str(recfile)

with operation_context(conn):
    table.insert([insert_dict])