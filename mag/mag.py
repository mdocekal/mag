# -*- coding: UTF-8 -*-
""""
Created on 29.11.21
This module contains class for reading Microsoft Academic Graph.

:author:     Martin Dočekal
"""
import logging
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Dict, Any, Type, Optional, Sequence, Callable, Generator, TextIO

from mag.utils import bin_search

PAPERS_SCHEMA = [
    ("PaperId", int),
    ("Rank", int),
    ("Doi", str),
    ("DocType", str),
    ("PaperTitle", str),
    ("OriginalTitle", str),
    ("BookTitle", str),
    ("Year", int),
    ("Date", str),
    ("OnlineDate", str),
    ("Publisher", str),
    ("JournalId", int),
    ("ConferenceSeriesId", int),
    ("ConferenceInstanceId", int),
    ("Volume", str),
    ("Issue", str),
    ("FirstPage", str),
    ("LastPage", str),
    ("ReferenceCount", int),
    ("CitationCount", int),
    ("EstimatedCitation", int),
    ("OriginalVenue", str),
    ("FamilyId", int),
    ("FamilyRank", int),
    ("DocSubTypes", str),
    ("CreatedDate", str)
]

PAPER_AUTHOR_AFFILIATIONS_SCHEMA = [
    ("PaperId", int),
    ("AuthorId", int),
    ("AffiliationId", int),
    ("AuthorSequenceNumber", int),
    ("OriginalAuthor", str),
    ("OriginalAffiliation", str),
]

AUTHORS_SCHEMA = [
    ("AuthorId", int),
    ("Rank", int),
    ("NormalizedName", str),
    ("DisplayName", str),
    ("LastKnownAffiliationId", int),
    ("PaperCount", int),
    ("PaperFamilyCount", int),
    ("CitationCount", int),
    ("CreatedDate", str)
]

PAPER_REFERENCES = [
    ("PaperId", int),
    ("PaperReferenceId", int)
]

FIELDS_OF_STUDY = [
    ("FieldOfStudyId", int),
    ("Rank", int),
    ("NormalizedName", str),
    ("DisplayName", str),
    ("MainType", str),
    ("Level", int),
    ("PaperCount", int),
    ("PaperFamilyCount", int),
    ("CitationCount", int),
    ("CreatedDate", str),
]

PAPER_FIELDS_OF_STUDY = [
    ("PaperId", int),
    ("FieldOfStudyId", int),
    ("Score", float)
]

JOURNALS = [
    ("JournalId", int),
    ("Rank", int),
    ("NormalizedName", str),
    ("DisplayName", str),
    ("Issn", str),
    ("Publisher", str),
    ("Webpage", str),
    ("PaperCount", int),
    ("PaperFamilyCount", int),
    ("CitationCount", int),
    ("CreatedDate", str)
]


