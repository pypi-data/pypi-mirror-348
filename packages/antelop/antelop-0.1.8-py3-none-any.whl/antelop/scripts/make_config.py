import toml
from pathlib import Path, PurePosixPath
from antelop.utils.os_utils import get_config_path, github_repo_exists


def run():
    print("\nWelcome to the antelop configuration setup tool.")

    config_path = get_config_path()
    if Path(config_path).exists():
        print(
            f"\nWarning, {config_path} already exists. Continuing will overwrite your current configuration."
        )
        cont = None
        while cont not in ["y", "n"]:
            cont = input("\nWould you like to continue? (y/n)\n")
            if cont == "n":
                exit()
            elif cont != "y":
                print("\nInvalid input. Please try again.\n")

    toml_dict = {"deployment": {"deployment": "local"}}

    toml_dict["mysql"] = {}
    toml_dict["mysql"]["host"] = input("\nPlease enter the MySQL host:\n")

    toml_dict["s3"] = {}
    toml_dict["s3"]["host"] = input("\nPlease enter the S3 host:\n")

    toml_dict["folders"] = {}
    folder_names = []  # Keep track of folder names for cluster folder configuration
    status = True
    print(
        "\nYou can add as many folders as you like which will be made searchable within Antelop."
    )
    print(
        "For example, you can add your home directory, plus a mounted cluster directory."
    )
    print("Please give each an identifiable name and path.")

    while status == True:
        name = input("\nPlease enter the folder name:\n")
        path = input("\nPlease enter the (absolute) folder path:\n")

        try:
            assert Path(path).is_absolute(), "\nInvalid path. Please try again."
        except AssertionError as e:
            print(e)
            continue

        toml_dict["folders"][name] = path
        folder_names.append(name)  # Add to the list of folder names
        cont = None

        while cont not in ["y", "n"]:
            cont = input("\nWould you like to add another folder? (y/n)\n")
            if cont == "n":
                status = False
            elif cont != "y":
                print("\nInvalid input. Please try again.\n")

    # Add cluster folders configuration
    toml_dict["cluster_folders"] = {}
    print("\nNow, let's configure which folders also exist on the cluster and their paths.")
    for name in folder_names:
        cont = None
        while cont not in ["y", "n"]:
            cont = input(f"\nDoes the folder '{name}' exist on the cluster? (y/n)\n")
            if cont not in ["y", "n"]:
                print("\nInvalid input. Please try again.\n")
        
        if cont == "y":
            status = False
            while not status:
                try:
                    cluster_path = input(f"\nPlease enter the cluster path for '{name}':\n")
                    assert PurePosixPath(cluster_path).is_absolute(), "\nInvalid path. Please try again."
                except AssertionError as e:
                    print(e)
                    print("Please try again.\n")
                else:
                    toml_dict["cluster_folders"][name] = cluster_path
                    status = True
        else:
            toml_dict["cluster_folders"][name] = None

    toml_dict["analysis"] = {}
    status = True
    print(
        "\nYou can add folders that contain your custom analysis scripts written to work with antelop."
    )
    print("Antelop will automatically load all functions found in these folders.")

    toml_dict["analysis"]["folders"] = []

    cont = None
    while cont not in ["y", "n"]:
        cont = input("\nWould you like to add a custom analysis path? (y/n)\n")
        if cont == "n":
            status = False
        elif cont != "y":
            print("\nInvalid input. Please try again.\n")

    while status == True:
        path = input("\nPlease enter the (absolute) folder path:\n")

        try:
            assert Path(path).is_absolute(), "\nInvalid path. Please try again."
        except AssertionError as e:
            print(e)
            continue

        toml_dict["analysis"]["folders"].append(path)
        cont = None

        while cont not in ["y", "n"]:
            cont = input("\nWould you like to add another folder? (y/n)\n")
            if cont == "n":
                status = False
            elif cont != "y":
                print("\nInvalid input. Please try again.\n")

    toml_dict["multithreading"] = {}
    print("\nAntelop can use multiple cores in the background to speed up processing.")
    status = False
    while not status:
        try:
            cores = input("Please enter the maximum number of cores to use:\n")
            assert cores.isdigit(), "\nThe number of cores must be an integer."
        except AssertionError as e:
            print(e)
            print("Please try again.\n")
        else:
            toml_dict["multithreading"]["max_workers"] = int(cores)
            status = True

    toml_dict["computation"] = {}
    toml_dict["computation"]["host"] = input(
        "\nPlease enter the host name of the compute cluster:\n"
    )

    status = False
    while not status:
        try:
            basedir = input(
                "\nPlease enter the base directory for your antelop installation on the compute cluster:\n"
            )
            assert PurePosixPath(basedir).is_absolute(), (
                "\nInvalid path. Please try again."
            )
        except AssertionError as e:
            print(e)
            print("Please try again.\n")
        else:
            toml_dict["computation"]["basedir"] = basedir
            status = True

    status = False
    while not status:
        try:
            antelop_data = input(
                "\nPlease enter the path to your antelop data directory on the compute cluster as mounted on this machine:\n"
            )
            assert Path(antelop_data).is_absolute(), "\nInvalid path. Please try again."
        except AssertionError as e:
            print(e)
            print("Please try again.\n")
        else:
            toml_dict["computation"]["antelop_data"] = antelop_data
            status = True

    toml_dict["github"] = {}
    status = True
    print(
        "\nYou can add GitHub repositories that contain your custom analysis scripts written to work with antelop."
    )
    print("Please give each an identifiable name and URL.")

    cont = None
    while cont not in ["y", "n"]:
        cont = input("\nWould you like to add a GitHub repository? (y/n)\n")
        if cont == "n":
            status = False
        elif cont != "y":
            print("\nInvalid input. Please try again.\n")

    while status == True:
        name = input("\nPlease enter the folder name:\n")
        path = input("\nPlease enter the GitHub URL:\n")

        try:
            assert github_repo_exists(path), "\nInvalid URL. Please try again."
        except AssertionError as e:
            print(e)
        else:
            toml_dict["github"][name] = path
            cont = None

        while cont not in ["y", "n"]:
            cont = input("\nWould you like to add another folder? (y/n)\n")
            if cont == "n":
                status = False
            elif cont != "y":
                print("\nInvalid input. Please try again.\n")

    print(f"\nWriting configuration to {config_path}")

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        toml.dump(toml_dict, f)
