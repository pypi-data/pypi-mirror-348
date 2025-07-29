"""A window processing evaluation on timeseries."""

from datetime import timedelta
from logging import getLogger, DEBUG
from typing import override
from collections.abc import Hashable

import pandas as pd

from pylotable.coprocessor import PandasDfGroupCoprocessor, PandasDfMergeCoprocessor

_LOG = getLogger(__name__)

_TRACE = DEBUG - DEBUG // 2

class WindowPandasDfGroupCoprocessor(PandasDfGroupCoprocessor):
    """A window processing on series."""

    def __init__(self,
                 left_labels: tuple[str, str],
                 right_labels: tuple[str, str],
                 windows: dict[Hashable: tuple[timedelta, timedelta]]):
        self._left_sid_label = left_labels[0]
        self._left_data_label = left_labels[1]
        self._right_sid_label = right_labels[0]
        self._right_data_label = right_labels[1]
        self._windows = windows

    @override
    def left_sid_label(self) -> str:
        return self._left_sid_label

    @override
    def left_data_label(self) -> str:
        return self._left_data_label

    @override
    def right_sid_label(self) -> str:
        return self._right_sid_label

    @override
    def right_data_label(self) -> str:
        return self._right_data_label

    def preprocess_left(self, data: pd.DataFrame) -> pd.DataFrame:
        """Computes the time windows around each reference event."""

        _LOG.log(level=_TRACE, msg='compute observation / validation windows')
        data = super().preprocess_left(data=data)
        for w in self._windows:
            data[f'{w}_inf'] = data[self.left_data_label()] - self._windows[w][0]
            data[f'{w}_sup'] = data[self.left_data_label()] + self._windows[w][1]
        return data

    @override
    def compute_core(self, left_row: pd.Series, right_series: pd.DataFrame | pd.Series):
        """Counts the modelisation data included in each time window."""

        result = super().compute_core(left_row=left_row, right_series=right_series)

        _LOG.log(level=_TRACE, msg='compute observed / validated')

        for w in self._windows:
            result[w] = right_series.between(left_row[f'{w}_inf'], left_row[f'{w}_sup']).sum()
        return result

    @classmethod
    def from_day_window(cls,
                        left_labels: tuple[str, str],
                        right_labels: tuple[str, str],
                        windows: dict[Hashable, tuple[int, int]]):
        """Get a window evaluation defined by daily margins around reference events."""

        return cls(left_labels=left_labels,
                   right_labels=right_labels,
                   windows={
                       w: tuple(timedelta(days=t) for t in windows[w]) for w in windows
                   })


class WindowPandasDfMergeCoprocessor(PandasDfMergeCoprocessor):
    """A window processing on series."""

    def __init__(self,
                 left_labels: tuple[str, str],
                 right_labels: tuple[str, str],
                 windows: dict[Hashable: tuple[timedelta, timedelta]]):
        self._left_sid_label = left_labels[0]
        self._left_data_label = left_labels[1]
        self._right_sid_label = right_labels[0]
        self._right_data_label = right_labels[1]
        self._windows = windows

    @override
    def left_sid_label(self) -> str:
        return self._left_sid_label

    @override
    def left_data_label(self) -> str:
        return self._left_data_label

    @override
    def right_sid_label(self) -> str:
        return self._right_sid_label

    @override
    def right_data_label(self) -> str:
        return self._right_data_label

    def preprocess(self, merge: pd.DataFrame) -> pd.DataFrame:
        """Computes the time windows around each reference event."""

        _LOG.log(level=_TRACE, msg='compute o')
        for w in self._windows:
            merge[w] = ((merge[self.right_data_label()] > merge[self.left_data_label()] - self._windows[w][0])
                         & (merge[self.right_data_label()] < merge[self.left_data_label()] + self._windows[w][1]))
        return merge

    @override
    def postprocess(self, merge: pd.DataFrame):
        merge.drop(columns=[self.right_data_label()], inplace=True)
        return merge.groupby(by=[self.left_sid_label(), self.left_data_label()], as_index=False).sum()

    @classmethod
    def from_day_window(cls,
                        left_labels: tuple[str, str],
                        right_labels: tuple[str, str],
                        windows: dict[Hashable, tuple[int, int]]):
        """Get a window evaluation defined by daily margins around reference events."""

        return cls(left_labels=left_labels,
                   right_labels=right_labels,
                   windows={
                       w: tuple(timedelta(days=t) for t in windows[w]) for w in windows
                   })
