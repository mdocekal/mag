# -*- coding: UTF-8 -*-
"""
Created on 13.12.21
This module contains class for reading .jsonl mag dataset.

:author:     Martin Dočekal
"""
import json

from typing import Dict, Any


class JsonlDataset:
    """
    MAG dataset in .jsonl format reader.
    """

    def __init__(self, p: str):
        """
        Initializes dataset, but doesn't open it.

        :param p: Path to .jsonl file.
        """
        self.path_to = p
        self.file = None
        self._id_2_line_offsets = {}
        self._index_file()

    def _index_file(self):
        """
        Makes index of line offsets.
        """

        with open(self.path_to, "r") as f:
            line_offset = 0
            line = f.readline()
            while line:
                record = json.loads(line)
                self._id_2_line_offsets[record["PaperId"]] = line_offset
                line_offset = f.tell()
                line = f.readline()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __len__(self) -> int:
        """
        Number of lines in the file.

        :return: Number of lines in the file.
        """
        return len(self._id_2_line_offsets)

    def open(self) -> "JsonlDataset":
        """
        Open the file if it was closed, else it is just empty operation.

        :return: Returns the object itself.
        :rtype: RandomLineAccessFile
        """

        if self.file is None:
            self.file = open(self.path_to, "r")
        return self

    def close(self):
        """
        Closes the file.
        """

        if self.file is not None:
            self.file.close()
            self.file = None

    def __getitem__(self, mag_id) -> Dict[str, Any]:
        """
        Get record with given mag id from file.

        :param mag_id: id of the record
        :return: record for given mag id
        :raise RuntimeError: When the file is not opened.
        :raise KeyError: for unknown id
        """
        if self.file is None:
            raise RuntimeError("Firstly open the file.")

        self.file.seek(self._id_2_line_offsets[mag_id])
        return json.loads(self.file.readline())
