import os
import datajoint as dj
from antelop.utils.os_utils import get_config
from pathlib import Path
import shutil

IN_CONTAINER = os.environ.get("IN_CONTAINER") == "True"

def clear_dir(path: Path):
    for item in path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def resolve_paths_in_config(config):
    """
    Resolve paths in the config that may contain $USER or other environment variables.
    """
    
    # Needed as sometimes USER doesn't copy across in apptainer environment
    if 'USER' not in os.environ and 'DB_USER' in os.environ:
        os.environ['USER'] = os.environ['DB_USER']

    for section, values in config.items():
        for key, value in values.items():
            if isinstance(value, str):  # Only process string values
                config[section][key] = os.path.expandvars(value)  # Resolve $USER or other env vars
    return config


def dbconnect(username, password):
    """
    Function loads configuration from home and
    returns a connection to the database.
    """
    
    # Set username to environment variable if None
    if username is None:
        username = os.getenv("DB_USER")
    if password is None:
        password = os.getenv("DB_PASS")

    if not IN_CONTAINER:
        cache_dir = Path.home() / ".cache" / "antelop"
        cache_dir.mkdir(parents=True, exist_ok=True)
        clear_dir(cache_dir)
    
    # Load config file
    config = get_config()

    # Resolve paths in the config
    import os
    from pprint import pprint
    pprint(dict(os.environ))
    config = resolve_paths_in_config(config)

    dj.config["database.host"] = config["mysql"]["host"]
    dj.config["database.user"] = username
    dj.config["database.password"] = password

    if config["s3"]["host"] == "local":
        filestore = Path(config["computation"]["antelop_data"]) / "data"
        if not filestore.exists():
            print(f"\nfilestore: {filestore}\n")
            filestore.mkdir(parents=True, exist_ok=True)
        for store in ["raw_ephys", "feature_behaviour", "dlcmodel", "behaviour_video", "labelled_frames", "evaluated_frames"]:
            if not (filestore / store).exists():
                (filestore / store).mkdir(parents=True, exist_ok=True)
        dj.config["stores"] = {
            "raw_ephys": {
                "protocol": "file",
                "location": filestore / "raw_ephys",
            },
            "feature_behaviour": {
                "protocol": "file",
                "location": filestore / "features_behaviour",
            },
            "dlcmodel": {
                "protocol": "file",
                "location": filestore / "dlcmodel",
            },
            "behaviour_video": {
                "protocol": "file",
                "location": filestore / "behaviour_video",
            },
            "labelled_frames": {
                "protocol": "file",
                "location": filestore / "labelled_frames",
            },
            "evaluated_frames": {
                "protocol": "file",
                "location": filestore / "evaluated_frames",
            },
        }
    else:
        dj.config["stores"] = {
            "raw_ephys": {
                "protocol": "s3",
                "endpoint": config["s3"]["host"],
                "bucket": "antelop-external-data",
                "location": "/raw_ephys",
                "access_key": username,
                "secret_key": password,
            },
            "feature_behaviour": {
                "protocol": "s3",
                "endpoint": config["s3"]["host"],
                "bucket": "antelop-external-data",
                "location": "/features_behaviour",
                "access_key": username,
                "secret_key": password,
            },
            "dlcmodel": {
                "protocol": "s3",
                "endpoint": config["s3"]["host"],
                "bucket": "antelop-external-data",
                "location": "/dlcmodel",
                "access_key": username,
                "secret_key": password,
            },
            "behaviour_video": {
                "protocol": "s3",
                "endpoint": config["s3"]["host"],
                "bucket": "antelop-external-data",
                "location": "/behaviour_video",
                "access_key": username,
                "secret_key": password,
            },
            "labelled_frames": {
                "protocol": "s3",
                "endpoint": config["s3"]["host"],
                "bucket": "antelop-external-data",
                "location": "/labelled_frames",
                "access_key": username,
                "secret_key": password,
            },
            "evaluated_frames": {
                "protocol": "s3",
                "endpoint": config["s3"]["host"],
                "bucket": "antelop-external-data",
                "location": "/evaluated_frames",
                "access_key": username,
                "secret_key": password,
            },
        }

    conn = dj.conn(reset=True)

    if not IN_CONTAINER:
        dj.config["query_cache"] = cache_dir
        conn.set_query_cache(query_cache="main")
    else:
        dj.config["query_cache"] = None
        conn.set_query_cache(query_cache=None)

    return conn
