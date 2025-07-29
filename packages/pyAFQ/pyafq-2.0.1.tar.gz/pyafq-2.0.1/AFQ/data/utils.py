BUNDLE_RECO_2_AFQ = \
    {
        "AF_L": "Left Arcuate", "AF_R": "Right Arcuate",
        "UF_L": "Left Uncinate", "UF_R": "Right Uncinate",
        "IFOF_L": "Left Inferior Fronto-occipital",
        "IFOF_R": "Right Inferior Fronto-occipital",
        "CST_L": "Left Corticospinal", "CST_R": "Right Corticospinal",
        "ILF_L": "Left Inferior Longitudinal",
        "ILF_R": "Right Inferior Longitudinal",
        "SLF_L": "Left Superior Longitudinal",
        "SLF_R": "Right Superior Longitudinal"
    }


BUNDLE_MAT_2_PYTHON = {
    'RightCorticospinal': 'Right Corticospinal',
    'LeftCorticospinal': 'Left Corticospinal',
    'RightUncinate': 'Right Uncinate', 'LeftUncinate': 'Left Uncinate',
    'Left IFOF': 'Left Inferior Fronto-occipital',
    'Right IFOF': 'Right Inferior Fronto-occipital',
    'LeftIFOF': 'Left Inferior Fronto-occipital',
    'RightIFOF': 'Right Inferior Fronto-occipital',
    'RightArcuate': 'Right Arcuate', 'LeftArcuate': 'Left Arcuate',
    'Right Thalamic Radiation': 'Right Anterior Thalamic',
    'Left Thalamic Radiation': 'Left Anterior Thalamic',
    'RightThalamicRadiation': 'Right Anterior Thalamic',
    'LeftThalamicRadiation': 'Left Anterior Thalamic',
    'Right Cingulum Cingulate': 'Right Cingulum Cingulate',
    'Left Cingulum Cingulate': 'Left Cingulum Cingulate',
    'RightCingulumCingulate': 'Right Cingulum Cingulate',
    'LeftCingulumCingulate': 'Left Cingulum Cingulate',
    'Callosum Forceps Major': 'Forceps Major',
    'Callosum Forceps Minor': 'Forceps Minor',
    'CallosumForcepsMajor': 'Forceps Major',
    'CallosumForcepsMinor': 'Forceps Minor',
    'Right ILF': 'Right Inferior Longitudinal',
    'Left ILF': 'Left Inferior Longitudinal',
    'RightILF': 'Right Inferior Longitudinal',
    'LeftILF': 'Left Inferior Longitudinal',
    'Right SLF': 'Right Superior Longitudinal',
    'Left SLF': 'Left Superior Longitudinal',
    'RightSLF': 'Right Superior Longitudinal',
    'LeftSLF': 'Left Superior Longitudinal'}


def aws_import_msg_error(module):
    """Alerts user to install the appropriate aws module """
    msg = f"To use {module} in pyAFQ, you will "
    msg += f"need to have {module} installed. "
    msg += "You can do that by installing pyAFQ with "
    msg += f"`pip install AFQ[aws]`"
    return msg
