# -*- coding: UTF-8 -*-
""""
Created on 03.12.21

:author:     Martin Dočekal
"""
import argparse
import atexit
import json
import logging
import sys
from multiprocessing import active_children

from tqdm import tqdm
from windpyutils.args import ExceptionsArgumentParser, ArgumentParserError

from mag.mag import MAG


class ArgumentsManager(object):
    """
    Parsers arguments for script.
    """

    @classmethod
    def parse_args(cls):
        """
        Performs arguments parsing.

        :param cls: arguments class
        :returns: Parsed arguments.
        """

        parser = ExceptionsArgumentParser(description="Package for working with MAG dataset.")

        subparsers = parser.add_subparsers()

        full_parser = subparsers.add_parser("full",
                                                      help="Creates from original MAG files. Full records jsonl files "
                                                           "containing samples with mag id, title, year, authors, "
                                                           "references, and fields of study. If any of these fields "
                                                           "is missing than the whole record is skipped."
                                                           "Results are at stdout")
        full_parser.add_argument("mag", help="Path to root folder, this root folder should contain mag and advanced "
                                             "folders.", type=str)
        full_parser.add_argument("--field-of-study-threshold",
                                 help="The score of field of study must be greater than this.",
                                 type=float)
        full_parser.set_defaults(func=create_full)

        if len(sys.argv) < 2:
            parser.print_help()
            return None
        try:

            parsed = parser.parse_args()

        except ArgumentParserError as e:
            parser.print_help()
            print("\n" + str(e), file=sys.stdout, flush=True)
            return None

        return parsed


def create_full(args: argparse.Namespace):
    """
    Creates from original MAG files. Full records jsonl files containing samples
    with mag id, title, year, authors, references, and fields of study.
    If any of these fields is missing than the whole record is skipped.

    Results are at stdout

    :param args: User arguments.
    """
    mag = MAG(args.mag)

    for record in tqdm(mag.gen_full_records(args.field_of_study_threshold), desc="Generating full records"):
        print(json.dumps(record))


def kill_children():
    """
    Kills all subprocesses created by multiprocessing module.
    """

    for p in active_children():
        p.terminate()


def main():
    logging.basicConfig(format='%(process)d: %(levelname)s : %(asctime)s : %(message)s', level=logging.DEBUG)

    atexit.register(kill_children)
    args = ArgumentsManager.parse_args()

    if args is not None:
        args.func(args)
    else:
        exit(1)


if __name__ == '__main__':
    main()
