
import numpy as np
import pandas as pd

from tqdm import tqdm
from collections import deque
from pyteomics import mzml

from mhcbooster.utils.constants import PROTON_MASS

def _extract_rt(spectrum):
    rt = spectrum['scanList']['scan'][0]['scan start time']
    return rt

def _extract_mz(spectrum):
    precursor = spectrum['precursorList']['precursor'][0]
    precursor_mz = precursor['selectedIonList']['selectedIon'][0]['selected ion m/z']
    lower_offset = precursor['isolationWindow']['isolation window lower offset']
    upper_offset = precursor['isolationWindow']['isolation window upper offset']
    return precursor_mz, lower_offset, upper_offset

def _extract_im_ms2(spectrum):
    mzs = spectrum['m/z array']
    ints = spectrum['intensity array']
    precursor = spectrum['precursorList']['precursor'][0]
    ce = precursor['activation']['collision energy']
    im = 0
    if 'inverse reduced ion mobility' in precursor['selectedIonList']['selectedIon'][0].keys():
        im = precursor['selectedIonList']['selectedIon'][0]['inverse reduced ion mobility']
    return im, ce, mzs, ints

def _extract_im_ms2_msfragger(spectrum):
    mzs = spectrum['m/z array']
    ints = spectrum['intensity array']
    if 'collision energy' in spectrum['precursorList']['precursor'][0]['activation'].keys():
        ce = spectrum['precursorList']['precursor'][0]['activation']['collision energy']
    else:
        ce = 25
    im = 0
    if 'inverse reduced ion mobility' in spectrum['scanList']['scan'][0].keys():
        im = spectrum['scanList']['scan'][0]['inverse reduced ion mobility']
    return im, ce, mzs, ints


def get_rt_ccs_ms2_from_mzml(mzml_path, scan_nrs, masses, charges):

    target_mzs = masses / charges + PROTON_MASS
    mzml_file = mzml.read(mzml_path)
    ms1_list = [data for data in tqdm(mzml_file, desc='Loading mzML spectra to memory...')]
    ms2_list = [data for data in ms1_list if data['ms level'] == 2]

    if len(ms2_list) > 0 and 'inverse reduced ion mobility' in ms2_list[0]['precursorList']['precursor'][0]['selectedIonList']['selectedIon'][0].keys():
        ms_list = ms2_list
    else:
        ms_list = ms1_list
    exp_rts = [None] * len(scan_nrs)
    exp_ims = [None] * len(scan_nrs)
    exp_mzs = [None] * len(scan_nrs)
    exp_intensities = [None] * len(scan_nrs)
    exp_ces = [None] * len(scan_nrs)
    for i, scan_nr in tqdm(enumerate(scan_nrs), total=len(scan_nrs), desc='Extracting RTs, CCSs, MS2s...'):
        spectrum = ms_list[scan_nr - 1]
        target_rt = _extract_rt(spectrum)
        exp_rts[i] = target_rt
        precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
        if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
            im, ce, mzs, ints = _extract_im_ms2(spectrum)
            exp_ims[i] = im
            exp_ces[i] = ce
            exp_mzs[i] = mzs
            exp_intensities[i] = ints
            continue

        # Search neighbor for TimsTOF data
        matched = False
        for j in range(1, scan_nr):  # to left
            spectrum = ms_list[scan_nr - j - 1]
            rt = _extract_rt(spectrum)
            if rt != target_rt:
                break
            precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
            if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
                matched = True
                im, ce, mzs, ints = _extract_im_ms2(spectrum)
                exp_ims[i] = im
                exp_ces[i] = ce
                exp_mzs[i] = mzs
                exp_intensities[i] = ints
                break
        if matched:
            continue
        for j in range(1, len(ms_list) - scan_nr + 1): # to right
            spectrum = ms_list[scan_nr + j - 1]
            rt = spectrum['scanList']['scan'][0]['scan start time']
            if rt != target_rt:
                break
            precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
            if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
                matched = True
                im, ce, mzs, ints = _extract_im_ms2(spectrum)
                exp_ims[i] = im
                exp_ces[i] = ce
                exp_mzs[i] = mzs
                exp_intensities[i] = ints
                break
        if not matched:
            print('Spectrum not matched. IDK what\'s going on here. Interesting.')

    exp_rts = np.array(exp_rts)
    exp_ims = np.array(exp_ims)
    exp_spectra = pd.DataFrame()
    exp_spectra['mzs'] = exp_mzs
    exp_spectra['intensities'] = exp_intensities
    exp_spectra['ce'] = exp_ces
    return exp_rts, exp_ims, exp_spectra


