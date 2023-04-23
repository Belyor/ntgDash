from collections import defaultdict
from dash import Dash, Input, Output, State
import glob
import pandas as pd
import os
from dash.exceptions import PreventUpdate

DATA = 1  # 1: Test Data, 0: All NTG data
global col_results
global col_postprocess
PI=3.14

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

def load_data():
    project_dir = os.path.join("TestData", "*.dat")
    metadata=[]
    if DATA == 0:
        project_dir = os.path.join("Data", "*.dat")
    data_names = defaultdict(dict)
    files = sorted(glob.glob(project_dir, ))
    data = defaultdict(pd.DataFrame)
    for file in files:
        dns = file.split(os.sep)
        dns = dns[1].split("_")
        _system = dns[0] 
        _functional = dns[1] 
        _gp = dns[2].split('gp')[1]
        _gn = dns[3].split('gn')[1]
        _b = dns[4].split('b')[1].replace('-', '.') 
        _phase = dns[5].split('Phase')[0]
        _ecm = dns[6].split('MeV')[0]
        data_tmp = pd.read_csv(file, sep=",", names=col_postprocess)  
        metadata.append([_system,_functional,_gp,_gn, _b,_phase,_ecm])
        data_tmp["totalmass"] = data_tmp["Number of Protons"][1] * \
           938.272013 + data_tmp["Number of Neutrons"][1] * 939.565346
        data[file] = data_tmp
    
    return data,metadata 
    
    
def pipe_data(app: Dash, df):
    """Funkcja do filtorwania danych, pobiera wartości wybrane przez użytkownika w aplikacji, zwraca
      listę z przefiltrywowanymi plikami, które są aktualizowane na wykresach 
    Args:
        app (Dash):
        df (DataFrame): 
    """
    @app.callback(
        Output(component_id='files_out', component_property='options'),
        Input(component_id='apply', component_property='n_clicks'),
        State(component_id='filter_system', component_property='value'),
        State(component_id='filter_method', component_property='value'),
        State(component_id='filter_filter', component_property='value'),
        State(component_id='filter_phase', component_property='value'),
        State(component_id='filter_ecms', component_property='value'),
        State(component_id='filter_D', component_property='value'),
    )
    def callback(button,system,method,functional,phase,ecms,b):
        """Ta funkcja uruchamia się z każdym wcisnięciem przycisku "applay", następnie 
        rozkłada nazwy plików na części tak aby sprawdzić czy dana wartość z pliku jest zgodna 
        z wartosciami z filtrów

        Args:
            button (int): liczba kliknięć przycisku 'applay'
            system (list): lista wybranych systemów 
            method (list): lista wybranych metod(akutalnie nie aktywana)
            functional (list): lista functionali
            phase (list): lista z minimalną i maksymalną wartością filtra fazy
            ecms (list): lista z minimalną i maksymalną wartością filtra energii
            b (list): lista z minimalną i maksymalną wartością filtra prametru b

        Raises:
            PreventUpdate: Przciwdziała uruchiniemu przycisku przy uruchamianu programu

        Returns:
            list: zwraca listę plików przefiltorwanych
        """
        _ecms=[]
        _phase=[]
        _functional=[]
        _b=[]
        _system=[]
        tab=[]
        dns=[]
        files_all=[]
        files_filtred=[]
        if button == 0:
            raise PreventUpdate
        for key in df.keys():
            tab.append(key)    
        for i in range(len(tab)):
            dns.append(tab[i].split("_"))
            _system.append(dns[i][0].replace('TestData\\', ''))
            _functional.append(dns[i][1])
            _b.append(float(dns[i][4].split('b')[1].replace('-', '.')))
            _phase.append((dns[i][5].replace('PIPhase', '')))
            _ecms.append(float(dns[i][6].replace('MeV','')))
        for k in range(len(_phase)):
            if( len(_phase[k])> 1):
                 _phase[k]=float(_phase[k][0])/float(_phase[k][2])
            else:
                _phase[k]=float( _phase[k])
        for i in range(len(tab)):
             if ( _system[i] not in system):
                continue
             if ( _functional[i] not in functional ):
                continue
             if ( _b[i]< b[0] or _b[i]>b[1] ):
                continue
             if ( _phase[i]<phase[0]/PI or _phase[i]>phase[1]/PI):
                continue
             if ( _ecms[i] < ecms[0] or _ecms[i] > ecms[1] ):
                continue
             files_all.append(i)
        for t in files_all:
             files_filtred.append(tab[t])
        return files_filtred   
