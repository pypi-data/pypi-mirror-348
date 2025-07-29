import os.path as op
import os
import logging
import tempfile

import numpy as np
from scipy.stats import sem
import pandas as pd
from tqdm.auto import tqdm

import AFQ.viz.utils as vut
from AFQ.viz.utils import display_string
from AFQ.utils.stats import contrast_index as calc_contrast_index
from AFQ.data.utils import BUNDLE_RECO_2_AFQ, BUNDLE_MAT_2_PYTHON
from AFQ.data.utils import aws_import_msg_error

try:
    from pingouin import intraclass_corr, corr
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    import IPython.display as display
except (ImportError, ModuleNotFoundError):
    raise ImportError(vut.viz_import_msg_error("plot"))

__all__ = ["visualize_tract_profiles", "visualize_gif_inline"]


def visualize_tract_profiles(tract_profiles, scalar="dti_fa", ylim=None,
                             n_boot=1000,
                             file_name=None,
                             positions=vut.POSITIONS):
    """
    Visualize all tract profiles for a scalar in one plot

    Parameters
    ----------
    tract_profiles : string
        Path to CSV containing tract_profiles.

    scalar : string, optional
       Scalar to use in plots. Default: "dti_fa".

    ylim : list of 2 floats, optional
        Minimum and maximum value used for y-axis bounds.
        If None, ylim is not set.
        Default: None

    n_boot : int, optional
        Number of bootstrap resamples for seaborn to use
        to estimate the ci.
        Default: 1000

    file_name : string, optional
        File name to save figure to if not None. Default: None

    positions : dictionary, optional
        Dictionary that maps bundle names to position in plot.
        Default: vut.POSITIONS

    Returns
    -------
        Matplotlib figure and axes.
    """
    csv_comparison = GroupCSVComparison(
        None,
        [tract_profiles],
        ["my_tract_profiles"],
        remove_model=False,
        scalar_bounds={'lb': {}, 'ub': {}})

    df = csv_comparison.tract_profiles(
        scalar=scalar,
        ylim=ylim,
        positions=positions,
        out_file=file_name,
        plot_subject_lines=False,
        n_boot=n_boot)

    return df


class BrainAxes():
    '''
    Helper class.
    Creates and handles a grid of axes.
    Each axis corresponds to a bundle.
    Axis placement should roughly correspond
    to the actual bundle placement in the brain.
    '''

    def __init__(self, size=(5, 5), positions=vut.POSITIONS, fig=None):
        self.size = size
        self.positions = positions
        self.on_grid = np.zeros((5, 5), dtype=bool)

        if fig is None:
            self.fig = plt.figure()
            label = "1"
            self.twinning = False
        else:  # we are twinning with another BrainAxes
            self.fig = fig
            label = "2"
            self.twinning = True
        self.axes = self.fig.subplots(
            self.size[0],
            self.size[1],
            subplot_kw={"label": label, "frame_on": False})
        self.fig.subplots_adjust(
            left=None,
            bottom=None,
            right=None,
            top=None,
            wspace=0.4,
            hspace=0.6)
        self.fig.set_size_inches((18, 18))
        self.temp_fig, self.temp_axis = plt.subplots()
        self.temp_axis_owner = None

    def get_axis(self, bundle, axes_dict={}):
        '''
        Given a bundle, turn on and get an axis.
        If bundle not positioned, will claim the temporary axis.
        If bundle in axes_dict, onyl return relevant axis.
        '''
        if bundle in axes_dict.keys():
            return axes_dict[bundle]
        elif bundle in self.positions.keys():
            self.on_grid[self.positions[bundle]] = True
            return self.axes[self.positions[bundle]]
        else:
            if self.temp_axis_owner != bundle:
                plt.close(self.temp_fig)
                self.temp_fig, self.temp_axis = plt.subplots()
                self.temp_axis_owner = bundle
            return self.temp_axis

    def plot_line(self, bundle, x, y, data, ylabel, ylim, n_boot, alpha,
                  lineplot_kwargs, plot_subject_lines=True, ax=None):
        '''
        Given a dataframe data with at least columns x, y,
        and subjectID, plot the mean of subjects with ci of 95
        in alpha and the individual subjects in alpha-0.2
        using sns.lineplot()
        '''
        if ax is None:
            ax = self.get_axis(bundle)
        lineplot_kwargs_mean = lineplot_kwargs.copy()
        sns.set(style="whitegrid", rc={"lines.linewidth": 1})
        ax.hlines(0, 0, 95, linestyles='dashed', color='red')
        if plot_subject_lines:
            lineplot_kwargs_mean["hue"] = None
            lineplot_kwargs_mean["palette"] = None
            lineplot_kwargs_mean["color"] = "lightgray"

            sns.set(style="whitegrid", rc={"lines.linewidth": 0.5})
            sns.lineplot(
                x=x, y=y,
                data=data,
                ci=None, estimator=None, units='subjectID',
                legend=False, ax=ax, alpha=alpha - 0.2,
                style=[True] * len(data.index), **lineplot_kwargs)

        sns.set(style="whitegrid", rc={"lines.linewidth": 3})
        sns.lineplot(
            x=x, y=y,
            data=data,
            estimator='mean',
            errorbar=('ci', 95),
            n_boot=n_boot,
            legend=False, ax=ax, alpha=alpha,
            style=[True] * len(data.index), **lineplot_kwargs_mean)

        ax.set_title(display_string(bundle), fontsize=vut.large_font)
        ax.set_ylabel(ylabel, fontsize=vut.medium_font)
        ax.set_ylim(ylim)

    def format(self, disable_x=True, disable_y=True):
        '''
        Call this functions once after all axes that you intend to use
        have been plotted on. Automatically formats brain axes.
        '''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.twinning:
                    self.axes[i, j].xaxis.tick_top()
                    self.axes[i, j].yaxis.tick_right()
                    self.axes[i, j].xaxis.set_label_position('top')
                    self.axes[i, j].yaxis.set_label_position('right')
                self.axes[i, j].tick_params(
                    axis='y', which='major', labelsize=vut.small_font)
                self.axes[i, j].tick_params(
                    axis='x', which='major', labelsize=vut.small_font)
                if not self.on_grid[i, j]:
                    self.axes[i, j].axis("off")
                if self.twinning:
                    if j != self.size[1] - 1 and self.on_grid[i][j + 1]:
                        self.axes[i, j].set_yticklabels([])
                        self.axes[i, j].set_ylabel("")
                    self.axes[i, j].set_xticklabels([])
                    self.axes[i, j].set_xlabel("")
                else:
                    if disable_y and (j != 0 and self.on_grid[i][j - 1]):
                        self.axes[i, j].set_yticklabels([])
                        self.axes[i, j].set_ylabel("")
                    if disable_x or (i != self.size[0] - 1
                                     and self.on_grid[i + 1][j]):
                        self.axes[i, j].set_xticklabels([])
                        self.axes[i, j].set_xlabel("")
        self.fig.tight_layout()

    def save_temp_fig(self, o_folder, o_file, save_func):
        '''
        If using a temporary axis, save it out and clear it.
        Returns True if temporary axis was saved, false if no
        temporary axis was in use
        '''
        if self.temp_axis_owner is None:
            return False
        self.temp_fig.tight_layout()
        save_func(self.temp_fig, o_folder, o_file)
        plt.close(self.temp_fig)
        self.temp_axis_owner = None
        return True

    def is_using_temp_axis(self):
        return (self.temp_axis_owner is not None)

    def close_all(self):
        '''
        Close all associated figures.
        '''
        plt.close(self.temp_fig)
        plt.close(self.fig)


