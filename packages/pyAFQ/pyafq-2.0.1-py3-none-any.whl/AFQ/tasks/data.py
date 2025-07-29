import nibabel as nib
import numpy as np
import logging

from dipy.io.gradients import read_bvals_bvecs
import dipy.core.gradients as dpg
from dipy.data import default_sphere

import pimms

import dipy.reconst.dki as dpy_dki
import dipy.reconst.dti as dpy_dti
import dipy.reconst.fwdti as dpy_fwdti
import dipy.reconst.msdki as dpy_msdki
from dipy.reconst.gqi import GeneralizedQSamplingModel
from dipy.reconst.rumba import RumbaSDModel, RumbaFit
from dipy.reconst import shm
from dipy.reconst.dki_micro import axonal_water_fraction

from AFQ.tasks.decorators import as_file, as_img, as_fit_deriv
from AFQ.tasks.utils import get_fname, with_name, str_to_desc
import AFQ.api.bundle_dict as abd
import AFQ.data.fetch as afd
from AFQ.utils.path import drop_extension, write_json
from AFQ._fixes import gwi_odf

from AFQ.definitions.utils import Definition
from AFQ.definitions.image import B0Image

from AFQ.models.dti import noise_from_b0
from AFQ.models.csd import _fit as csd_fit_model
from AFQ.models.csd import CsdNanResponseError
from AFQ.models.dki import _fit as dki_fit_model
from AFQ.models.dti import _fit as dti_fit_model
from AFQ.models.fwdti import _fit as fwdti_fit_model
from AFQ.models.QBallTP import (
    extract_odf, anisotropic_index, anisotropic_power)


logger = logging.getLogger('AFQ')


DIPY_GH = "https://github.com/dipy/dipy/blob/master/dipy/"


@pimms.calc("data", "gtab", "dwi", "dwi_affine")
def get_data_gtab(dwi_data_file, bval_file, bvec_file, min_bval=None,
                  max_bval=None, filter_b=True, b0_threshold=50):
    """
    DWI data as an ndarray for selected b values,
    A DIPY GradientTable with all the gradient information,
    DWI data in a Nifti1Image,
    and the affine transformation of the DWI data

    Parameters
    ----------
    min_bval : float, optional
        Minimum b value you want to use
        from the dataset (other than b0), inclusive.
        If None, there is no minimum limit. Default: None
    max_bval : float, optional
        Maximum b value you want to use
        from the dataset (other than b0), inclusive.
        If None, there is no maximum limit. Default: None
    filter_b : bool, optional
        Whether to filter the DWI data based on min or max bvals.
        Default: True
    b0_threshold : int, optional
        The value of b under which
        it is considered to be b0. Default: 50.
    """
    img = nib.load(dwi_data_file)
    bvals, bvecs = read_bvals_bvecs(bval_file, bvec_file)

    data = img.get_fdata()
    if filter_b and (min_bval is not None):
        valid_b = np.logical_or(
            (bvals >= min_bval), (bvals <= b0_threshold))
        data = data[..., valid_b]
        bvals = bvals[valid_b]
        bvecs = bvecs[valid_b]
    if filter_b and (max_bval is not None):
        valid_b = np.logical_or(
            (bvals <= max_bval), (bvals <= b0_threshold))
        data = data[..., valid_b]
        bvals = bvals[valid_b]
        bvecs = bvecs[valid_b]
    gtab = dpg.gradient_table(
        bvals = bvals, bvecs = bvecs,
        b0_threshold = b0_threshold)
    img = nib.Nifti1Image(data, img.affine)
    return data, gtab, img, img.affine


@pimms.calc("b0")
@as_file('_b0ref.nii.gz')
def b0(dwi, gtab):
    """
    full path to a nifti file containing the mean b0
    """
    mean_b0 = np.mean(dwi.get_fdata()[..., gtab.b0s_mask], -1)
    mean_b0_img = nib.Nifti1Image(mean_b0, dwi.affine)
    meta = dict(b0_threshold=gtab.b0_threshold)
    return mean_b0_img, meta


@pimms.calc("masked_b0")
@as_file('_desc-masked_b0ref.nii.gz')
def b0_mask(b0, brain_mask):
    """
    full path to a nifti file containing the
    mean b0 after applying the brain mask
    """
    img = nib.load(b0)
    brain_mask = nib.load(brain_mask).get_fdata().astype(bool)

    masked_data = img.get_fdata()
    masked_data[~brain_mask] = 0

    masked_b0_img = nib.Nifti1Image(masked_data, img.affine)
    meta = dict(
        source=b0,
        masked=True)
    return masked_b0_img, meta


@pimms.calc("dti_tf")
def dti_fit(dti_params, gtab):
    """DTI TensorFit object"""
    dti_params = nib.load(dti_params).get_fdata()
    tm = dpy_dti.TensorModel(gtab)
    return dpy_dti.TensorFit(tm, dti_params)


@pimms.calc("dti_params")
@as_file(suffix='_model-dti_param-diffusivity_dwimap.nii.gz',
         subfolder="models")
