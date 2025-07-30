"""A time series comparison/evaluation processing."""

from logging import getLogger

import pandas as pd

_LOG = getLogger(__name__)



class PandasDfGroupCoprocessor:
    """Co-processes two series collections here called "right" and "left"."""

    def left_sid_label(self) -> str:
        """The series id label of the left collection."""

    def left_data_label(self) -> str:
        """The data column label of the left collection."""

    def right_sid_label(self) -> str:
        """The series id label of the right collection."""

    def right_data_label(self) -> str:
        """The data column label of the right collection."""

    def preprocess_left(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the left data collection.

        Args:
            data (pd.DataFrame): the left data.

        Returns (pd.Series): the left data.
        """
        return data

    def preprocess_right(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the right data collection.

        Args:
            data (pd.DataFrame): the right data.

        Returns (pd.Series): the right data.
        """

        return data

    def preprocess_right_series(self, data: pd.DataFrame) -> pd.DataFrame | pd.Series:
        """The core process loops over each left data and processes it to the corresponding right data.

        Before each of these processing loops, the right data relative to the series id is isolated so to
        avoid useless comparisons between unrelated left series.

        Then, this right data subset is preprocessed in order to manipulate the lightest possible data.

        This last right subset preprocessing is the purpose of the current method.

        By default, it only returns the data series of the right subset corresponding to the current series to process.

        Args:
            data (pd.DataFrame): the right data subset of the currently processed series.

        Returns (pd.DataFrame | pd.Series): the right series useful for the core processing.
        """
        return data[self.right_data_label()]


    def compute_core(self, left_row: pd.Series, right_series: pd.DataFrame | pd.Series):
        """The elementary processing of a given series. For consistency purpose, inside this method, both left and
        right data must be related to the same series id, even if this information is not always used by the processing.

        Args:
            left_row (pd.Series): a series of the left data related to a single row
            right_series (pd.DataFrame | pd.Series): a subset of the right data related to the same
            series id of the left data row

        Returns: the method result is applied to each row of the left data subset related to a given series id,
        with the same right data series given in argument. Please refer to the
        pd.DataFrame.apply() method to adjust the current method return type to custom usages. The default behavior
        returns a dict in order to produce a dataframe whose column labels are the dict keys and the column values the
        successive associated dict values. The default dict maps the series id to its label in the left data
        and the left data value to the left data label.
        """
        return {
            self.left_sid_label(): left_row[self.right_sid_label()],
            self.left_data_label(): left_row[self.left_data_label()]
        }

    def compute(self, left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        """The global core processing.

        Only override it with caution. Prefers to override each data preprocessing steps.

        Preprocesses the left and right data. Then, loops over left series and applies the elementary core process to
        each of its rows.

        Args:
            left (pd.DataFrame): the left data collection; be careful to make a defensive copy before passing it as
            an argument or when overriding the preprocessing stage if no modification is wanted on the raw dataframe
            right (pd.DataFrame): the right data collection; be careful to make a defensive copy before passing it as
            an argument or when overriding the preprocessing stage if no modification is wanted on the raw dataframe

        Returns (list[pd.DataFrame]): the data computation for the whole series collections.
        """
        _LOG.debug("preprocess left data")
        left = self.preprocess_left(data=left)

        _LOG.debug("preprocess right data")
        right = self.preprocess_right(data=right)

        _LOG.debug("process group analysis")
        l = []
        for sid, left_series in left.groupby(self.left_sid_label()):

            right_data = self.preprocess_right_series(data=right[right[self.right_sid_label()] == sid])

            l.append(left_series.apply(self.compute_core,
                                        axis=1,
                                        result_type='expand',
                                        right_series=right_data))
        _LOG.debug("end of processing")
        return pd.concat(l)


class PandasDfMergeCoprocessor:
    """Co-processes two series collections here called "right" and "left"."""

    def left_sid_label(self) -> str:
        """The series id label of the left collection."""

    def left_data_label(self) -> str:
        """The data column label of the left collection."""

    def right_sid_label(self) -> str:
        """The series id label of the right collection."""

    def right_data_label(self) -> str:
        """The data column label of the right collection."""

    def preprocess_left(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the left data collection.

        Args:
            data (pd.DataFrame): the left data.

        Returns (pd.Series): the left data.
        """
        return data

    def preprocess_right(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the right data collection.

        Args:
            data (pd.DataFrame): the right data.

        Returns (pd.Series): the right data.
        """

        return data

    def merge(self, left: pd.DataFrame, right: pd.DataFrame):
        """Merges left and right series collections."""
        return pd.merge(left=left,
                        right=right,
                        how='inner',
                        left_on=[self.left_sid_label()],
                        right_on=[self.right_sid_label()],
                        validate='many_to_many')

    def preprocess(self, merge: pd.DataFrame):
        """Preprocesses the merged data before the core process applied by series."""
        return merge

    def compute_core(self, merge_series: pd.DataFrame) -> pd.DataFrame:
        """The default core processing for an individual serries."""
        return merge_series

    def process(self, merge: pd.DataFrame) -> pd.DataFrame:
        """The default core processing series by series.

        Args:
            merge (pd.DataFrame): a series of the left data inner joined to the right data for a given series.
        """
        l = []
        for _, merge_series in merge.groupby(self.left_sid_label()):
            l.append(self.compute_core(merge_series=merge_series))

        return pd.concat(l)

    def postprocess(self, merge: pd.DataFrame):
        """Postprocesses the concatenated processed data."""
        return merge

    def compute(self, left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        """The global core processing.

        Only override it with caution. Prefers to override each data preparation and preprocessing steps.

        Prepares and preprocesses the reference and modelisation data. Then, loops over reference timeseries and applies
        the elementary core process to each of its rows.

        Args:
            left (pd.DataFrame): the reference data ; be careful to make a defensive copy before passing it as
            an argument or when overriding the preparation stage if no modification is wanted on the raw dataframe
            right (pd.DataFrame): the modelisation data ; be careful to make a defensive copy before passing
            it as an argument or when overriding the preparation stage if no modification is wanted on the raw dataframe

        Returns (list[pd.DataFrame]): a list of resulting data computations for each timeseries.
        """
        _LOG.debug("preprocess left data")
        left = self.preprocess_left(data=left)

        _LOG.debug("preprocess right data")
        right = self.preprocess_right(data=right)

        _LOG.debug("merge data")
        m = self.merge(left=left, right=right)

        _LOG.debug("preprocess data")
        m = self.preprocess(m)

        _LOG.debug("process group analysis")
        m = self.process(m)

        _LOG.debug("end of processing")
        return self.postprocess(merge=m)
