# Copyright (c) 2024, InfinityQ Technology, Inc.
import abc
import re
from typing import List, Union
from warnings import warn

from titanq.errors import MpsMalformedFileError, MpsMissingValueError

from .model import (
    MPSBounds,
    MPSColumns,
    MPSEndata,
    MPSName,
    MPSQuadobj,
    MPSRanges,
    MPSRhs,
    MPSRow,
)
from .utils import BoundsType, ColumnsType, RowsType, SectionType, UniqueList
from ._visitor import LineSection


# Following this IBM documentation, this parser currently uses spaces as delimiters
# https://www.ibm.com/docs/en/icos/22.1.0?topic=standard-records-in-mps-format

# For integer variables both ways are supported (COLUMNS via markers and in the bounds section)
# https://www.ibm.com/docs/en/icos/22.1.1?topic=extensions-integer-variables-in-mps-files

# Integer variables markers in COLUMNS
_INTEGER_START = "'INTORG'" # 'INTORG'
_INTEGER_END = "'INTEND'" # 'INTEND'

_MPS_FILE_DEFAULT_NAME = "IMPORTED_BY_TITANQ"

# common regular expressions used in the MPS parser
# Matches "C1 R1 -2.0E+10"
SINGLE_VALUE_PATTERN = re.compile(r"^(\S+)\s+(\S+)\s+([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?)\s*$")
# Matches "C1 R1 2.0 R2 3.0" | "C1 R1 -2.0E+10 R2 3.0E+10"
DOUBLE_VALUE_PATTERN = re.compile(r"^(\S+)\s+(\S+)\s+([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?)\s+(\S+)\s+([-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?)\s*$")



def _failed_to_parsed_at_section_and_line(section_name: str, line_index: int):
    raise MpsMalformedFileError(
        f"Failed to parse a line in section '{section_name}' (line: {line_index})"
    )


class SectionParser(abc.ABC):
    """class interface for any section needed to be parsed"""
    def __init__(self, start_index: int, lines: List[str]) -> None:
        super().__init__()
        self._start_index = start_index
        self._lines = lines

    def parse() -> List[LineSection]:
        """parse the given lines"""


class NameParser(SectionParser):
    """parses the NAME section of an .mps file into python objects"""

    def __init__(self, start_index, lines):
        super().__init__(start_index, lines)

        # Matches "NAME" or "NAME SOMENAME"
        self._name_pattern = re.compile(r"^NAME\s*(.*?)\s*$")

    def parse(self) -> List[MPSName]:
        if len(self._lines) > 1:
            raise MpsMalformedFileError(f"Found more than 2 lines for section '{SectionType.NAME}'")

        name_pattern_match = self._name_pattern.match(self._lines[0])
        if name_pattern_match:
            value = name_pattern_match.group(1)

            # give it a default name if nothing was set
            name = value if value else _MPS_FILE_DEFAULT_NAME
            return [MPSName(name=name)]

        _failed_to_parsed_at_section_and_line(SectionType.NAME, self._start_index)

class RowsParser(SectionParser):
    """parses the ROWS section of an .mps file into python objects"""

    def __init__(self, start_index: int, lines: List[str]) -> None:
        super().__init__(start_index, lines)
        self._rows_identifier = UniqueList(f"Found duplicates in the '{SectionType.ROWS}' section")
        self._free_row = None

        # Matches "N ANYTHING" | "E ANYTHING" | "L ANYTHING" | "G ANYTHING"
        self._rows_pattern = re.compile(r"^([NELG])\s+(\S+)\s*$")

    def _set_free_row(self, free_row_identifier):
        if self._free_row is not None:
            warn(
                f"Found a free row {RowsType.FREE_ROW} identified as '{free_row_identifier}', "
                f"but one was already identified with: '{self._free_row}'. New one will be ignored"
            )
        self._free_row = free_row_identifier


    def parse(self) -> List[MPSRow]:
        # possible format --> ['N', 'OBJ']
        rows = []
        for index, line in enumerate(self._lines):
            rows_pattern_match = self._rows_pattern.match(line)
            if rows_pattern_match:
                sense = rows_pattern_match.group(1)
                row_identifier = rows_pattern_match.group(2)

                if sense == RowsType.FREE_ROW:
                    self._set_free_row(row_identifier)

                rows.append(MPSRow(sense=sense, identifier=row_identifier))
                continue

            _failed_to_parsed_at_section_and_line(SectionType.ROWS, self._start_index + index)

        if self._free_row is None:
            raise MpsMissingValueError(f"Did not find a free row '{RowsType.FREE_ROW}' in the '{SectionType.ROWS}' section")

        return rows


