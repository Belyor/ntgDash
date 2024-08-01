from dash import callback, Input, Output, State
import json
import glob
import pandas as pd
import os

from collections import defaultdict

from math import pi
from pathlib import Path

DATA = 1  # 1: Test Data, 0: All NTG data
global col_results
global col_postprocess

col_results = ["Time", "Total Energy", "Number of Protons", "Number of Neutrons",
               "X_cm", "Y_cm", "Z_cm",
               "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
               "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
               "Beta", "Flow Energy", "Ground State Enrgy",
               "Quadrupole Moment Q20", "Octupole Moment Q30", "Hexadecupole Moment Q40",
               "Pairing gap for Protons", "Pairing gap for Neutrons", "Center of Mass Energy"]

col_postprocess = ["Time", "Total Energy", "Total Fermi Energy", "Total Fermi Energy 1st correction", "Total Fermi Energy with Pairing and 1st correction",
                   "Number of Protons", "Number of Neutrons",
                   "X_cm", "Y_cm", "Z_cm",
                   "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
                   "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
                   "Beta", "Flow Energy", "Quadrupole Moment Q20",
                   "Velocity in X_cm", "Velocity in Y_cm", "Velocity in Z_cm",
                   "Octupole Moment Q30", "Hexadecupole Moment Q40", "something", "Quadrupole Moment Q22",
                   "Triaxial X", "Triaxial Y", "Triaxial Z",
                   "Pairing gap for Neutrons", "Pairing gap for Protons", "Gradient of Delta for Protons", "Gradient of Delta for Neutrons",
                   "Coulomb Force", "Total Kinetic Energy", "Total Excitation Energy", "Distance"]

def fname_to_metadata(fname : str):
    fname_split = Path(fname).stem.split('_')

    # The most work is with phase, it will be convinient to have both
    # fractional string and numeric value
    phase_fraction = fname_split[5].replace('PIPhase', '').replace('-', '/')
    phase_split = phase_fraction.split('/')
    phase_val = float(phase_split[0]) * pi
    if len(phase_split) > 1:
        phase_val /= float(phase_split[1])

    md = {
        'filename'       : fname,
        'system'         : fname_split[0],
        'functional'     : fname_split[1],
        'b'              : float(fname_split[4].replace('b', '').replace('-', '.')),
        'phase_fraction' : phase_fraction,
        'phase_value'    : phase_val,
        'energy'         : int(fname_split[6].replace('MeV', '')),
    }

    return md

def register_filter_callback(metadata : pd.DataFrame, custom_filters):
    """
    Function registering a callback for files filter
    Args:
        metadata (DataFrame): Metadata returned from load_data() function
        custom_filters (list[dict]): Every entry contains 'label' and 'files'
    """

    @callback(
        Output('filtered_files', 'data'),
        Input('apply', 'n_clicks'),
        Input('URL-copy', 'n_clicks'),
        State('filter_set', 'value'),
        State('filter_system', 'value'),
        State('filter_method', 'value'),
        State('filter_functional', 'value'),
        State('filter_phase', 'value'),
        State('filter_ecms', 'value'),
        State('filter_b', 'value'),
    )
    def filter(n_clicks, n_clicks_url, custom_set, system, method, functional, phase, ecms, b):
        """
        Ta funkcja uruchamia się z każdym wcisnięciem przycisku "apply", następnie
        rozkłada nazwy plików na części tak aby sprawdzić czy dana wartość z pliku jest zgodna
        z wartosciami z filtrów

        Args:
            n_clicks (int): liczba kliknięć przycisku 'apply'
            system (list): lista wybranych systemów
            method (list): lista wybranych metod(akutalnie nie aktywana)
            functional (list): lista funkcjonałów
            phase (list): lista z minimalną i maksymalną wartością filtra fazy
            ecms (list): lista z minimalną i maksymalną wartością filtra energii
            b (list): lista z minimalną i maksymalną wartością filtra parametru b

        Returns:
            list: List of filtered files
        """

        mask = metadata['phase_value'].between(phase[0], phase[1]) \
            & metadata['b'].between(b[0], b[1]) \
            & metadata['energy'].between(ecms[0], ecms[1])

        if system:
            mask &= metadata['system'].isin(system) 

        if functional:
            mask &= metadata['functional'].isin(functional)

        if custom_set != 'All Data':
            for entry in custom_filters:
                if entry['label'] == custom_set:
                    mask &= metadata['filename'].isin(entry['files'])

        return metadata['filename'][mask]

def load_data():
    project_dir = os.path.join("TestData", "*.dat")
    if DATA == 0:
        project_dir = os.path.join("Data", "*.dat")

    files = sorted(glob.glob(project_dir, ))
    data = defaultdict(pd.DataFrame)

    for file in files:
        data_tmp = pd.read_csv(file, sep=",", names=col_postprocess)
        data_tmp["totalmass"] = data_tmp["Number of Protons"][1] * \
           938.272013 + data_tmp["Number of Neutrons"][1] * 939.565346
        data[file] = data_tmp

    metadata = pd.DataFrame([fname_to_metadata(file) for file in files])

    # Setup filters
    with open('./custom_filters.json') as file:
        custom_filters = json.load(file)
    register_filter_callback(metadata, custom_filters)
    return data, metadata
