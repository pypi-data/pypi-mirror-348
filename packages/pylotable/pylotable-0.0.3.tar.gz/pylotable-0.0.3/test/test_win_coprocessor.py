"""WindowTSCoprocessor tests"""

import pandas as pd

from pylotable.win_coprocessor import WindowPandasDfGroupCoprocessor, WindowPandasDfMergeCoprocessor


def test_reference_fixture(ref_pd_df):
    """Tests the reference fixture"""

    exp_ref = pd.DataFrame()
    exp_ref['tsid'] = pd.Series(data=[0, 2, 1, 1, 1, 2])
    exp_ref['date'] = pd.Series(data=[pd.to_datetime(e) for e in [
        '2015-01-03 16:15:38',
        '2015-01-24 05:14:54',
        '2015-01-20 15:17:29',
        '2015-01-14 03:59:32',
        '2015-01-13 23:46:15',
        '2015-01-26 18:11:25']])
    pd.testing.assert_frame_equal(ref_pd_df, exp_ref)


def test_modelisation_fixture(model_pd_df):
    """Tests the modelisation fixture"""

    exp_model = pd.DataFrame()
    exp_model['tsid'] = pd.Series(data=[1, 1, 2, 2, 0, 0])
    exp_model['date'] = pd.Series(data=[pd.to_datetime(e) for e in [
        '2015-01-15 04:41:45',
        '2015-01-16 08:30:41',
        '2015-01-23 15:43:14',
        '2015-01-29 12:20:01',
        '2015-01-02 01:05:37',
        '2015-01-05 07:47:41']])
    pd.testing.assert_frame_equal(model_pd_df, exp_model)


def test_win_group_coprocessor(ref_pd_df: pd.DataFrame, model_pd_df: pd.DataFrame):
    """Tests the default window counts are correctly computed."""

    coprocessor = WindowPandasDfGroupCoprocessor.from_day_window(left_labels=('tsid', 'date'),
                                                                 right_labels=('tsid', 'date'),
                                                                 windows={
                                                                     'w_10_10': (10, 10),
                                                                     'w_1_5': (1, 5),
                                                                 })

    evaluation = (coprocessor.compute(left=ref_pd_df, right=model_pd_df)
                  .sort_values(by=[coprocessor.left_sid_label(), coprocessor.left_data_label()],
                               axis=0,
                               ascending=True))

    # sort date
    exp_eval = pd.DataFrame(index=[0, 4, 3, 2, 1, 5], data={
        'tsid': [0, 1, 1, 1, 2, 2],
        'date': [pd.to_datetime(e) for e in [
            '2015-01-03 16:15:38',
            '2015-01-13 23:46:15',
            '2015-01-14 03:59:32',
            '2015-01-20 15:17:29',
            '2015-01-24 05:14:54',
            '2015-01-26 18:11:25']],
        'w_10_10': [2, 2, 2, 2, 2, 2],
        'w_1_5': [1, 2, 2, 0, 1, 1]
    })

    pd.testing.assert_frame_equal(evaluation, exp_eval)


def test_win_merge_coprocessor(ref_pd_df: pd.DataFrame, model_pd_df: pd.DataFrame):
    """Tests the default window counts are correctly computed."""

    ref_pd_df = ref_pd_df.rename(columns={'date': 'date_ref'}, inplace=False)
    model_pd_df = model_pd_df.rename(columns={'date': 'date_mod'}, inplace=False)

    coprocessor = WindowPandasDfMergeCoprocessor.from_day_window(left_labels=('tsid', 'date_ref'),
                                                                 right_labels=('tsid', 'date_mod'),
                                                                 windows={
                                                                     'w_10_10': (10, 10),
                                                                     'w_1_5': (1, 5),
                                                                 })

    evaluation = coprocessor.compute(left=ref_pd_df, right=model_pd_df)

    # index is
    exp_eval = pd.DataFrame(index=[0, 1, 2, 3, 4, 5], data={
        'tsid': [0, 1, 1, 1, 2, 2],
        'date_ref': [pd.to_datetime(e) for e in [
            '2015-01-03 16:15:38',
            '2015-01-13 23:46:15',
            '2015-01-14 03:59:32',
            '2015-01-20 15:17:29',
            '2015-01-24 05:14:54',
            '2015-01-26 18:11:25']],
        'w_10_10': [2, 2, 2, 2, 2, 2],
        'w_1_5': [1, 2, 2, 0, 1, 1]
    })

    pd.testing.assert_frame_equal(evaluation, exp_eval)