class ColumnParser(SectionParser):
    """parses the COLUMNS section of an .mps file into python objects"""

    def __init__(self, start_index: int, lines: List[str]) -> None:
        super().__init__(start_index, lines)
        self._type = ColumnsType.CONTINUOUS

        self._single_value_pattern = SINGLE_VALUE_PATTERN
        self._double_value_pattern = DOUBLE_VALUE_PATTERN
        # Matches "SOMENAME 'MARKER' 'INTORG'"
        self._start_int_pattern = re.compile(r"^\S+\s+'MARKER'\s+'INTORG'\s*$")
        # Matches "SOMENAME 'MARKER' 'INTEND'"
        self._end_int_pattern = re.compile(r"^\S+\s+'MARKER'\s+'INTEND'\s*$")

    def _activate_integer_mode(self): self._type = ColumnsType.INTEGER
    def _deactivate_integer_mode(self): self._type = ColumnsType.CONTINUOUS

    def _handle_marker_line(self, value: str) -> None:
        if value == _INTEGER_START:
            self._activate_integer_mode()
        elif value == _INTEGER_END:
            self._deactivate_integer_mode()

    def parse(self) -> List[MPSColumns]:
        columns = []
        for index, line in enumerate(self._lines):
            single_pattern_match = self._single_value_pattern.match(line)
            if single_pattern_match:
                columns.append(MPSColumns(
                    identifier=single_pattern_match.group(1),
                    row_identifier=single_pattern_match.group(2),
                    coeff=float(single_pattern_match.group(3)),
                    type=self._type
                ))
                continue

            double_pattern_match = self._double_value_pattern.match(line)
            if double_pattern_match:
                columns.append(MPSColumns(
                    identifier=double_pattern_match.group(1),
                    row_identifier=double_pattern_match.group(2),
                    coeff=float(double_pattern_match.group(3)),
                    type=self._type
                ))
                columns.append(MPSColumns(
                    identifier=double_pattern_match.group(1),
                    row_identifier=double_pattern_match.group(4),
                    coeff=float(double_pattern_match.group(5)),
                    type=self._type
                ))
                continue

            start_int_pattern_match = self._start_int_pattern.match(line)
            if start_int_pattern_match:
                self._handle_marker_line(_INTEGER_START)
                continue

            end_int_pattern_match = self._end_int_pattern.match(line)
            if end_int_pattern_match:
                self._handle_marker_line(_INTEGER_END)
                continue

            _failed_to_parsed_at_section_and_line(SectionType.COLUMNS, self._start_index + index)

        return columns


class RhsParser(SectionParser):
    """parses the RHS section of an .mps file into python objects"""

    def __init__(self, start_index, lines):
        super().__init__(start_index, lines)

        self._single_value_pattern = SINGLE_VALUE_PATTERN
        self._double_value_pattern = DOUBLE_VALUE_PATTERN

    def parse(self) -> List[MPSRhs]:
        rhs = []
        for index, line in enumerate(self._lines):
            single_pattern_match = self._single_value_pattern.match(line)
            if single_pattern_match:
                rhs.append(MPSRhs(
                    identifier=single_pattern_match.group(1),
                    row_identifier=single_pattern_match.group(2),
                    coeff=float(single_pattern_match.group(3))
                ))
                continue

            double_pattern_match = self._double_value_pattern.match(line)
            if double_pattern_match:
                rhs.append(MPSRhs(
                    identifier=double_pattern_match.group(1),
                    row_identifier=double_pattern_match.group(2),
                    coeff=float(double_pattern_match.group(3))
                ))
                rhs.append(MPSRhs(
                    identifier=double_pattern_match.group(1),
                    row_identifier=double_pattern_match.group(4),
                    coeff=float(double_pattern_match.group(5))
                ))
                continue

            _failed_to_parsed_at_section_and_line(SectionType.ROWS, self._start_index + index)

        return rhs