class MAG:
    """
    Reading Microsoft Academic Graph.
    """

    def __init__(self, p: str):
        """
        Initialization of MAG.

        :param p: Path to root folder this root folder should contain following folders:
            mag
                Papers.txt
                PaperAuthorAffiliations.txt
        """

        self._path = Path(p)
        self._mag_path = self._path.joinpath("mag")
        self._advanced_path = self._path.joinpath("advanced")
        self._opened_files = {}

    def __enter__(self) -> "MAG":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for _, f in self._opened_files.items():
            f.close()

        self._opened_files = {}

    def _open_file(self, p: str) -> TextIO:
        """
        Opens file on given path for reading. If the file was already opened it does not open it again.
        """
        try:
            return self._opened_files[p]
        except KeyError:
            self._opened_files[p] = open(p, "r")

        return self._opened_files[p]

    @staticmethod
    def convert_row(row: str, schema: List[Tuple[str, Type]]) -> Dict[str, Any]:
        """
        Converts row according to given schema.
        works in place

        :param row: the row for conversion
        :param schema: the schema that is used
        :return: converted row
        """
        row = row.rstrip("\n").split("\t")
        res = {}
        for i, (column, c_type) in enumerate(schema):
            try:
                res[column] = c_type(row[i])
            except (ValueError, TypeError):
                # problems with type conversion
                res[column] = None
            except IndexError:
                # there are not enough columns
                for c, _ in schema[i:]:
                    res[c] = None
                break

        return res

    @property
    def papers(self) -> Generator[Dict[str, Any], None, None]:
        """
        Returns generator of papers.

        See PAPERS_SCHEMA for more info about its content.
        """

        f = self._open_file(str(self._mag_path.joinpath("Papers.txt")))

        for row in f:
            yield self.convert_row(row, PAPERS_SCHEMA)

    def paper_author_affiliations(self, f_offset: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Returns data frame of paper_author_affiliations.

        See PAPER_AUTHOR_AFFILIATIONS_SCHEMA for more info about its content.

        :param f_offset: If you pass this argument the file offset will be shifted to that value before generating.
        """
        f = self._open_file(str(self._mag_path.joinpath("PaperAuthorAffiliations.txt")))

        if f_offset is not None:
            f.seek(f_offset)
        for row in f:
            yield self.convert_row(row, PAPER_AUTHOR_AFFILIATIONS_SCHEMA)

    def paper_references(self, f_offset: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Returns generator of paper references.

        See PAPER_REFERENCES for more info about its content.

        :param f_offset: If you pass this argument the file offset will be shifted to that value before generating.
        """
        f = self._open_file(str(self._mag_path.joinpath("PaperReferences.txt")))

        if f_offset is not None:
            f.seek(f_offset)
        for row in f:
            yield self.convert_row(row, PAPER_REFERENCES)

    def fields_of_study(self, f_offset: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Returns generator of fields of study.

        See FIELDS_OF_STUDY for more info about its content.

        :param f_offset: If you pass this argument the file offset will be shifted to that value before generating.
        """
        f = self._open_file(str(self._advanced_path.joinpath("FieldsOfStudy.txt")))

        if f_offset is not None:
            f.seek(f_offset)
        for row in f:
            yield self.convert_row(row, FIELDS_OF_STUDY)

    def paper_fields_of_study(self, f_offset: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Returns generator of paper fields of study.

        See PAPER_FIELDS_OF_STUDY for more info about its content.

        :param f_offset: If you pass this argument the file offset will be shifted to that value before generating.
        """
        f = self._open_file(str(self._advanced_path.joinpath("PaperFieldsOfStudy.txt")))

        if f_offset is not None:
            f.seek(f_offset)
        for row in f:
            yield self.convert_row(row, PAPER_FIELDS_OF_STUDY)

    def journals(self, f_offset: Optional[int] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Returns generator of journals.

        See JOURNALS for more info about its content.

        :param f_offset: If you pass this argument the file offset will be shifted to that value before generating.
        """
        f = self._open_file(str(self._mag_path.joinpath("Journals.txt")))

        if f_offset is not None:
            f.seek(f_offset)
        for row in f:
            yield self.convert_row(row, JOURNALS)

    @staticmethod
    def make_index(p: str) -> Optional[Tuple[List[int], List[int]]]:
        """
        For files with non-decreasing paper ids makes index of file offsets for first record of each paper id.
            we are checking the non-decreasing property while reading
        Example of file:
            file offset     paper id
            0               100
            1000            100
            2000            100
            3000            200
            3100            300

        Result:
            paper_ids_index: [100, 200, 300]
            paper_ids_index_offsets: [0, 3000, 3100]

        :param p: path to given file
        :return: tuple of two lists:
            paper_ids_index
            paper_ids_index_offsets

            or None when the Violation of non-decreasing property occurs
        """
        paper_ids_index = []
        paper_ids_index_offsets = []

        with open(p) as f:
            last_paper_id_paper_author_affiliations = -math.inf  # for checking the non-decreasing property
            beg_offset = f.tell()
            line = f.readline()
            while line:
                paper_id = int(line.split("\t", maxsplit=1)[0])

                if last_paper_id_paper_author_affiliations != paper_id:
                    # there is a new one
                    paper_ids_index.append(paper_id)
                    paper_ids_index_offsets.append(beg_offset)

                if last_paper_id_paper_author_affiliations > paper_id:
                    # Violation of non-decreasing property for
                    return None
                last_paper_id_paper_author_affiliations = paper_id

                beg_offset = f.tell()
                line = f.readline()

        return paper_ids_index, paper_ids_index_offsets

    @staticmethod
    def search_field_for_paper(paper_id: int, paper_ids_index: Sequence[int],
                               paper_ids_index_offsets: Sequence[int], gen_fun: Callable[[int], Generator],
                               field_name: str,  use_intern: bool = False) -> List[Any]:
        """
        Goes through generator and accepts all records until a different paper_id is reached.
        It expects that the generator is generating records in non-decreasing order in terms of paper ids.

        :param paper_id: value of PaperId of our interest
        :param paper_ids_index: index of all ids that is used for selecting file offset that is used to initialize
            generator so it will begins from line that contains givne paper id
            if given paper id is missing empty list is returned
        :param paper_ids_index_offsets: corresponding list of file offsets for paper_ids_index
        :param gen_fun: A generator that accepts file offset that is determining where to start reading
        :param field_name: Name of field that should be gathered.
        :param use_intern: If true uses sys.intern on value of field with field_name.
        :return: values of field with field_name
        """

        start_offset = bin_search(paper_ids_index, paper_id)

        if start_offset is None:
            # is missing
            return []

        res = []

        for row in gen_fun(paper_ids_index_offsets[start_offset]):
            if row["PaperId"] != paper_id:
                break
            res.append(sys.intern(row[field_name]) if use_intern else row[field_name])

        return res

    def gen_full_records(self, field_of_study_score_threshold: float = 0.0) -> Generator[Dict[str, Any], None, None]:
        """
        Generates tuple with mag id, title, year, authors, references, and fields of study.

        If any of these fields is missing than the whole record is skipped.

        :param field_of_study_score_threshold: The score of field of study must be greater than this.
        :return: Generator of dicts.
        """

        logging.log(logging.INFO, "reading PaperAuthorAffiliations")
        paper_authors = defaultdict(list)
        for row in self.paper_author_affiliations():
            paper_authors[row["PaperId"]].append(row["OriginalAuthor"])

        logging.log(logging.INFO, "reading PaperReferences")
        paper_references = defaultdict(list)
        for row in self.paper_references():
            paper_references[row["PaperId"]].append(row["PaperReferenceId"])

        logging.log(logging.INFO, "reading FieldsOfStudy")
        fields_of_study = {
            fields_of_study_row["FieldOfStudyId"]: fields_of_study_row["DisplayName"]
            for fields_of_study_row in self.fields_of_study()
        }

        papers_fields_of_study = defaultdict(list)
        logging.log(logging.INFO, "reading PaperFieldsOfStudy")
        for row in self.paper_fields_of_study():
            if row["Score"] > field_of_study_score_threshold:
                papers_fields_of_study[row["PaperId"]].append(row["FieldOfStudyId"])

        journals = defaultdict(str)
        logging.log(logging.INFO, "reading Journals")
        for row in self.journals():
            journals[row["JournalId"]] = row["DisplayName"]

        logging.log(logging.INFO, "generating")
        for paper_row in self.papers:
            if not(paper_row["PaperId"] and paper_row["OriginalTitle"] and paper_row["Year"]):
                # we are interested only in the full records
                continue

            try:
                fields = [fields_of_study[field_id] for field_id in papers_fields_of_study[paper_row["PaperId"]]]
                authors = paper_authors[paper_row["PaperId"]]
                references = paper_references[paper_row["PaperId"]]
            except KeyError:
                #  we are interested only in the full records
                continue

            if fields and authors and references:
                yield {
                        "PaperId": paper_row["PaperId"],
                        "OriginalTitle": paper_row["OriginalTitle"],
                        "Year": paper_row["Year"],
                        "Authors": authors,
                        "References": references,
                        "Fields": fields,
                        "Doi": paper_row["Doi"],
                        "Journal": journals[paper_row["JournalId"]] if paper_row["JournalId"] in journals else ""
                    }