@as_img
def dti_params(brain_mask, data, gtab,
               bval_file, bvec_file, b0_threshold=50,
               robust_tensor_fitting=False):
    """
    full path to a nifti file containing parameters
    for the DTI fit

    Parameters
    ----------
    robust_tensor_fitting : bool, optional
        Whether to use robust_tensor_fitting when
        doing dti. Only applies to dti.
        Default: False
    b0_threshold : int, optional
        The value of b under which
        it is considered to be b0. Default: 50.
    """
    mask =\
        nib.load(brain_mask).get_fdata()
    if robust_tensor_fitting:
        bvals, _ = read_bvals_bvecs(
            bval_file, bvec_file)
        sigma = noise_from_b0(
            data, gtab, bvals,
            mask=mask, b0_threshold=b0_threshold)
    else:
        sigma = None
    dtf = dti_fit_model(
        gtab, data,
        mask=mask, sigma=sigma)
    meta = dict(
        Parameters=dict(
            FitMethod="WLS"),
        OutlierRejection=robust_tensor_fitting,
        ModelURL=f"{DIPY_GH}reconst/dti.py")
    return dtf.model_params, meta


@pimms.calc("fwdti_tf")
def fwdti_fit(fwdti_params, gtab):
    """Free-water DTI TensorFit object"""
    fwdti_params = nib.load(fwdti_params).get_fdata()
    fwtm = dpy_fwdti.FreeWaterTensorModel(gtab)
    return dpy_fwdti.FreeWaterTensorFit(fwtm, fwdti_params)


@pimms.calc("fwdti_params")
@as_file(suffix='_model-fwdti_param-diffusivity_dwimap.nii.gz',
         subfolder="models")
@as_img
def fwdti_params(brain_mask, data, gtab):
    """
    Full path to a nifti file containing parameters
    for the free-water DTI fit.
    """
    mask =\
        nib.load(brain_mask).get_fdata()
    dtf = fwdti_fit_model(
        data, gtab,
        mask=mask)
    meta = dict(
        Parameters=dict(
            FitMethod="NLS"),
        ModelURL=f"{DIPY_GH}reconst/fwdti.py")
    return dtf.model_params, meta


@pimms.calc("dki_tf")
def dki_fit(dki_params, gtab):
    """DKI DiffusionKurtosisFit object"""
    dki_params = nib.load(dki_params).get_fdata()
    tm = dpy_dki.DiffusionKurtosisModel(gtab)
    return dpy_dki.DiffusionKurtosisFit(tm, dki_params)


@pimms.calc("dki_params")
@as_file(suffix='_model-dki_param-diffusivity_dwimap.nii.gz',
         subfolder="models")
@as_img
def dki_params(brain_mask, gtab, data):
    """
    full path to a nifti file containing
    parameters for the DKI fit
    """
    if len(dpg.unique_bvals_magnitude(gtab.bvals)) < 3:
        raise ValueError((
            "The DKI model requires at least 2 non-zero b-values, "
            f"but you provided {len(dpg.unique_bvals_magnitude(gtab.bvals))}"
            " b-values (including b=0)."))
    mask =\
        nib.load(brain_mask).get_fdata()
    dkf = dki_fit_model(
        gtab, data,
        mask=mask)
    meta = dict(
        Parameters=dict(
            FitMethod="WLS"),
        OutlierRejection=False,
        ModelURL=f"{DIPY_GH}reconst/dki.py")
    return dkf.model_params, meta


@pimms.calc("msdki_tf")
def msdki_fit(msdki_params, gtab):
    """Mean Signal DKI DiffusionKurtosisFit object"""
    msdki_params = nib.load(msdki_params).get_fdata()
    tm = dpy_msdki.MeanDiffusionKurtosisModel(gtab)
    return dpy_msdki.MeanDiffusionKurtosisFit(tm, msdki_params)


@pimms.calc("msdki_params")
@as_file(suffix='_model-msdki_param-diffusivity_dwimap.nii.gz',
         subfolder="models")
@as_img
def msdki_params(brain_mask, gtab, data):
    """
    full path to a nifti file containing
    parameters for the Mean Signal DKI fit
    """
    mask =\
        nib.load(brain_mask).get_fdata()
    msdki_model = dpy_msdki.MeanDiffusionKurtosisModel(gtab)
    msdki_fit = msdki_model.fit(data, mask=mask)
    meta = dict(
        ModelURL=f"{DIPY_GH}reconst/msdki.py")
    return msdki_fit.model_params, meta