class RangesParser(SectionParser):
    """parses the RANGES section of an .mps file into python objects"""

    def __init__(self, start_index, lines):
        super().__init__(start_index, lines)

        self._single_value_pattern = SINGLE_VALUE_PATTERN
        self._double_value_pattern = DOUBLE_VALUE_PATTERN

    def parse(self) -> List[MPSRanges]:
        ranges = []
        for index, line in enumerate(self._lines):
            single_pattern_match = self._single_value_pattern.match(line)
            if single_pattern_match:
                ranges.append(MPSRanges(
                    identifier=single_pattern_match.group(1),
                    row_identifier=single_pattern_match.group(2),
                    coeff=float(single_pattern_match.group(3))
                ))
                continue

            double_pattern_match = self._double_value_pattern.match(line)
            if double_pattern_match:
                ranges.append(MPSRanges(
                    identifier=double_pattern_match.group(1),
                    row_identifier=double_pattern_match.group(2),
                    coeff=float(double_pattern_match.group(3))
                ))
                ranges.append(MPSRanges(
                    identifier=double_pattern_match.group(1),
                    row_identifier=double_pattern_match.group(4),
                    coeff=float(double_pattern_match.group(5))
                ))
                continue

            _failed_to_parsed_at_section_and_line(SectionType.RANGES, self._start_index + index)

        return ranges


class BoundParser(SectionParser):
    """parses the BOUNDS section of an .mps file into python objects"""
    def __init__(self, start_index, lines):
        super().__init__(start_index, lines)

        # Matches "FR A B" "LO A B -2.0E+10", the first item needs to be a valid bounds option, see 'BoundsType'
        self._bounds_pattern = re.compile(r"^(LO|LI|UP|UI|FX|FR|MI|PL|BV|SC)\s+(\S+)\s+(\S+)(\s+[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?)?\s*$")

    def parse(self) -> List[MPSBounds]:
        bounds = []
        for index, line in enumerate(self._lines):
            bounds_pattern_match = self._bounds_pattern.match(line)
            if bounds_pattern_match:
                value = bounds_pattern_match.group(4)
                bounds.append(MPSBounds(
                    identifier=bounds_pattern_match.group(2),
                    type=BoundsType(bounds_pattern_match.group(1)),
                    column_identifier=bounds_pattern_match.group(3),
                    value=float(value) if value else None
                ))
                continue

            _failed_to_parsed_at_section_and_line(SectionType.BOUNDS, self._start_index + index)

        return bounds


class QuadobjParser(SectionParser):
    """parses the QUADOBJ or QMATRIX section of an .mps file into python objects"""

    def __init__(self, start_index: int, lines: List[str], type: Union[SectionType.QUADOBJ, SectionType.QMATRIX]) -> None:
        super().__init__(start_index, lines)
        self._type = type

        self._quadobj_pattern = SINGLE_VALUE_PATTERN

    def parse(self) -> List[MPSQuadobj]:
        quadobj = []
        for index, line in enumerate(self._lines):
            quadobj_pattern_match = self._quadobj_pattern.match(line)
            if quadobj_pattern_match:
                row = quadobj_pattern_match.group(1)
                column = quadobj_pattern_match.group(2)
                value = quadobj_pattern_match.group(3)

                quadobj.append(MPSQuadobj(row_identifier=row, column_identifier=column, value=float(value)))

                # if QUADOBJ is set instead of QMATRIX, write another line but inversed to fill the matrix symmetrically
                if self._type == SectionType.QUADOBJ and row != column:
                    quadobj.append(MPSQuadobj(row_identifier=column, column_identifier=row, value=float(value)))
                continue

            _failed_to_parsed_at_section_and_line(self._type, self._start_index + index)

        return quadobj


class EndataParser(SectionParser):
    """parses the ENDATA section of an .mps file into a python objects"""

    def parse(self) -> List[MPSEndata]:
        # possible format --> ['ENDATA'] # no need to parse here
        if len(self._lines) > 1:
            raise MpsMalformedFileError(f"Found more than 2 lines for section '{SectionType.ENDATA}'")

        return [MPSEndata()]