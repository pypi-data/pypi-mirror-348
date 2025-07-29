#!/usr/bin/env python

import argparse
import logging
import pathlib
import zipfile

# local imports
from esi_utils_pager.configurator import Configurator


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter,
):
    pass


def configure(args):
    configurator = Configurator(
        args.data_folder, args.zipfile, pop_zipfile=args.population_file
    )
    cfg_dict, extract_files = configurator.configure()
    configurator.write(cfg_dict, extract_files)


def main():
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    desc = """Program to automate initial PAGER configuration.

     
    """
    parser = argparse.ArgumentParser(description=desc, formatter_class=CustomFormatter)
    parser.add_argument(
        "zipfile", help="Path to zip file containing all necessary PAGER data."
    )
    dhelp = (
        "Path to top level data folder for PAGER input. \n"
        "This folder will contain all of the data files \n"
        "from the model data zipfile. Population data \n"
        "will be stored in a 'population' sub-directory.\n"
    )
    parser.add_argument(
        "data_folder",
        default=None,
        help=dhelp,
    )
    parser.add_argument(
        "-p",
        "--population-file",
        help=(
            "Path to zip file containing many years of landscan population data. "
            "Useful only if use case includes running many historical events."
        ),
        default=None,
    )
    parser.add_argument(
        "-c",
        "--configuration-type",
        choices=["pagerapp", "pagerlite"],
        help=(
            "Specify type of PAGER installation: "
            " - pagerapp means that you will be setting up a full PAGER application "
            " - pagerlite means you are just running code found in esi-utils-pager"
        ),
        default="pagerlite",
    )

    args = parser.parse_args()
    configure(args)


if __name__ == "__main__":
    main()