@pimms.calc("msdki_msd")
@as_file('_model-msdki_param-msd_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('MSDKI')
def msdki_msd(msdki_tf):
    """
    full path to a nifti file containing
    the MSDKI mean signal diffusivity
    """
    return msdki_tf.msd


@pimms.calc("msdki_msk")
@as_file('_model-msdki_param-msk_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('MSDKI')
def msdki_msk(msdki_tf):
    """
    full path to a nifti file containing
    the MSDKI mean signal kurtosis
    """
    return msdki_tf.msk


@pimms.calc("csd_params")
@as_file(suffix='_model-csd_param-fod_dwimap.nii.gz',
         subfolder="models")
@as_img
def csd_params(dwi, brain_mask, gtab, data,
               csd_response=None, csd_sh_order=None,
               csd_lambda_=1, csd_tau=0.1,
               csd_fa_thr=0.7):
    """
    full path to a nifti file containing
    parameters for the CSD fit

    Parameters
    ----------
    csd_response : tuple or None, optional.
        The response function to be used by CSD, as a tuple with two elements.
        The first is the eigen-values as an (3,) ndarray and the second is
        the signal value for the response function without diffusion-weighting
        (i.e. S0). If not provided, auto_response will be used to calculate
        these values.
        Default: None
    csd_sh_order : int or None, optional.
        default: infer the number of parameters from the number of data
        volumes, but no larger than 8.
        Default: None
    csd_lambda_ : float, optional.
        weight given to the constrained-positivity regularization part of
        the deconvolution equation. Default: 1
    csd_tau : float, optional.
        threshold controlling the amplitude below which the corresponding
        fODF is assumed to be zero.  Ideally, tau should be set to
        zero. However, to improve the stability of the algorithm, tau is
        set to tau*100 percent of the mean fODF amplitude (here, 10 percent
        by default)
        (see [1]_). Default: 0.1
    csd_fa_thr : float, optional.
        The threshold on the FA used to calculate the single shell auto
        response. Can be useful to reduce for baby subjects. Default: 0.7

    References
    ----------
    .. [1] Tournier, J.D., et al. NeuroImage 2007. Robust determination of
            the fibre orientation distribution in diffusion MRI:
            Non-negativity constrained super-resolved spherical
            deconvolution
    """
    mask =\
        nib.load(brain_mask).get_fdata()
    try:
        csdf = csd_fit_model(
            gtab, data,
            mask=mask,
            response=csd_response, sh_order=csd_sh_order,
            lambda_=csd_lambda_, tau=csd_tau,
            csd_fa_thr=csd_fa_thr)
    except CsdNanResponseError as e:
        raise CsdNanResponseError(
            'Could not compute CSD response function for file: '
            f'{dwi}.') from e

    meta = dict(
        SphericalHarmonicDegree=csd_sh_order,
        ResponseFunctionTensor=csd_response,
        lambda_=csd_lambda_,
        tau=csd_tau,
        csd_fa_thr=csd_fa_thr)
    meta["SphericalHarmonicBasis"] = "DESCOTEAUX"
    meta["ModelURL"] = f"{DIPY_GH}reconst/csdeconv.py"
    return csdf.shm_coeff, meta


@pimms.calc("csd_pmap")
@as_file(suffix='_model-csd_param-apm_dwimap.nii.gz',
         subfolder="models")
@as_img
def anisotropic_power_map(csd_params):
    """
    full path to a nifti file containing
    the anisotropic power map
    """
    sh_coeff = nib.load(csd_params).get_fdata()
    pmap = anisotropic_power(sh_coeff)
    return pmap, dict(CSDParamsFile=csd_params)


@pimms.calc("csd_ai")
@as_file(suffix='_model-csd_param-ai_dwimap.nii.gz',
         subfolder="models")
@as_img
def csd_anisotropic_index(csd_params):
    """
    full path to a nifti file containing
    the anisotropic index
    """
    sh_coeff = nib.load(csd_params).get_fdata()
    AI = anisotropic_index(sh_coeff)
    return AI, dict(CSDParamsFile=csd_params)


@pimms.calc("gq_params", "gq_iso", "gq_aso")
def gq(base_fname, gtab, dwi_affine, data,
       gq_sampling_length=1.2):
    """
    full path to a nifti file containing
    parameters for the Generalized Q-Sampling
    shm_coeff,
    full path to a nifti file containing isotropic diffusion component,
    full path to a nifti file containing anisotropic diffusion component

    Parameters
    ----------
    gq_sampling_length : float
        Diffusion sampling length.
        Default: 1.2
    """
    gqmodel = GeneralizedQSamplingModel(
        gtab,
        sampling_length=gq_sampling_length)

    odf = gwi_odf(gqmodel, data)

    GQ_shm, ASO, ISO = extract_odf(odf)

    params_suffix = "_model-GQ_param-fod_dwimap.nii.gz"
    params_fname = get_fname(base_fname, params_suffix, "models")
    nib.save(nib.Nifti1Image(GQ_shm, dwi_affine), params_fname)
    write_json(
        get_fname(
            base_fname,
            f"{drop_extension(params_suffix)}.json",
            "models"),
        dict(GQSamplingLength=gq_sampling_length)
    )

    ASO_suffix = "_model-GQ_param-ASO_dwimap.nii.gz"
    ASO_fname = get_fname(base_fname, ASO_suffix, "models")
    nib.save(nib.Nifti1Image(ASO, dwi_affine), ASO_fname)
    write_json(
        get_fname(
            base_fname,
            f"{drop_extension(ASO_suffix)}.json",
            "models"),
        dict(GQSamplingLength=gq_sampling_length)
    )

    ISO_suffix = "_model-GQ_param-ISO_dwimap.nii.gz"
    ISO_fname = get_fname(base_fname, ISO_suffix, "models")
    nib.save(nib.Nifti1Image(ISO, dwi_affine), ISO_fname)
    write_json(
        get_fname(base_fname, f"{drop_extension(ISO_suffix)}.json", "models"),
        dict(GQSamplingLength=gq_sampling_length)
    )

    return params_fname, ISO_fname, ASO_fname


@pimms.calc("gq_pmap")
@as_file(suffix='_model-gq_param-apm_dwimap.nii.gz',
         subfolder="models")
@as_img
def gq_pmap(gq_params):
    """
    full path to a nifti file containing
    the anisotropic power map from GQ
    """
    sh_coeff = nib.load(gq_params).get_fdata()
    pmap = anisotropic_power(sh_coeff)
    return pmap, dict(GQParamsFile=gq_params)


@pimms.calc("gq_ai")
@as_file(suffix='_model-gq_param-ai_dwimap.nii.gz',
         subfolder="models")
@as_img
def gq_ai(gq_params):
    """
    full path to a nifti file containing
    the anisotropic index from GQ
    """
    sh_coeff = nib.load(gq_params).get_fdata()
    AI = anisotropic_index(sh_coeff)
    return AI, dict(GQParamsFile=gq_params)


@pimms.calc("rumba_model")
def rumba_model(gtab,
                rumba_wm_response=[0.0017, 0.0002, 0.0002],
                rumba_gm_response=0.0008,
                rumba_csf_response=0.003,
                rumba_n_iter=600):
    """
    fit for RUMBA-SD model as documented on dipy reconstruction options

    Parameters
    ----------
    rumba_wm_response: 1D or 2D ndarray or AxSymShResponse.
        Able to take response[0] from auto_response_ssst.
        default: array([0.0017, 0.0002, 0.0002])
    rumba_gm_response: float, optional
        Mean diffusivity for GM compartment.
        If None, then grey matter volume fraction is not computed.
        Default: 0.8e-3
    rumba_csf_response: float, optional
        Mean diffusivity for CSF compartment.
        If None, then CSF volume fraction is not computed.
        Default: 3.0e-3
    rumba_n_iter: int, optional
        Number of iterations for fODF estimation.
        Must be a positive int.
        Default: 600
    """
    return RumbaSDModel(
        gtab,
        wm_response=np.asarray(rumba_wm_response),
        gm_response=rumba_gm_response,
        csf_response=rumba_csf_response,
        n_iter=rumba_n_iter,
        recon_type='smf',
        n_coils=1,
        R=1,
        voxelwise=False,
        use_tv=False,
        sphere=default_sphere,
        verbose=True)


@pimms.calc("rumba_params")
@as_file(suffix='_model-rumba_param-fod_dwimap.nii.gz',
         subfolder="models")
@as_img
def rumba_params(rumba_model, data, brain_mask):
    """
    Takes the fitted RUMBA-SD model as input and returns
    the spherical harmonics coefficients (SHM).
    """
    rumba_fit = rumba_model.fit(
        data,
        mask=nib.load(brain_mask).get_fdata())
    odf = rumba_fit.odf(sphere=default_sphere)
    rumba_shm, _, _ = extract_odf(odf)
    meta = dict()
    return rumba_shm, meta


@pimms.calc("rumba_fit")
def rumba_fit(rumba_model, rumba_params):
    """RUMBA FIT"""
    return RumbaFit(
        rumba_model,
        nib.load(rumba_params).get_fdata())


@pimms.calc("rumba_f_csf")
@as_file(suffix='_model-rumba_param-csf_probseg.nii.gz',
         subfolder="models")
@as_fit_deriv('RUMBA')
def rumba_f_csf(rumba_fit):
    """
    full path to a nifti file containing
    the CSF volume fraction for each voxel.
    """
    return rumba_fit.f_csf  # CSF volume fractions


@pimms.calc("rumba_f_gm")
@as_file(suffix='_model-rumba_param-gm_probseg.nii.gz',
         subfolder="models")
@as_fit_deriv('RUMBA')
def rumba_f_gm(rumba_fit):
    """
    full path to a nifti file containing
    the GM volume fraction for each voxel.
    """
    return rumba_fit.f_gm  # gray matter volume fractions


@pimms.calc("rumba_f_wm")
@as_file(suffix='_model-rumba_param-wm_probseg.nii.gz',
         subfolder="models")
@as_fit_deriv('RUMBA')
def rumba_f_wm(rumba_fit):
    """
    full path to a nifti file containing
    the white matter volume fraction for each voxel.
    """
    return rumba_fit.f_wm  # white matter volume fractions


@pimms.calc("opdt_params", "opdt_gfa")
def opdt_params(base_fname, data, gtab,
                dwi_affine, brain_mask,
                opdt_sh_order=8):
    """
    full path to a nifti file containing
    parameters for the Orientation Probability Density Transform
    shm_coeff,
    full path to a nifti file containing GFA

    Parameters
    ----------
    opdt_sh_order : int
        Spherical harmonics order for OPDT model. Must be even.
        Default: 8
    """
    opdt_model = shm.OpdtModel(gtab, opdt_sh_order)
    opdt_fit = opdt_model.fit(data, mask=brain_mask)

    params_suffix = "_model-OPDT_param-fod_dwimap.nii.gz"
    params_fname = get_fname(base_fname, params_suffix, "models")
    nib.save(nib.Nifti1Image(opdt_fit._shm_coef, dwi_affine), params_fname)
    write_json(
        get_fname(base_fname,
                  f"{drop_extension(params_suffix)}.json",
                  "models"),
        dict(sh_order=opdt_sh_order)
    )

    GFA_suffix = "_model-OPDT_param-GFA_dwimap.nii.gz"
    GFA_fname = get_fname(base_fname, GFA_suffix, "models")
    nib.save(nib.Nifti1Image(opdt_fit.gfa, dwi_affine), GFA_fname)
    write_json(
        get_fname(base_fname, f"{drop_extension(GFA_suffix)}.json", "models"),
        dict(sh_order=opdt_sh_order)
    )

    return params_fname, GFA_fname


@pimms.calc("opdt_pmap")
@as_file(suffix='_model-opdt_param-apm_dwimap.nii.gz',
         subfolder="models")
@as_img
def opdt_pmap(opdt_params):
    """
    full path to a nifti file containing
    the anisotropic power map from OPDT
    """
    sh_coeff = nib.load(opdt_params).get_fdata()
    pmap = anisotropic_power(sh_coeff)
    return pmap, dict(OPDTParamsFile=opdt_params)


@pimms.calc("opdt_ai")
@as_file(suffix='_model-opdt_param-ai_dwimap.nii.gz',
         subfolder="models")
@as_img
def opdt_ai(opdt_params):
    """
    full path to a nifti file containing
    the anisotropic index from OPDT
    """
    sh_coeff = nib.load(opdt_params).get_fdata()
    AI = anisotropic_index(sh_coeff)
    return AI, dict(OPDTParamsFile=opdt_params)


@pimms.calc("csa_params", "csa_gfa")
def csa_params(base_fname, data, gtab,
               dwi_affine, brain_mask,
               csa_sh_order=8):
    """
    full path to a nifti file containing
    parameters for the Constant Solid Angle
    shm_coeff,
    full path to a nifti file containing GFA

    Parameters
    ----------
    csa_sh_order : int
        Spherical harmonics order for CSA model. Must be even.
        Default: 8
    """
    csa_model = shm.CsaOdfModel(gtab, csa_sh_order)
    csa_fit = csa_model.fit(data, mask=brain_mask)

    params_suffix = "_model-csa_param-fod_dwimap.nii.gz"
    params_fname = get_fname(base_fname, params_suffix, "models")
    nib.save(nib.Nifti1Image(csa_fit._shm_coef, dwi_affine), params_fname)
    write_json(
        get_fname(base_fname,
                  f"{drop_extension(params_suffix)}.json",
                  "models"),
        dict(sh_order=csa_sh_order)
    )

    GFA_suffix = "_model-csa_param-gfa_dwimap.nii.gz"
    GFA_fname = get_fname(base_fname, GFA_suffix, "models")
    nib.save(nib.Nifti1Image(csa_fit.gfa, dwi_affine), GFA_fname)
    write_json(
        get_fname(
            base_fname,
            f"{drop_extension(GFA_suffix)}.json",
            "models"),
        dict(sh_order=csa_sh_order)
    )

    return params_fname, GFA_fname


@pimms.calc("csa_pmap")
@as_file(suffix='_model-csa_param-apm_dwimap.nii.gz',
         subfolder="models")
@as_img
def csa_pmap(csa_params):
    """
    full path to a nifti file containing
    the anisotropic power map from CSA
    """
    sh_coeff = nib.load(csa_params).get_fdata()
    pmap = anisotropic_power(sh_coeff)
    return pmap, dict(CSAParamsFile=csa_params)


@pimms.calc("csa_ai")
@as_file(suffix='_model-csa_param-ai_dwimap.nii.gz',
         subfolder="models")
@as_img
def csa_ai(csa_params):
    """
    full path to a nifti file containing
    the anisotropic index from CSA
    """
    sh_coeff = nib.load(csa_params).get_fdata()
    AI = anisotropic_index(sh_coeff)
    return AI, dict(CSAParamsFile=csa_params)


@pimms.calc("fwdti_fa")
@as_file(suffix='_model-fwdti_param-fa_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('FWDTI')
def fwdti_fa(fwdti_tf):
    """
    full path to a nifti file containing the Free-water DTI fractional
    anisotropy
    """
    return fwdti_tf.fa


@pimms.calc("fwdti_md")
@as_file(suffix='_model-fwdti_param-md_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('FWDTI')
def fwdti_md(fwdti_tf):
    """
    full path to a nifti file containing the Free-water DTI mean diffusivity
    """
    return fwdti_tf.md


@pimms.calc("fwdti_fwf")
@as_file(suffix='_model-fwdti_param-fwf_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('FWDTI')
def fwdti_fwf(fwdti_tf):
    """
    full path to a nifti file containing the Free-water DTI free water fraction
    """
    return fwdti_tf.f


@pimms.calc("dti_fa")
@as_file(suffix='_model-dti_param-fa_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_fa(dti_tf):
    """
    full path to a nifti file containing
    the DTI fractional anisotropy
    """
    return dti_tf.fa


@pimms.calc("dti_lt0", "dti_lt1", "dti_lt2", "dti_lt3", "dti_lt4", "dti_lt5")
def dti_lt(dti_tf, dwi_affine):
    """
    Image of first element in the DTI tensor according to DIPY convention
    i.e. Dxx (rate of diffusion from the left to right side of the brain),
    Image of second element in the DTI tensor according to DIPY convention
    i.e. Dyy (rate of diffusion from the posterior to anterior part of 
    the brain),
    Image of third element in the DTI tensor according to DIPY convention
    i.e. Dzz (rate of diffusion from the inferior to superior part of the
    brain),
    Image of fourth element in the DTI tensor according to DIPY convention
    i.e. Dxy (rate of diffusion in the xy plane indicating the 
    relationship between the x and y directions),
    Image of fifth element in the DTI tensor according to DIPY convention
    i.e. Dxz (rate of diffusion in the xz plane indicating the
    relationship between the x and z directions),
    Image of sixth element in the DTI tensor according to DIPY convention
    i.e. Dyz (rate of diffusion in the yz plane indicating the
    relationship between the y and z directions)
    """
    dti_lt_dict = {}
    for ii in range(6):
        dti_lt_dict[f"dti_lt{ii}"] = nib.Nifti1Image(
            dti_tf.lower_triangular()[..., ii],
            dwi_affine)
    return dti_lt_dict


@pimms.calc("dti_cfa")
@as_file(suffix='_model-dti_param-cfa_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_cfa(dti_tf):
    """
    full path to a nifti file containing
    the DTI color fractional anisotropy
    """
    return dti_tf.color_fa


@pimms.calc("dti_pdd")
@as_file(suffix='_model-dti_param-pdd_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_pdd(dti_tf):
    """
    full path to a nifti file containing
    the DTI principal diffusion direction
    """
    pdd = dti_tf.directions.squeeze()
    # Invert the x coordinates:
    pdd[..., 0] = pdd[..., 0] * -1
    return pdd


@pimms.calc("dti_md")
@as_file('_model-dti_param-md_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_md(dti_tf):
    """
    full path to a nifti file containing
    the DTI mean diffusivity
    """
    return dti_tf.md


@pimms.calc("dti_ga")
@as_file(suffix='_model-dti_param-ga_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_ga(dti_tf):
    """
    full path to a nifti file containing
    the DTI geodesic anisotropy
    """
    return dti_tf.ga


@pimms.calc("dti_rd")
@as_file(suffix='_model-dti_param-rd_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_rd(dti_tf):
    """
    full path to a nifti file containing
    the DTI radial diffusivity
    """
    return dti_tf.rd


@pimms.calc("dti_ad")
@as_file(suffix='_model-dti_param-ad_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DTI')
def dti_ad(dti_tf):
    """
    full path to a nifti file containing
    the DTI axial diffusivity
    """
    return dti_tf.ad


@pimms.calc(
    "dki_kt0", "dki_kt1", "dki_kt2", "dki_kt3", "dki_kt4",
    "dki_kt5", "dki_kt6", "dki_kt7", "dki_kt8", "dki_kt9",
    "dki_kt10", "dki_kt11", "dki_kt12", "dki_kt13", "dki_kt14")
def dki_kt(dki_tf, dwi_affine):
    """
    Image of first element in the DKI kurtosis model,
    Image of second element in the DKI kurtosis model,
    Image of third element in the DKI kurtosis model,
    Image of fourth element in the DKI kurtosis model,
    Image of fifth element in the DKI kurtosis model,
    Image of sixth element in the DKI kurtosis model,
    Image of seventh element in the DKI kurtosis model,
    Image of eighth element in the DKI kurtosis model,
    Image of ninth element in the DKI kurtosis model,
    Image of tenth element in the DKI kurtosis model,
    Image of eleventh element in the DKI kurtosis model,
    Image of twelfth element in the DKI kurtosis model,
    Image of thirteenth element in the DKI kurtosis model,
    Image of fourteenth element in the DKI kurtosis model,
    Image of fifteenth element in the DKI kurtosis model
    """
    dki_kt_dict = {}
    for ii in range(15):
        dki_kt_dict[f"dki_kt{ii}"] = nib.Nifti1Image(
            dki_tf.kt[..., ii],
            dwi_affine)
    return dki_kt_dict


@pimms.calc("dki_lt0", "dki_lt1", "dki_lt2", "dki_lt3", "dki_lt4", "dki_lt5")
def dki_lt(dki_tf, dwi_affine):
    """
    Image of first element in the DTI tensor from DKI,
    Image of second element in the DTI tensor from DKI,
    Image of third element in the DTI tensor from DKI,
    Image of fourth element in the DTI tensor from DKI,
    Image of fifth element in the DTI tensor from DKI,
    Image of sixth element in the DTI tensor from DKI
    """
    dki_lt_dict = {}
    for ii in range(6):
        dki_lt_dict[f"dki_lt{ii}"] = nib.Nifti1Image(
            dki_tf.lower_triangular()[..., ii],
            dwi_affine)
    return dki_lt_dict


@pimms.calc("dki_fa")
@as_file('_model-dki_param-fa_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_fa(dki_tf):
    """
    full path to a nifti file containing
    the DKI fractional anisotropy
    """
    return dki_tf.fa


@pimms.calc("dki_md")
@as_file('_model-dki_param-md_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_md(dki_tf):
    """
    full path to a nifti file containing
    the DKI mean diffusivity
    """
    return dki_tf.md


@pimms.calc("dki_awf")
@as_file('_model-dki_param-awf_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_awf(dki_params,
            sphere='repulsion100', gtol=1e-2):
    """
    full path to a nifti file containing
    the DKI axonal water fraction

    Parameters
    ----------
    sphere : Sphere class instance, optional
        The sphere providing sample directions for the initial
        search of the maximal value of kurtosis.
        Default: 'repulsion100'
    gtol : float, optional
        This input is to refine kurtosis maxima under the precision of
        the directions sampled on the sphere class instance.
        The gradient of the convergence procedure must be less than gtol
        before successful termination.
        If gtol is None, fiber direction is directly taken from the initial
        sampled directions of the given sphere object.
        Default: 1e-2
    """
    dki_params = nib.load(dki_params).get_fdata()
    return axonal_water_fraction(dki_params, sphere=sphere, gtol=gtol)


@pimms.calc("dki_mk")
@as_file('_model-dki_param-mk_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_mk(dki_tf):
    """
    full path to a nifti file containing
    the DKI mean kurtosis file
    """
    return dki_tf.mk()


@pimms.calc("dki_kfa")
@as_file('_model-dki_param-kfa_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_kfa(dki_tf):
    """
    full path to a nifti file containing
    the DKI kurtosis FA file

    References
    ----------
    .. [Hansen2019] Hansen B. An Introduction to Kurtosis Fractional
    Anisotropy. AJNR Am J Neuroradiol. 2019 Oct;40(10):1638-1641.
    doi: 10.3174/ajnr.A6235. Epub 2019 Sep 26. PMID: 31558496;
    PMCID: PMC7028548.
    """
    return dki_tf.kfa


@pimms.calc("dki_ga")
@as_file(suffix='_model-dki_param-ga_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_ga(dki_tf):
    """
    full path to a nifti file containing
    the DKI geodesic anisotropy
    """
    return dki_tf.ga


@pimms.calc("dki_rd")
@as_file(suffix='_model-dki_param-rd_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_rd(dki_tf):
    """
    full path to a nifti file containing
    the DKI radial diffusivity
    """
    return dki_tf.rd


@pimms.calc("dki_ad")
@as_file(suffix='_model-dki_param-ad_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_ad(dki_tf):
    """
    full path to a nifti file containing
    the DKI axial diffusivity
    """
    return dki_tf.ad


@pimms.calc("dki_rk")
@as_file(suffix='_model-dki_param-rk_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_rk(dki_tf):
    """
    full path to a nifti file containing
    the DKI radial kurtosis
    """
    return dki_tf.rk


@pimms.calc("dki_ak")
@as_file(suffix='_model-dki_param-ak_dwimap.nii.gz',
         subfolder="models")
@as_fit_deriv('DKI')
def dki_ak(dki_tf):
    """
    full path to a nifti file containing
    the DKI axial kurtosis file
    """
    return dki_tf.ak


@pimms.calc("brain_mask")
@as_file('_desc-brain_mask.nii.gz')
def brain_mask(b0, brain_mask_definition=None):
    """
    full path to a nifti file containing
    the brain mask

    Parameters
    ----------
    brain_mask_definition : instance from `AFQ.definitions.image`, optional
        This will be used to create
        the brain mask, which gets applied before registration to a
        template.
        If you want no brain mask to be applied, use FullImage.
        If None, use B0Image()
        Default: None
    """
    # Note that any case where brain_mask_definition is not None
    # is handled in get_data_plan
    # This is just the default
    return B0Image().get_image_getter("data")(b0)


@pimms.calc("bundle_dict", "reg_template", "tmpl_name")
def get_bundle_dict(brain_mask, b0,
                    bundle_info=None, reg_template_spec="mni_T1",
                    reg_template_space_name="mni"):
    """
    Dictionary defining the different bundles to be segmented,
    and a Nifti1Image containing the template for registration,
    and the name of the template space for file outputs

    Parameters
    ----------
    bundle_info : dict or BundleDict, optional
        A dictionary or BundleDict for use in segmentation.
        See `Defining Custom Bundle Dictionaries`
        in the `usage` section of pyAFQ's documentation for details.
        If None, will get all appropriate bundles for the chosen
        segmentation algorithm.
        Default: None
    reg_template_spec : str, or Nifti1Image, optional
        The target image data for registration.
        Can either be a Nifti1Image, a path to a Nifti1Image, or
        if "mni_T2", "dti_fa_template", "hcp_atlas", or "mni_T1",
        image data will be loaded automatically.
        If "hcp_atlas" is used, slr registration will be used
        and reg_subject should be "subject_sls".
        Default: "mni_T1"
    reg_template_space_name : str, optional
        Name to use in file names for the template space.
        Default: "mni"
    """
    if not isinstance(reg_template_spec, str)\
            and not isinstance(reg_template_spec, nib.Nifti1Image):
        raise TypeError(
            "reg_template must be a str or Nifti1Image")

    if bundle_info is not None and not ((
            isinstance(bundle_info, dict)) or (
            isinstance(bundle_info, abd.BundleDict))):
        raise TypeError((
            "bundle_info must be"
            " a dict, or a BundleDict"))

    if bundle_info is None:
        bundle_info = abd.default18_bd() + abd.callosal_bd()

    use_brain_mask = True
    brain_mask = nib.load(brain_mask).get_fdata()
    if np.all(brain_mask == 1.0):
        use_brain_mask = False
    if isinstance(reg_template_spec, nib.Nifti1Image):
        reg_template = reg_template_spec
    else:
        img_l = reg_template_spec.lower()
        if img_l == "mni_t2":
            reg_template = afd.read_mni_template(
                mask=use_brain_mask, weight="T2w")
        elif img_l == "mni_t1":
            reg_template = afd.read_mni_template(
                mask=use_brain_mask, weight="T1w")
        elif img_l == "dti_fa_template":
            reg_template = afd.read_ukbb_fa_template(mask=use_brain_mask)
        elif img_l == "hcp_atlas":
            reg_template = afd.read_mni_template(mask=use_brain_mask)
        elif img_l == "pediatric":
            reg_template = afd.read_pediatric_templates()[
                "UNCNeo-withCerebellum-for-babyAFQ"]
        else:
            reg_template = nib.load(reg_template_spec)

    if isinstance(bundle_info, abd.BundleDict):
        bundle_dict = bundle_info.copy()
    else:
        bundle_dict = abd.BundleDict(
            bundle_info,
            resample_to=reg_template)

    if bundle_dict.resample_subject_to is None:
        bundle_dict.resample_subject_to = b0

    return bundle_dict, reg_template, reg_template_space_name


def get_data_plan(kwargs):
    if "scalars" in kwargs and not (
        isinstance(kwargs["scalars"], list) and isinstance(
            kwargs["scalars"][0], (str, Definition))):
        raise TypeError(
            "scalars must be a list of "
            "strings/scalar definitions")

    data_tasks = with_name([
        get_data_gtab, b0, b0_mask, brain_mask,
        dti_fit, dki_fit, fwdti_fit, anisotropic_power_map,
        csd_anisotropic_index,
        dti_fa, dti_lt, dti_cfa, dti_pdd, dti_md, dki_kt, dki_lt, dki_fa,
        gq, gq_pmap, gq_ai, opdt_params, opdt_pmap, opdt_ai,
        csa_params, csa_pmap, csa_ai,
        fwdti_fa, fwdti_md, fwdti_fwf,
        msdki_fit, msdki_params, msdki_msd, msdki_msk,
        dki_md, dki_awf, dki_mk, dki_kfa, dki_ga, dki_rd,
        dti_ga, dti_rd, dti_ad,
        dki_ad, dki_rk, dki_ak, dti_params, dki_params, fwdti_params,
        rumba_fit, rumba_params, rumba_model,
        rumba_f_csf, rumba_f_gm, rumba_f_wm,
        csd_params, get_bundle_dict])

    if "scalars" not in kwargs:
        bvals, _ = read_bvals_bvecs(kwargs["bval_file"], kwargs["bvec_file"])
        if len(dpg.unique_bvals_magnitude(bvals)) > 2:
            kwargs["scalars"] = [
                "dki_fa", "dki_md",
                "dki_kfa", "dki_mk"]
        else:
            kwargs["scalars"] = [
                "dti_fa", "dti_md"]
    else:
        scalars = []
        for scalar in kwargs["scalars"]:
            if isinstance(scalar, str):
                scalars.append(scalar.lower())
            else:
                scalars.append(scalar)
        kwargs["scalars"] = scalars

    bm_def = kwargs.get(
        "brain_mask_definition", None)
    if bm_def is not None:
        if not isinstance(bm_def, Definition):
            raise TypeError(
                "brain_mask_definition must be a Definition")
        data_tasks["brain_mask_res"] = pimms.calc("brain_mask")(
            as_file(
                suffix=(
                    f'_desc-{str_to_desc(bm_def.get_name())}'
                    '_mask.nii.gz'),
                subfolder="models")(bm_def.get_image_getter("data")))

    return pimms.plan(**data_tasks)
