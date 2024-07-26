from dash import callback, Input, Output, State
import glob
import pandas as pd
import os
from dash.exceptions import PreventUpdate
from collections import defaultdict

from utils.ntg_util import fname_to_metadata

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

# FIXME: This returns data as dictionary, but some other function requires DataFrame (huh?)
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
    return data, metadata


def pipe_data(metadata : pd.DataFrame):
    """
    Funkcja do filtorwania danych, pobiera wartości wybrane przez użytkownika w aplikacji, zwraca
    listę z przefiltrywowanymi plikami, które są aktualizowane na wykresach

    Args:
        df (DataFrame):
    """
    
    @callback(
        Output('filter_system', 'value'),
        Input('filter_system', 'value')
    )
    def filter_system_cleanup(system):
        if 'All' in system:
            if system[-1] == 'All':
                return ['All']
            system.remove('All')
        return system

    @callback(
        Output('filter_functional', 'value'),
        Input('filter_functional', 'value')
    )
    def filter_functional_cleanup(functional):
        if 'All' in functional:
            if functional[-1] == 'All':
                return ['All']
            functional.remove('All')
        return functional

    @callback(
        Output('filtered_files', 'data'),
        Input('apply', 'n_clicks'),
        State('filter_system', 'value'),
        State('filter_method', 'value'),
        State('filter_functional', 'value'),
        State('filter_phase', 'value'),
        State('filter_ecms', 'value'),
        State('filter_b', 'value'),
    )
    def filter(n_clicks, system, method, functional, phase, ecms, b):
        """
        Ta funkcja uruchamia się z każdym wcisnięciem przycisku "apply", następnie
        rozkłada nazwy plików na części tak aby sprawdzić czy dana wartość z pliku jest zgodna
        z wartosciami z filtrów

        Args:
            button (int): liczba kliknięć przycisku 'apply'
            system (list): lista wybranych systemów
            method (list): lista wybranych metod(akutalnie nie aktywana)
            functional (list): lista funkcjonałów
            phase (list): lista z minimalną i maksymalną wartością filtra fazy
            ecms (list): lista z minimalną i maksymalną wartością filtra energii
            b (list): lista z minimalną i maksymalną wartością filtra parametru b

        Raises:
            PreventUpdate: Przciwdziała uruchomieniu przycisku przy uruchamianiu programu

        Returns:
            list: zwraca listę plików przefiltorwanych
        """
        if n_clicks == 0:
            raise PreventUpdate

        mask = metadata['phase_value'].between(phase[0], phase[1]) \
            & metadata['b'].between(b[0], b[1]) \
            & metadata['energy'].between(ecms[0], ecms[1])

        if system != ['All']:
            mask &= metadata['system'].isin(system) 

        if functional != ['All']:
            mask &= metadata['functional'].isin(functional)

        return metadata['filename'][mask]