def get_rt_ccs_ms2_from_timsconvert_mzml(mzml_path, scan_nrs, masses, charges):

    target_mzs = masses / charges + PROTON_MASS
    mzml_file = mzml.read(mzml_path)
    ms1_list = [data for data in tqdm(mzml_file, desc='Loading mzML spectra to memory...')]
    # ms2_list = [data for data in ms1_list if data['ms level'] == 2]

    # if len(ms2_list) > 0 and 'inverse reduced ion mobility' in ms2_list[0]['precursorList']['precursor'][0]['selectedIonList']['selectedIon'][0].keys():
    #     ms_list = ms2_list
    # else:
    #     ms_list = ms1_list
    ms_list = ms1_list
    exp_rts = [None] * len(scan_nrs)
    exp_ims = [None] * len(scan_nrs)
    exp_mzs = [None] * len(scan_nrs)
    exp_intensities = [None] * len(scan_nrs)
    exp_ces = [None] * len(scan_nrs)
    for i, scan_nr in tqdm(enumerate(scan_nrs), total=len(scan_nrs), desc='Extracting RTs, CCSs, MS2s...'):
        spectrum = ms_list[scan_nr - 1]
        target_rt = _extract_rt(spectrum)
        exp_rts[i] = target_rt
        precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
        if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
            im, ce, mzs, ints = _extract_im_ms2(spectrum)
            exp_ims[i] = im
            exp_ces[i] = ce
            exp_mzs[i] = mzs
            exp_intensities[i] = ints
            continue

        # Search neighbor for TimsTOF data
        matched = False
        for j in range(1, scan_nr):  # to left
            spectrum = ms_list[scan_nr - j - 1]
            rt = _extract_rt(spectrum)
            if rt != target_rt:
                break
            precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
            if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
                matched = True
                im, ce, mzs, ints = _extract_im_ms2(spectrum)
                exp_ims[i] = im
                exp_ces[i] = ce
                exp_mzs[i] = mzs
                exp_intensities[i] = ints
                break
        if matched:
            continue
        for j in range(1, len(ms_list) - scan_nr + 1): # to right
            spectrum = ms_list[scan_nr + j - 1]
            rt = spectrum['scanList']['scan'][0]['scan start time']
            if rt != target_rt:
                break
            precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
            if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
                matched = True
                im, ce, mzs, ints = _extract_im_ms2(spectrum)
                exp_ims[i] = im
                exp_ces[i] = ce
                exp_mzs[i] = mzs
                exp_intensities[i] = ints
                break
        if not matched:
            print('Spectrum not matched. IDK what\'s going on here. Interesting.')

    exp_rts = np.array(exp_rts)
    exp_ims = np.array(exp_ims)
    exp_spectra = pd.DataFrame()
    exp_spectra['mzs'] = exp_mzs
    exp_spectra['intensities'] = exp_intensities
    exp_spectra['ce'] = exp_ces
    return exp_rts, exp_ims, exp_spectra


def get_rt_ccs_ms2_from_msfragger_mzml(mzml_path, scan_nrs, masses, charges):

    target_mzs = masses / charges + PROTON_MASS
    mzml_file = mzml.read(mzml_path)
    scan_nrs = [str(nr) for nr in scan_nrs]
    ms2_list = deque()
    scan_nr_idx = 0
    for data in tqdm(mzml_file, desc='Loading related MS2 spectrum to memory...'):
        tmp_scan_nr = data['spectrum title'].rsplit('.', 2)[-2]
        if tmp_scan_nr == scan_nrs[scan_nr_idx]:
            ms2_list.append(data)
            scan_nr_idx += 1
            if scan_nr_idx == len(scan_nrs):
                break
    ms2_list = list(ms2_list)
    assert len(ms2_list) == len(scan_nrs), 'Error in MSFragger uncalibrated mzML file reading...'
    exp_rts = [None] * len(scan_nrs)
    exp_ims = [None] * len(scan_nrs)
    exp_mzs = [None] * len(scan_nrs)
    exp_intensities = [None] * len(scan_nrs)
    exp_ces = [None] * len(scan_nrs)
    for i, scan_nr in tqdm(enumerate(scan_nrs), total=len(scan_nrs), desc='Extracting RTs, CCSs, MS2s...'):
        spectrum = ms2_list[i]
        target_rt = _extract_rt(spectrum)
        exp_rts[i] = target_rt
        precursor_mz, lower_offset, upper_offset = _extract_mz(spectrum)
        if precursor_mz - lower_offset < target_mzs[i] < precursor_mz + upper_offset:
            im, ce, mzs, ints = _extract_im_ms2_msfragger(spectrum)
            exp_ims[i] = im
            exp_ces[i] = ce
            exp_mzs[i] = mzs
            exp_intensities[i] = ints
        else:
            print('Spectrum not matched. IDK what\'s going on here. Interesting.')

    exp_rts = np.array(exp_rts)
    exp_ims = np.array(exp_ims)
    exp_spectra = pd.DataFrame()
    exp_spectra['mzs'] = exp_mzs
    exp_spectra['intensities'] = exp_intensities
    exp_spectra['ce'] = exp_ces
    return exp_rts, exp_ims, exp_spectra