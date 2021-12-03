# -*- coding: UTF-8 -*-
""""
Created on 03.12.21

:author:     Martin Dočekal
"""
import argparse
import atexit
import json
import logging
import re
import sys
from collections import defaultdict
from multiprocessing import active_children
from typing import Dict, Any, Optional, TextIO

from tqdm import tqdm
from windpyutils.args import ExceptionsArgumentParser, ArgumentParserError
from windpyutils.visual.text import print_histogram

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

        stats_parser = subparsers.add_parser("stats", help="Statistics for mag.")
        stats_parser.add_argument("full", help="Path to full record jsonl MAG file. "
                                              "You can obtain it be the full argument.", type=str)
        stats_parser.add_argument("--title-filter", help="Python regex for title. Can be used for filtration.",
                                  type=str)
        stats_parser.set_defaults(func=stats)

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


def stats_count(f: TextIO, title_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculates statistics for given file.

    :param f: Opened MAG .jsonl file with full records
    :param title_filter: regex for filtering records according to title
        all others are not considered in stats just in total_cnt
    :return: Results in form of dictionary:
        total_cnt   total number of records
        passed_filter_cnt   number of records that passed through the filter
        year_hist   dict year -> number of records with this year
        fields_hist field -> number of times this field of study occured
    """
    total_cnt = 0
    passed_filter_cnt = 0
    year_hist = defaultdict(int)
    fields_hist = defaultdict(int)

    for line in f:
        total_cnt += 1
        record = json.loads(line)
        if not title_filter or re.match(title_filter, record["OriginalTitle"]):
            passed_filter_cnt += 1
            year_hist[record["Year"]] += 1

            for field in record["Fields"]:
                fields_hist[field] += 1

    return {
        "total_cnt": total_cnt,
        "passed_filter_cnt": passed_filter_cnt,
        "year_hist": year_hist,
        "fields_hist": fields_hist
    }


def stats(args: argparse.Namespace):
    """
    Statistics for full record of mag.

    :param args: User arguments.
    """

    stats_res = stats_count(args.full, args.title_filter)
    print(f"Total number of records:\t{stats_res['total_cnt']}")
    print(f"Total number of records that passed through the filter:\t{stats_res['passed_filter_cnt']}")
    print(f"Total number of records that passed through the filter:\t{stats_res['passed_filter_cnt']}")

    print("\nYears")
    print_histogram(sorted(stats_res["year_hist"].items(), key=lambda x: x[1], reverse=True))

    print("\nFields of study")
    print_histogram(sorted(stats_res["fields_hist"].items(), key=lambda x: x[1], reverse=True))


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