class GroupCSVComparison():
    """
    Compare different CSVs, using:
    tract profiles, contrast indices,
    scan-rescan reliability using ICC.
    """

    def __init__(self, out_folder, csv_fnames, names, is_special="",
                 subjects=None,
                 scalar_bounds={'lb': {'FA': 0.2},
                                'ub': {'MD': 0.002}},
                 bundles=None,
                 percent_nan_tol=10,
                 percent_edges_removed=10,
                 remove_model=True,
                 mat_bundle_converter=BUNDLE_MAT_2_PYTHON,
                 mat_column_converter=vut.CSV_MAT_2_PYTHON,
                 mat_scale_converter=vut.SCALE_MAT_2_PYTHON,
                 bundle_converter=BUNDLE_RECO_2_AFQ,
                 ICC_func="ICC2"):
        """
        Load in csv files, converting from matlab if necessary.

        Parameters
        ----------
        out_folder : path
            Folder where outputs of this class's methods will be saved.

        csv_fnames : list of filenames
            Filenames for the two CSVs containing tract profiles to compare.
            Will obtain subject list from the first file.

        names : list of strings
            Name to use to identify each CSV dataset.

        is_special : str or list of strs, optional
            Whether or not the csv needs special attention.
            Can be "", "mat" if the csv was generated using mAFQ,
            or "reco" if the csv was generated using Recobundles.
            Default: ""

        subjects : list of num, optional
            List of subjects to consider.
            If None, will use all subjects in first dataset.
            Default: None

        scalar_bounds : dictionary, optional
            A dictionary with a lower bound and upper bound containting a
            series of scalar / threshold pairs used as a white-matter mask
            on the profiles (any values outside of the threshold will be
            marked NaN and not used or set to 0, depending on the case).
            Default: {'lb': {'FA': 0.2}, 'ub': {'MD': 0.002}}

        bundles : list of strings, optional
            Bundles to compare.
            If None, use all bundles in the first profile group.
            Default: None

        percent_nan_tol : int, optional
            Percentage of NaNs tolerable. If a profile has less than this
            percentage of NaNs, NaNs are interpolated. If it has more,
            the profile is thrown out.
            Default: 10

        percent_edges_removed : int, optional
            Percentage of nodes to remove from the edges of the profile.
            Scalar values often change dramatically at the boundary between
            the grey matter and the white matter, and these effects can
            dominate plots. However, they are generally not interesting to us,
            and have low intersubject reliability.
            In a profile of 100 nodes, percent_edges_removed=10 would remove
            5 nodes from each edge.
            Default: 10

        remove_model : bool, optional
            Whether to remove prefix of scalars which specify model
            i.e., dti_fa => FA.
            Default: True

        mat_bundle_converter : dictionary, optional
            Dictionary that maps matlab bundle names to python bundle names.
            Default: BUNDLE_MAT_2_PYTHON

        mat_column_converter : dictionary, optional
            Dictionary that maps matlab column names to python column names.
            Default: CSV_MAT_2_PYTHON

        mat_scale_converter : dictionary, optional
            Dictionary that maps scalar names to how they should be scaled
            to match pyAFQ's scale for that scalar.
            Default: SCALE_MAT_2_PYTHON

        bundle_converter : dictionary, optional
            Dictionary that maps bundle names to more standard bundle names.
            Unlike mat_bundle_converter, this converter is applied to all CSVs
            Default: BUNDLE_RECO_2_AFQ

        ICC_func : string, optional
            ICC function to use to calculate correlations.
            Can be 'ICC1, 'ICC2', 'ICC3', 'ICC1k', 'ICC2k', 'ICC3k'.
            Default: "ICC2"
        """
        self.logger = logging.getLogger('AFQ')
        self.ICC_func = ICC_func
        if "k" in self.ICC_func:
            self.ICC_func_name = f"ICC({self.ICC_func[3]},k)"
        else:
            self.ICC_func_name = f"ICC({self.ICC_func[3]},1)"
        self.out_folder = out_folder
        self.percent_nan_tol = percent_nan_tol

        if not isinstance(is_special, list):
            is_special = [is_special] * len(csv_fnames)

        self.profile_dict = {}
        for i, fname in enumerate(csv_fnames):
            profile = pd.read_csv(fname)
            if 'subjectID' in profile.columns:
                profile['subjectID'] = \
                    profile['subjectID'].apply(
                        lambda x: int(
                            ''.join(c for c in x if c.isdigit())
                        ) if isinstance(x, str) else x)
            else:
                profile['subjectID'] = 0

            if is_special[i] == "mat":
                profile.rename(
                    columns=mat_column_converter, inplace=True)
                profile['tractID'] = \
                    profile['tractID'].apply(
                        lambda x: mat_bundle_converter[x])
                for scalar, scale in mat_scale_converter.items():
                    profile[scalar] = \
                        profile[scalar].apply(lambda x: x * scale)
            profile.replace({"tractID": bundle_converter}, inplace=True)
            if is_special[i] == "reco":
                def reco_flip(df):
                    if df.tractID in vut.RECO_FLIP:
                        return 99 - df.nodeID
                    else:
                        return df.nodeID
                profile["nodeID"] = profile.apply(reco_flip, axis=1)
            if remove_model:
                profile.rename(
                    columns=vut.SCALAR_REMOVE_MODEL, inplace=True)

            for bound, constraint in scalar_bounds.items():
                for scalar, threshold in constraint.items():
                    profile[scalar] = \
                        profile[scalar].apply(
                            lambda x: self._threshold_scalar(
                                bound,
                                threshold,
                                x))

            if percent_edges_removed > 0:
                profile = profile.drop(profile[np.logical_or(
                    (profile["nodeID"] < percent_nan_tol // 2),
                    (profile["nodeID"] >= 100 - (percent_nan_tol // 2))
                )].index)

            self.profile_dict[names[i]] = profile
        if subjects is None:
            self.subjects = self.profile_dict[names[0]]['subjectID'].unique()
        else:
            self.subjects = subjects
        self.prof_len = 100 - (percent_nan_tol // 2) * 2
        if bundles is None:
            self.bundles = self.profile_dict[names[0]]['tractID'].unique()
            self.bundles.sort()
        else:
            self.bundles = bundles
        self.color_dict = vut.gen_color_dict([*self.bundles, "median"])

        # TODO: make these parameters
        self.scalar_markers = ["o", "x"]
        self.patterns = (
            None, '/', 'o', 'x', '-', '.',
            '+', '//', '\\', '*', 'O', '|')

    def _threshold_scalar(self, bound, threshold, val):
        """
        Threshold scalars by a lower and upper bound.
        """
        if bound == "lb":
            if val > threshold:
                return val
            else:
                return np.nan
        elif bound == "ub":
            if val < threshold:
                return val
            else:
                return np.nan
        else:
            raise RuntimeError("scalar_bounds dictionary "
                               + " formatted incorrectly. See"
                               + " the default for reference")

    def _save_fig(self, fig, folder, f_name):
        """
        Get file to save to, and generate the folder if it does not exist.
        """
        if self.out_folder is None and folder is None:
            f_folder = None
        elif self.out_folder is None:
            f_folder = folder
        elif folder is None:
            f_folder = self.out_folder
        else:
            f_folder = op.join(
                self.out_folder,
                folder)

        if f_folder is None:
            fig.savefig(f_name + ".png")
            fig.savefig(f_name + ".svg",
                        format='svg',
                        dpi=300)
        else:
            os.makedirs(f_folder, exist_ok=True)
            fig.savefig(op.join(f_folder, f_name) + ".png")
            fig.savefig(op.join(f_folder, f_name) + ".svg",
                        format='svg',
                        dpi=300)

    def _get_profile(self, name, bundle, subject, scalar):
        """
        Get a single profile, then handle not found / NaNs
        """
        profile = self.profile_dict[name]
        single_profile = profile[
            (profile['subjectID'] == subject)
            & (profile['tractID'] == bundle)
        ].sort_values("nodeID")[scalar].to_numpy()
        nans = np.isnan(single_profile)
        percent_nan = (np.sum(nans) * 100) // self.prof_len
        if len(single_profile) < 1:
            self.logger.warning(
                'No scalars found for scalar ' + scalar
                + ' for subject ' + str(subject)
                + ' for bundle ' + bundle
                + ' for CSV ' + name)
            return None

        if percent_nan > 0:
            message = (
                f'{percent_nan}% NaNs found in scalar ' + scalar
                + ' for subject ' + str(subject)
                + ' for bundle ' + bundle
                + ' for CSV ' + name)
            if np.sum(nans) > self.percent_nan_tol:
                self.logger.warning(message + '. Profile ignored. ')
                return None
            else:
                self.logger.info(message + '. NaNs interpolated. ')
                non_nan = np.logical_not(nans)
                single_profile[nans] = np.interp(
                    nans.nonzero()[0],
                    non_nan.nonzero()[0],
                    single_profile[non_nan])

        return single_profile

    def _alpha(self, alpha):
        '''
        Keep alpha in a reasonable range
        Useful when calculating alpha automatically
        '''
        if alpha < 0.3:
            return 0.3
        if alpha > 1:
            return 1
        return alpha

    def _array_to_df(self, arr):
        '''
        Converts a 2xn array to a pandas dataframe with columns x, y
        Useful for plotting with seaborn.
        '''
        df = pd.DataFrame()
        df['x'] = arr[0]
        df['y'] = arr[1]
        return df

    def masked_corr(self, arr, corrtype):
        '''
        Mask arr for NaNs before calling np.corrcoef
        '''
        mask = np.logical_not(
            np.logical_or(
                np.isnan(arr[0, ...]),
                np.isnan(arr[1, ...])))
        if np.sum(mask) < 2:
            return np.nan, np.nan, np.nan
        arr = arr[:, mask]
        if corrtype == "ICC":
            data = pd.DataFrame({
                "targets": np.concatenate(
                    (np.arange(arr.shape[1]), np.arange(arr.shape[1]))),
                "raters": np.concatenate(
                    (np.zeros(arr.shape[1]), np.ones(arr.shape[1]))),
                "ratings": np.concatenate(
                    (arr[0], arr[1]))})
            stats = intraclass_corr(
                data=data,
                targets="targets",
                raters="raters",
                ratings="ratings")
            row = stats[stats["Type"] == self.ICC_func].iloc[0]
            return row["ICC"], row["ICC"] - row["CI95%"][0], \
                row["CI95%"][1] - row["ICC"]
        elif corrtype == "Srho":
            stats = corr(
                x=arr[0],
                y=arr[1],
                method="spearman")
            row = stats.iloc[0]
            return row["r"], row["r"] - row["CI95%"][0], \
                row["CI95%"][1] - row["r"]
        else:
            raise ValueError("corrtype not recognized")

    def tract_profiles(self, names=None, scalar="FA",
                       ylim=[0.0, 1.0],
                       show_plots=False,
                       positions=vut.POSITIONS,
                       out_file=None,
                       n_boot=1000,
                       plot_subject_lines=True,
                       axes_dict={}):
        """
        Compare all tract profiles for a scalar from different CSVs.
        Plots tract profiles for all in one plot.
        Bundles taken from positions argument.

        Parameters
        ----------
        names : list of strings, optional
            Names of datasets to plot profiles of.
            If None, all datasets are used.
            Default: None

        scalar : string, optional
            Scalar to use in plots. Default: "FA".

        ylim : list of 2 floats, optional
            Minimum and maximum value used for y-axis bounds.
            If None, ylim is not set.
            Default: [0.0, 1.0]

        out_file : str, optional
            Path to save the figure to.
            If None, use the default naming convention in self.out_folder
            Default: None

        n_boot : int, optional
            Number of bootstrap resamples for seaborn to use
            to estimate the ci.
            Default: 1000

        show_plots : bool, optional
            Whether to show plots if in an interactive environment.
            Default: False

        positions : dictionary, optional
            Dictionary that maps bundle names to position in plot.
            Default: vut.POSITIONS

        plot_subject_lines : bool, optional
            Whether to plot individual subject lines with a smaller width.
            Default: True

        axes_dict : dictionary of axes, optional
            Plot contrast index for bundles that are keys of
            axes_dict on the corresponding axis. Default: {}
        """
        if not show_plots:
            plt.ioff()
        if names is None:
            names = list(self.profile_dict.keys())
        if out_file is None:
            o_folder = f"tract_profiles/{scalar}"
            o_file = f"{'_'.join(names)}"
        else:
            o_folder = None
            o_file = out_file

        ba = BrainAxes(positions=positions)
        labels = []
        self.logger.info("Calculating means and CIs...")
        for j, bundle in enumerate(tqdm(self.bundles)):
            labels_temp = []
            for i, name in enumerate(names):
                if i == 0:
                    plot_kwargs = {
                        "hue": "tractID",
                        "palette": [self.color_dict[bundle]]}
                else:
                    plot_kwargs = {
                        "dashes": [(2**(i - 1), 2**(i - 1))],
                        "hue": "tractID",
                        "palette": [self.color_dict[bundle]]}
                profile = self.profile_dict[name]
                profile = profile[profile['tractID'] == bundle]
                ba.plot_line(
                    bundle, "nodeID", scalar, profile,
                    display_string(scalar), ylim, n_boot, self._alpha(
                        0.6 + 0.2 * i),
                    plot_kwargs,
                    plot_subject_lines=plot_subject_lines,
                    ax=axes_dict.get(bundle))
                if j == 0:
                    line = Line2D(
                        [], [],
                        color=[0, 0, 0])
                    line.set_dashes((2**(i + 1), 2**(i + 1)))
                    if ba.is_using_temp_axis():
                        labels_temp.append(line)
                    else:
                        labels.append(line)
            if ba.is_using_temp_axis():
                ba.temp_fig.legend(
                    labels_temp, names, fontsize=vut.medium_font)
                if "_desc" in o_file:  # Use BIDS naming convention
                    o_file_pre = o_file.split("_desc-")[0]
                    o_file_post = o_file.split("_desc-")[1].split("_")[1]
                    bids_bname = bundle.lower().replace(
                        " ", "").replace(
                            "-", "").replace(
                                "_", "")
                    bf_name = o_file_pre + "_desc-" + bids_bname + o_file_post
                else:
                    bf_name = f"{o_file}_{bundle}"
                ba.save_temp_fig(
                    o_folder, bf_name, self._save_fig)
        if len(names) > 1:
            ba.fig.legend(
                labels, names, loc='center',
                fontsize=vut.medium_font)
        ba.format()

        self._save_fig(ba.fig, o_folder, o_file)

        if not show_plots:
            ba.close_all()
            plt.ion()

    def _contrast_index_df_maker(self, bundles, names, scalar):
        ci_df = pd.DataFrame(columns=["subjectID", "nodeID", "diff"])
        for subject in self.subjects:
            profiles = [None] * 2
            both_found = True
            for i, name in enumerate(names):
                for j, bundle in enumerate(bundles):
                    profiles[i + j] = self._get_profile(
                        name, bundle, subject, scalar)
                    if profiles[i + j] is None:
                        both_found = False
            if both_found:
                this_contrast_index = \
                    calc_contrast_index(profiles[0], profiles[1])
                for i, diff in enumerate(this_contrast_index):
                    ci_df = ci_df.append({
                        "subjectID": subject,
                        "nodeID": i,
                        "diff": diff},
                        ignore_index=True)
        return ci_df

    def contrast_index(self, names=None, scalar="FA",
                       show_plots=False, n_boot=1000,
                       ylim=(-0.5, 0.5), show_legend=False,
                       positions=vut.POSITIONS, plot_subject_lines=True,
                       axes_dict={}):
        """
        Calculate the contrast index for each bundle in two datasets.

        Parameters
        ----------
        names : list of strings, optional
            Names of datasets to plot profiles of.
            If None, all datasets are used.
            Should be a total of only two datasets.
            Default: None

        scalar : string, optional
            Scalar to use for the contrast index. Default: "FA".

        show_plots : bool, optional
            Whether to show plots if in an interactive environment.
            Default: False

        n_boot : int, optional
            Number of bootstrap resamples for seaborn to use
            to estimate the ci.
            Default: 1000

        ylim : list of 2 floats, optional
            Minimum and maximum value used for y-axis bounds.
            If None, ylim is not set.
            Default: None

        show_legend : bool, optional
            Show legend in center with single entry denoting the scalar used.
            Default: False

        positions : dictionary, optional
            Dictionary that maps bundle names to position in plot.
            Default: vut.POSITIONS

        plot_subject_lines : bool, optional
            Whether to plot individual subject lines with a smaller width.
            Default: True

        axes_dict : dictionary of axes, optional
            Plot contrast index for bundles that are keys of
            axes_dict on the corresponding axis. Default: {}
        """
        if not show_plots:
            plt.ioff()

        if names is None:
            names = list(self.profile_dict.keys())
        if len(names) != 2:
            self.logger.error("To calculate the contrast index, "
                              + "only two dataset names should be given")
            return None

        ba = BrainAxes(positions=positions)
        ci_all_df = {}
        for j, bundle in enumerate(tqdm(self.bundles)):
            ci_df = self._contrast_index_df_maker(
                [bundle], names, scalar)
            ba.plot_line(
                bundle, "nodeID", "diff", ci_df, "ACI", ylim,
                n_boot, 1.0, {"color": self.color_dict[bundle]},
                plot_subject_lines=plot_subject_lines,
                ax=axes_dict.get(bundle))
            ci_all_df[bundle] = ci_df
            ba.save_temp_fig(
                f"contrast_plots/{scalar}/",
                f"{names[0]}_vs_{names[1]}_contrast_index_{bundle}",
                self._save_fig)
        if show_legend:
            ba.fig.legend([scalar], loc='center', fontsize=vut.medium_font)
        ba.format()
        self._save_fig(
            ba.fig,
            f"contrast_plots/{scalar}/",
            f"{names[0]}_vs_{names[1]}_contrast_index")
        if not show_plots:
            ba.close_all()
            plt.ion()
        return ba.fig, ba.axes, ci_all_df

    def lateral_contrast_index(self, name, scalar="FA",
                               show_plots=False, n_boot=1000,
                               ylim=(-1, 1),
                               positions=vut.POSITIONS,
                               plot_subject_lines=True):
        """
        Calculate the lateral contrast index for each bundle in a given
        dataset, for each dataset in names.

        Parameters
        ----------
        name : string
            Names of dataset to plot profiles of.

        scalar : string, optional
            Scalar to use for the contrast index. Default: "FA".

        show_plots : bool, optional
            Whether to show plots if in an interactive environment.
            Default: False

        n_boot : int, optional
            Number of bootstrap resamples for seaborn to use
            to estimate the ci.
            Default: 1000

        ylim : list of 2 floats, optional
            Minimum and maximum value used for y-axis bounds.
            If None, ylim is not set.
            Default: None

        positions : dictionary, optional
            Dictionary that maps bundle names to position in plot.
            Default: vut.POSITIONS

        plot_subject_lines : bool, optional
            Whether to plot individual subject lines with a smaller width.
            Default: True
        """
        if not show_plots:
            plt.ioff()

        ba = BrainAxes(positions=positions)
        for j, bundle in enumerate(tqdm(self.bundles)):
            other_bundle = list(bundle)
            if other_bundle[-1] == 'L':
                other_bundle[-1] = 'R'
            elif other_bundle[-1] == 'R':
                other_bundle[-1] = 'L'
            else:
                continue
            other_bundle = "".join(other_bundle)
            if other_bundle not in self.bundles:
                continue

            ci_df = self._contrast_index_df_maker(
                [bundle, other_bundle], [name], scalar)
            ba.plot_line(
                bundle, "nodeID", "diff", ci_df, "ACI", ylim,
                n_boot, 1.0, {"color": self.color_dict[bundle]},
                plot_subject_lines=plot_subject_lines)
            ba.save_temp_fig(
                f"contrast_plots/{scalar}/",
                f"{name}_lateral_contrast_index_{bundle}",
                self._save_fig)

        ba.fig.legend([scalar], loc='center', fontsize=vut.medium_font)
        ba.format()
        self._save_fig(
            ba.fig,
            f"contrast_plots/{scalar}/",
            f"{name}_lateral_contrast_index")
        if not show_plots:
            ba.close_all()

        if not show_plots:
            plt.ion()

    def reliability_plots(self, names=None,
                          scalars=["FA", "MD"],
                          ylims=[0.0, 1.0],
                          show_plots=False,
                          only_plot_above_thr=None,
                          rotate_y_labels=False,
                          rtype="Reliability",
                          positions=vut.POSITIONS,
                          fig_axes=None,
                          prof_axes_dict={},
                          sub_axes_dict={}):
        """
        Plot the scan-rescan reliability using ICC for 2 scalars.

        Parameters
        ----------
        names : list of strings, optional
            Names of datasets to plot profiles of.
            If None, all datasets are used.
            Should be a total of only two datasets.
            Default: None

        scalars : list of strings, optional
            Scalars to correlate. Default: ["FA", "MD"].

        ylims : 2-tuple of floats, optional
            Limits of the y-axis. Useful to synchronize axes across graphs.
            Default: [0.0, 1.0].

        show_plots : bool, optional
            Whether to show plots if in an interactive environment.
            Default: False

        only_plot_above_thr : int or None, optional
            Only plot bundles with intrersubject reliability above this
            threshold on the final reliability bar plots. If None, plot all.
            Default: None

        rotate_y_labels : bool, optional
            Rotate y labels on final reliability plots.
            Default: False

        rtype : str, optional
            Type of reliability to name the y axis of the reliability bar
            charts. Default: "Reliability"

        positions : dictionary, optional
            Dictionary that maps bundle names to position in plot.
            Default: vut.POSITIONS

        fig_axes : tuple of matplotlib figure and axes, optional
            If not None, the resulting reliability plots will use this
            figure and axes. Default: None

        prof_axes_dict : dictionary of axes, optional
            Plot profile reliability histograms for bundles that
            are keys of prof_axes_dict on the corresponding axis.
            Default: {}

        sub_axes_dict : dictionary of axes, optional
            Plot subject reliability scatter plots for bundles that
            are keys of sub_axes_dict on the corresponding axis.
            Default: {}

        Returns
        -------
        Returns 8 objects:
        1. Matplotlib figure
        2. Matplotlib axes
        3. A dictionary containing the number of missing bundles
           for each dataset.
        4. A list of bundles with sufficient correlation
        5. A pandas dataframe describing the intersubject reliabilities,
           per bundle
        6. A numpy array describing the intersubject reliability errors,
           per bundle
        7. A pandas dataframe desribing the profile reliabilities,
           per bundle
        8. A numpy array desribing the profile reliability errors,
           per bundle
        """
        if not show_plots:
            plt.ioff()
        if names is None:
            names = list(self.profile_dict.keys())
        if len(names) != 2:
            self.logger.error("To plot correlations, "
                              + "only two dataset names should be given")
            return None

        # extract relevant statistics / data from profiles
        N = len(self.subjects)
        all_sub_coef = np.zeros((len(scalars), len(self.bundles)))
        all_sub_coef_err = np.zeros((len(scalars), len(self.bundles), 2))
        all_sub_means = np.zeros(
            (len(scalars), len(self.bundles), 2, N))
        all_profile_coef = \
            np.zeros((len(scalars), len(self.bundles), N))
        all_node_coef = np.zeros(
            (len(scalars), len(self.bundles), self.prof_len))
        miss_counts = pd.DataFrame(0, index=self.bundles, columns=[
            f"miss_count{names[0]}", f"miss_count{names[1]}"])
        for m, scalar in enumerate(scalars):
            for k, bundle in enumerate(tqdm(self.bundles)):
                bundle_profiles =\
                    np.zeros((2, N, self.prof_len))
                for j, name in enumerate(names):
                    for i, subject in enumerate(self.subjects):
                        single_profile = self._get_profile(
                            name, bundle, subject, scalar)
                        if single_profile is None:
                            bundle_profiles[j, i] = np.nan
                            miss_counts.at[bundle, f"miss_count{name}"] =\
                                miss_counts.at[
                                    bundle, f"miss_count{name}"] + 1
                        else:
                            bundle_profiles[j, i] = single_profile

                all_sub_means[m, k] = np.nanmean(bundle_profiles, axis=2)
                all_sub_coef[m, k], all_sub_coef_err[m, k, 0], \
                    all_sub_coef_err[m, k, 1] =\
                    self.masked_corr(all_sub_means[m, k], "Srho")
                if np.isnan(all_sub_coef[m, k]).all():
                    self.logger.error((
                        f"Not enough non-nan profiles"
                        f"for scalar {scalar} for bundle {bundle}"))
                    all_sub_coef[m, k] = 0

                bundle_coefs = np.zeros(N)
                for i in range(N):
                    bundle_coefs[i], _, _ = \
                        self.masked_corr(bundle_profiles[:, i, :], "ICC")
                all_profile_coef[m, k] = bundle_coefs

                node_coefs = np.zeros(self.prof_len)
                for i in range(self.prof_len):
                    node_coefs[i], _, _ =\
                        self.masked_corr(bundle_profiles[:, :, i], "ICC")
                all_node_coef[m, k] = node_coefs

        # plot histograms of subject ICC
        maxi = np.nanmax(all_profile_coef)
        mini = np.nanmin(all_profile_coef)
        bins = np.linspace(mini, maxi, 10)
        ba = BrainAxes(positions=positions)
        for k, bundle in enumerate(self.bundles):
            ax = ba.get_axis(bundle, axes_dict=prof_axes_dict)
            for m, scalar in enumerate(scalars):
                bundle_coefs = all_profile_coef[m, k]
                bundle_coefs = bundle_coefs[~np.isnan(bundle_coefs)]
                sns.set(style="whitegrid")
                sns.histplot(
                    data=bundle_coefs,
                    bins=bins,
                    alpha=0.5,
                    color=self.color_dict[bundle],
                    hatch=self.patterns[m],
                    label=scalar,
                    ax=ax)
            ax.set_title(display_string(bundle), fontsize=vut.large_font)
            ax.set_xlabel(self.ICC_func_name, fontsize=vut.medium_font)
            ax.set_ylabel("Subject count", fontsize=vut.medium_font)
            ba.temp_fig.legend(
                display_string(scalars),
                fontsize=vut.medium_font)
            ba.save_temp_fig(
                f"rel_plots/{'_'.join(scalars)}/verbose",
                (f"{names[0]}_vs_{names[1]}_profile_r_distributions"
                 f"_{bundle}"),
                self._save_fig)

        legend_labels = []
        for m, _ in enumerate(scalars):
            legend_labels.append(Patch(
                facecolor='k',
                hatch=self.patterns[m]))
        ba.fig.legend(
            legend_labels, display_string(scalars),
            loc='center', fontsize=vut.medium_font)
        ba.format(disable_x=False)
        self._save_fig(
            ba.fig,
            f"rel_plots/{'_'.join(scalars)}/verbose",
            f"{names[0]}_vs_{names[1]}_profile_r_distributions")

        if not show_plots:
            ba.close_all()

        # plot node reliability profile
        all_node_coef[np.isnan(all_node_coef)] = 0
        if ylims is None:
            maxi = all_node_coef.max()
            mini = all_node_coef.min()
        else:
            maxi = ylims[1]
            mini = ylims[0]
        ba = BrainAxes(positions=positions)
        for k, bundle in enumerate(self.bundles):
            ax = ba.get_axis(bundle)
            for m, scalar in enumerate(scalars):
                sns.set(style="whitegrid")
                sns.lineplot(
                    data=all_node_coef[m, k],
                    label=scalar,
                    color=vut.tableau_20[m * 2],
                    ax=ax,
                    legend=False,
                    ci=None, estimator=None)
            ax.set_ylim([mini, maxi])
            ax.set_title(display_string(bundle), fontsize=vut.large_font)
            ax.set_ylabel(self.ICC_func_name, fontsize=vut.medium_font)
            ba.temp_fig.legend(
                display_string(scalars),
                fontsize=vut.medium_font)
            ba.save_temp_fig(
                f"rel_plots/{'_'.join(scalars)}/verbose",
                (f"{names[0]}_vs_{names[1]}_node_profiles"
                    f"_{bundle}"),
                self._save_fig)

        ba.fig.legend(display_string(scalars),
                      loc='center', fontsize=vut.medium_font)
        ba.format()
        self._save_fig(
            ba.fig,
            f"rel_plots/{'_'.join(scalars)}/verbose",
            f"{names[0]}_vs_{names[1]}_node_profiles")

        if not show_plots:
            ba.close_all()

        # plot mean profile scatter plots
        for m, scalar in enumerate(scalars):
            maxi = np.nanmax(all_sub_means[m])
            mini = np.nanmin(all_sub_means[m])
            if len(scalars) == 2:
                twinning_next = (m == 0)
                twinning = (m == 1)
            else:
                twinning = False
                twinning_next = False
            if twinning:
                ba = BrainAxes(positions=positions, fig=ba.fig)
            else:
                ba = BrainAxes(positions=positions)
            for k, bundle in enumerate(self.bundles):
                if twinning:
                    fc = 'w'
                    ec = self.color_dict[bundle]
                else:
                    fc = self.color_dict[bundle]
                    ec = 'w'
                ax = ba.get_axis(bundle, axes_dict=sub_axes_dict)
                sns.set(style="whitegrid")
                if not twinning:
                    ax.plot(
                        [[0, 0], [1, 1]], [[0, 0], [1, 1]],
                        '--', color='red')
                ax.scatter(
                    all_sub_means[m, k, 0],
                    all_sub_means[m, k, 1],
                    label=scalar,
                    marker=self.scalar_markers[m - twinning],
                    facecolors=fc,
                    edgecolors=ec,
                    s=vut.marker_size,
                    linewidth=1)
                if twinning or twinning_next:
                    twinning_color = 'k'
                    if twinning_next:
                        ax.spines['bottom'].set_color(twinning_color)
                        ax.spines['left'].set_color(twinning_color)
                    else:
                        ax.spines['top'].set_color(twinning_color)
                        ax.spines['right'].set_color(twinning_color)
                    ax.xaxis.label.set_color(twinning_color)
                    ax.tick_params(axis='x', colors=twinning_color)
                    ax.xaxis.label.set_color(twinning_color)
                    ax.yaxis.label.set_color(twinning_color)
                    ax.tick_params(axis='y', colors=twinning_color)
                    ax.yaxis.label.set_color(twinning_color)
                if not twinning:
                    ax.set_title(
                        display_string(bundle),
                        fontsize=vut.large_font)
                ax.set_xlabel(names[0], fontsize=vut.medium_font)
                ax.set_ylabel(names[1], fontsize=vut.medium_font)
                ax.set_ylim([mini, maxi])
                ax.set_xlim([mini, maxi])
                ba.temp_fig.legend(
                    [scalar], fontsize=vut.medium_font)
                ba.save_temp_fig(
                    f"rel_plots/{'_'.join(scalars)}/verbose",
                    (f"{names[0]}_vs_{names[1]}_{scalar}_mean_profiles"
                        f"_{bundle}"),
                    self._save_fig)
            if twinning:
                legend_labels = [
                    Line2D(
                        [], [],
                        markerfacecolor='k',
                        markeredgecolor='w',
                        marker=self.scalar_markers[0],
                        linewidth=0,
                        markersize=15),
                    Line2D(
                        [], [],
                        markeredgecolor='k',
                        markerfacecolor='w',
                        marker=self.scalar_markers[0],
                        linewidth=0,
                        markersize=15)]
                ba.fig.legend(
                    legend_labels,
                    display_string(scalars),
                    loc='center',
                    fontsize=vut.medium_font)
            elif not twinning_next:
                ba.fig.legend([scalar], loc='center', fontsize=vut.medium_font)
                self._save_fig(
                    ba.fig,
                    f"rel_plots/{'_'.join(scalars)}/verbose",
                    f"{names[0]}_vs_{names[1]}_{scalar}_mean_profiles")
            ba.format(disable_x=False)
            if not (show_plots or twinning_next):
                ba.close_all()

        # plot bar plots of ICC
        if fig_axes is None:
            fig, axes = plt.subplots(2, 1)
            fig.set_size_inches((8, 8))
        else:
            fig = fig_axes[0]
            axes = fig_axes[1]
        bundle_prof_means = np.nanmean(all_profile_coef, axis=2)
        bundle_prof_stds = 1.95 * \
            sem(all_profile_coef, axis=2, nan_policy='omit')
        if ylims is None:
            maxi = np.maximum(bundle_prof_means.max(), all_sub_coef.max())
            mini = np.minimum(bundle_prof_means.min(), all_sub_coef.min())
        else:
            maxi = ylims[1]
            mini = ylims[0]

        if only_plot_above_thr is not None:
            is_removed_bundle =\
                np.logical_not(
                    np.logical_and(
                        np.all(all_sub_coef > only_plot_above_thr, axis=0),
                        np.all(bundle_prof_means > only_plot_above_thr,
                               axis=0)))
            removal_idx = np.where(is_removed_bundle)[0]
            bundle_prof_means_removed = np.delete(
                bundle_prof_means,
                removal_idx,
                axis=1)
            bundle_prof_stds_removed = np.delete(
                bundle_prof_stds,
                removal_idx,
                axis=1)
            all_sub_coef_removed = np.delete(
                all_sub_coef,
                removal_idx,
                axis=1)
            all_sub_coef_err_removed = np.delete(
                all_sub_coef_err,
                removal_idx,
                axis=1)
        else:
            is_removed_bundle = [False] * len(self.bundles)
            bundle_prof_means_removed = bundle_prof_means
            bundle_prof_stds_removed = bundle_prof_stds
            all_sub_coef_err_removed = all_sub_coef_err
            all_sub_coef_removed = all_sub_coef

        updated_bundles = []
        for k, bundle in enumerate(self.bundles):
            if not is_removed_bundle[k]:
                if bundle == "CC_ForcepsMinor":
                    updated_bundles.append("CC_FMi")
                else:
                    updated_bundles.append(bundle)
        updated_bundles.append("median")

        sns.set(style="whitegrid")
        width = 0.6
        spacing = 1.5
        x = np.arange(len(updated_bundles)) * spacing
        x_shift = np.linspace(-0.5 * width, 0.5 * width, num=len(scalars))

        bundle_prof_means_removed = np.pad(
            bundle_prof_means_removed, [(0, 0), (0, 1)])
        bundle_prof_stds_removed = np.pad(
            bundle_prof_stds_removed, [(0, 0), (0, 1)])
        all_sub_coef_removed = np.pad(
            all_sub_coef_removed, [(0, 0), (0, 1)])
        all_sub_coef_err_removed = np.transpose(np.pad(
            all_sub_coef_err_removed, [(0, 0), (0, 1), (0, 0)]))

        for m, scalar in enumerate(scalars):
            bundle_prof_means_removed[m, -1] = np.median(
                bundle_prof_means_removed[m, :-1])
            all_sub_coef_removed[m, -1] = np.median(
                all_sub_coef_removed[m, :-1])

            # This code can be used as a baseline to make violin plots
            #
            # mask = ~np.isnan(all_profile_coef[m].T)
            # all_profile_coef_m_removed =\
            #     [d[k] for d, k in zip(all_profile_coef[m], mask.T)]
            # vl_parts = axes[0].violinplot(
            #     all_profile_coef_m_removed,
            #     positions=x[:-1] + x_shift[m],
            #     showmedians=True
            #     )
            # color_list = list(self.color_dict.values())
            # for c, pc in enumerate(vl_parts['bodies']):
            #     pc.set_facecolor(color_list[c])
            #     pc.set_edgecolor(color_list[c])
            #     pc.set_alpha(1)
            #     pc.set_hatch(self.patterns[m])
            # vl_parts['cbars'].set_color(color_list)

            axes[0].bar(
                x + x_shift[m],
                bundle_prof_means_removed[m],
                width,
                label=scalar,
                yerr=bundle_prof_stds_removed[m],
                hatch=self.patterns[m],
                color=self.color_dict.values())
            axes[1].bar(
                x + x_shift[m],
                all_sub_coef_removed[m],
                width,
                label=scalar,
                yerr=all_sub_coef_err_removed[:, :, m],
                hatch=self.patterns[m],
                color=self.color_dict.values())

        if len(updated_bundles) > 20:
            xaxis_font_size = vut.small_font - 6
        else:
            xaxis_font_size = vut.small_font

        axes[0].set_title("A", fontsize=vut.large_font)
        axes[0].set_ylabel(f'Profile {rtype}',
                           fontsize=vut.medium_font)
        axes[0].set_ylim([mini, maxi])
        axes[0].set_xlabel("")
        axes[0].set_yticklabels(
            [0, 0.2, 0.4, 0.6, 0.8, 1.0],
            fontsize=vut.small_font - 8)
        axes[0].set_xticks(x + 0.5)
        axes[0].set_xticklabels(
            display_string(updated_bundles), fontsize=xaxis_font_size)
        axes[1].set_title("B", fontsize=vut.large_font)
        axes[1].set_ylabel(f'Subject {rtype}',
                           fontsize=vut.medium_font)
        axes[1].set_ylim([mini, maxi])
        axes[1].set_xlabel("")
        axes[1].set_yticklabels(
            [0, 0.2, 0.4, 0.6, 0.8, 1.0],
            fontsize=vut.small_font - 8)
        axes[1].set_xticks(x + 0.5)
        axes[1].set_xticklabels(
            display_string(updated_bundles), fontsize=xaxis_font_size)

        plt.setp(axes[0].get_xticklabels(),
                 rotation=65,
                 horizontalalignment='right')
        plt.setp(axes[1].get_xticklabels(),
                 rotation=65,
                 horizontalalignment='right')

        if rotate_y_labels:
            plt.setp(axes[0].get_yticklabels(),
                     rotation=90)
            plt.setp(axes[1].get_yticklabels(),
                     rotation=90)

        fig.tight_layout()
        legend_labels = []
        for m, _ in enumerate(scalars):
            legend_labels.append(Patch(
                facecolor='k',
                hatch=self.patterns[m]))
        fig.legend(
            legend_labels,
            display_string(scalars),
            fontsize=vut.small_font,
            bbox_to_anchor=(1.25, 0.5))
        self._save_fig(
            fig,
            f"rel_plots/{'_'.join(scalars)}",
            f"{names[0]}_vs_{names[1]}")

        if not show_plots:
            plt.close(fig)
            plt.ion()
        return fig, axes, miss_counts, updated_bundles, \
            all_sub_coef_removed, all_sub_coef_err_removed, \
            bundle_prof_means_removed, bundle_prof_stds_removed

    def compare_reliability(self, reliability1, reliability2,
                            analysis_label1, analysis_label2,
                            bundles,
                            errors1=None, errors2=None,
                            scalars=["FA", "MD"],
                            rtype="Subject Reliability",
                            show_plots=False,
                            show_legend=True,
                            fig_ax=None):
        """
        Plot a comparison of scan-rescan reliability between two analyses.

        Parameters
        ----------
        reliability1, reliability2 : numpy arrays
            numpy arrays of reliabilities.
            Typically, each of this will be outputs of separate calls
            to reliability_plots.

        analysis_label1, analysis_label2 : Strings
            Names of the analyses used to obtain each dataset.
            Used to label the x and y axes.

        bundles : list of str
            List of bundles that correspond to the second dimension of the
            reliability arrays.

        errors1, errors2 : numpy arrays or None
            Numpy arrays describing the errors.
            Typically, each of this will be outputs of separate calls
            to reliability_plots.
            If None, errors are not shown.
            Default is None.

        scalars : list of str, optional
            Lsit of scalars that correspond to the first dimension of the
            reliability arrays. Default: ["FA", "MD"]

        rtype : str
            type of reliability. Can be any string; used in x axis lavel.
            Default: Subject Reliability

        show_plots : bool, optional
            Whether to show plots if in an interactive environment.
            Default: False

        show_legend : bool, optional
            Show legend for the plot, off to the right hand side.
            Default: True

        fig_ax : tuple of matplotlib figure and axis, optional
            If not None, the resulting reliability plots will use this
            figure and axis. Default: None

        Returns
        -------
        Returns a Matplotlib figure and axes.
        """
        show_error = ((errors1 is not None) and (errors2 is not None))
        if fig_ax is None:
            fig, ax = plt.subplots()
        else:
            fig = fig_ax[0]
            ax = fig_ax[1]
        legend_labels = []
        for i, scalar in enumerate(scalars):
            marker = self.scalar_markers[i]
            if marker == "x":
                marker = marker.upper()
            for j, bundle in enumerate(bundles):
                ax.scatter(
                    reliability1[i, j],
                    reliability2[i, j],
                    s=vut.marker_size,
                    c=[self.color_dict[bundle]],
                    marker=marker
                )
                if show_error:
                    if len(errors1.shape) > 2:
                        xerr = errors1[:, j, i].reshape((2, 1))
                    else:
                        xerr = errors1[i, j]
                    if len(errors2.shape) > 2:
                        yerr = errors2[:, j, i].reshape((2, 1))
                    else:
                        yerr = errors2[i, j]

                    ax.errorbar(
                        reliability1[i, j],
                        reliability2[i, j],
                        xerr=xerr,
                        yerr=yerr,
                        c=[self.color_dict[bundle]],
                        alpha=0.5,
                        fmt="none"
                    )
                if i == 0:
                    legend_labels.append(Patch(
                        facecolor=self.color_dict[bundle],
                        label=bundle))
            legend_labels.append(Line2D(
                [0], [0],
                marker=marker,
                color='k',
                lw=0,
                markersize=10,
                label=scalar))

        ax.set_xlabel(f"{analysis_label1} {rtype}",
                      fontsize=vut.medium_font)
        ax.set_ylabel(f"{analysis_label2} {rtype}",
                      fontsize=vut.medium_font)
        ax.tick_params(
            axis='x', which='major', labelsize=vut.medium_font)
        ax.tick_params(
            axis='y', which='major', labelsize=vut.medium_font)
        ax.set_ylim(0.2, 1)
        ax.set_xlim(0.2, 1)
        ax.plot([[0, 0], [1, 1]], [[0, 0], [1, 1]], '--', color='red')
        legend_labels.append(Line2D(
            [0], [0], linewidth=3, linestyle='--', color='red', label='X=Y'))
        if show_legend:
            fig.legend(
                handles=legend_labels,
                fontsize=vut.small_font - 6,
                bbox_to_anchor=(1.5, 2.0))
            fig.tight_layout()
        return fig, ax


def visualize_gif_inline(fname, use_s3fs=False):
    """Display a gif inline, possible from s3fs """
    if use_s3fs:
        try:
            import s3fs
        except (ImportError, ModuleNotFoundError):
            aws_import_msg_error("s3fs")
        fs = s3fs.S3FileSystem()
        tdir = tempfile.gettempdir()
        fname_remote = fname
        fname = op.join(tdir, "fig.gif")
        fs.get(fname_remote, fname)

    display.display(display.Image(fname))


def show_anatomical_slices(img_data, title):
    """
    display anatomical slices from midpoint

    based on:
    https://nipy.org/nibabel/coordinate_systems.html
    """

    axial_slice = img_data[:, :, int(img_data.shape[2] / 2)]
    coronal_slice = img_data[:, int(img_data.shape[1] / 2), :]
    sagittal_slice = img_data[int(img_data.shape[0] / 2), :, :]

    fig = plt.figure(constrained_layout=False)
    gs = fig.add_gridspec(nrows=3, ncols=2, wspace=0.01, hspace=0.01)
    ax1 = fig.add_subplot(gs[:-1, :])
    ax1.imshow(axial_slice.T, cmap="gray", origin="lower")
    ax1.axis('off')
    ax2 = fig.add_subplot(gs[2, 0])
    ax2.imshow(coronal_slice.T, cmap="gray", origin="lower")
    ax2.axis('off')
    ax3 = fig.add_subplot(gs[2, 1])
    ax3.imshow(sagittal_slice.T, cmap="gray", origin="lower")
    ax3.axis('off')

    plt.suptitle(title)
    plt.show()
