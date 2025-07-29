import numpy as np

from tqdm import tqdm
import scipy.io

from dipy.io.stateful_tractogram import StatefulTractogram, Space
import nibabel as nib

from AFQ.data.utils import BUNDLE_MAT_2_PYTHON


# This dictionary is used to convert the names of the bundles
# from old pyAFQ bundle names to the new pyAFQ bundle names.
old_acronyms_to_formal = {
    "ATR_L": "Left Anterior Thalamic",
    "ATR_R": "Right Anterior Thalamic",
    "CST_L": "Left Corticospinal",
    "CST_R": "Right Corticospinal",
    "CGC_L": "Left Cingulum Cingulate",
    "CGC_R": "Right Cingulum Cingulate",
    "IFO_L": "Left Inferior Fronto-occipital",
    "IFO_R": "Right Inferior Fronto-occipital",
    "ILF_L": "Left Inferior Longitudinal",
    "ILF_R": "Right Inferior Longitudinal",
    "SLF_L": "Left Superior Longitudinal",
    "SLF_R": "Right Superior Longitudinal",
    "UNC_L": "Left Uncinate",
    "UNC_R": "Right Uncinate",
    "ARC_L": "Left Arcuate",
    "ARC_R": "Right Arcuate",
    "VOF_L": "Left Vertical Occipital",
    "VOF_R": "Right Vertical Occipital",
    "pARC_L": "Left Posterior Arcuate",
    "pARC_R": "Right Posterior Arcuate",
    "Orbital": "Callosum Orbital",
    "AntFrontal": "Callosum Anterior Frontal",
    "SupFrontal": "Callosum Superior Frontal",
    "Motor": "Callosum Motor",
    "SupParietal": "Callosum Superior Parietal",
    "PostParietal": "Callosum Posterior Parietal",
    "Occipital": "Callosum Occipital",
    "Temporal": "Callosum Temporal"
}


class MatlabFileTracking():
    """
    Helper class.
    Acts the same as a tracking class from DIPY,
    in that it yields a streamline for each call to __iter__.
    Initialized with an opened h5py matlab file
    and the location of the streamlines in that h5py file.
    """

    def __init__(self, fg_ref):
        self.fg_ref = fg_ref

    def __iter__(self):
        for i in tqdm(range(self.fg_ref.shape[0])):
            yield np.transpose(self.fg_ref[i, 0])


def matlab_tractography(mat_file, img):
    """
    Converts a matlab tractography file to a stateful tractogram.

    Parameters
    ----------
    mat_file : str
        Path to a matlab tractography file.
    img : Nifti1Image or str
        Path to an img file to be loaded with nibabel or an img
        to serve as the reference for the stateful tractogram.

    Returns
    -------
    DIPY :class:`StatefulTractogram` in RASMM space.
    """
    mat_file = scipy.io.loadmat(mat_file)
    if isinstance(img, str):
        img = nib.load(img)

    tracker = MatlabFileTracking(mat_file['fg']['fibers'][0][0])
    return StatefulTractogram(tracker, img, Space.RASMM)


def matlab_mori_groups(mat_file, img):
    """
    Converts a matlab Mori groups file to a dictionary of fiber groups.
    This dictionary is structured the same way as the results of pyAFQ
    segmentation. The keys are bundle names and the values are 
    :class:`StatefulTractogram` instances.
    If you want to merge this dictionary into one :class:`StatefulTractogram`,
    use :class:`SegmentedSFT`.

    Parameters
    ----------
    mat_file : str
        Path to a matlab Mori groups file.
    img : Nifti1Image or str
        Path to an img file to be loaded with nibabel or an img
        to serve as the reference for the stateful tractogram.

    Returns
    -------
    Dictionary where keys are the pyAFQ bundle names and values are
    DIPY :class:`StatefulTractogram` instances in RASMM space.
    """
    mat_file = scipy.io.loadmat(mat_file)
    if isinstance(img, str):
        img = nib.load(img)

    fiber_groups = {}
    for i in range(mat_file["fg"]["name"].shape[1]):
        name = mat_file["fg"]["name"][0][i][0]
        py_name = None
        if name in BUNDLE_MAT_2_PYTHON.keys():
            py_name = BUNDLE_MAT_2_PYTHON[name]
        elif name in BUNDLE_MAT_2_PYTHON.values():
            py_name = name
        if py_name is not None:
            bundle_ref = mat_file["fg"]["fibers"][0][i]
            tracker = MatlabFileTracking(bundle_ref)
            fiber_groups[py_name] =\
                StatefulTractogram(tracker, img, Space.RASMM)

    return fiber_groups
