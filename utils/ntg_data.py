from collections import defaultdict
from dash import Dash, dcc, html, ctx, Input, Output, State
import glob
import pandas as pd
import os
from dash.exceptions import PreventUpdate

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

#system = []
#emc = []

def load_data():
    project_dir = os.path.join("TestData", "*.dat")

    if DATA == 0:
        project_dir = os.path.join("Data", "*.dat")

    data_names = defaultdict(dict)

    files = sorted(glob.glob(project_dir, ))
    data = defaultdict(pd.DataFrame)
    for file in files:
        dns = file.split(os.sep)
        dns = dns[1].split("_")
        _system = dns[0] #system #dns[0] jako cały sytem  #system
        _functional = dns[1] 
        _gp = dns[2].split('gp')[1]
        _gn = dns[3].split('gn')[1]
        _b = dns[4].split('b')[1].replace('-', '.') # lista do każdego 
        _phase = dns[5].split('Phase')[0]
        _ecm = dns[6].split('MeV')[0]
        data_tmp = pd.read_csv(file, sep=",", names=col_postprocess)  # READ FILES

        data_tmp["totalmass"] = data_tmp["Number of Protons"][1] * \
           938.272013 + data_tmp["Number of Neutrons"][1] * 939.565346
        data[file] = data_tmp
    return _system, _ecm,_b,_functional

    
def pipe_data(app: Dash):
    @app.callback(
        Output(component_id='filter_system', component_property='value'),
        Output(component_id='filter_filter', component_property='value'),
        Output(component_id='filter_method', component_property='value'),
        Output(component_id='filter_phase', component_property='value'),
        Input(component_id='apply', component_property='n_clicks'),
        State(component_id='filter_system', component_property='value'),
        State(component_id='filter_method', component_property='value'),
        State(component_id='filter_filter', component_property='value'),
        State(component_id='filter_phase', component_property='value'),
        State(component_id='filter_ecms', component_property='value'),
        State(component_id='filter_D', component_property='value'),
    )
    def callback(button,system,method,functional,phase,ecms,b):
        #if ( df.dns[5] > phase[0] and df.dns[5] < phase[1] ):
        project_dir = os.path.join("TestData", "*.dat")
        if DATA == 0:
            project_dir = ""
        data_names = defaultdict(dict)
        files = sorted(glob.glob(project_dir, ))
        data = defaultdict(pd.DataFrame)
        for file in files:
            dns = file.split(os.sep)
            dns = dns[1].split("_")
            _system = dns[0]
            _functional = dns[1] 
            _b = float(dns[4].split('b')[1].replace('-', '.'))
            _phase = float(dns[5].split('PIPhase')[0].split("-"))
            if(len(_phase)==2):
                _phase=_phase[0]
            else:
                _phase=_phase[0]/_phase[1]
            _ecm = float(dns[6].split('MeV')[0])
            # data_tmp = pd.read_csv(file, sep=",", names=col_results)  # READ FILES
            # data_tmp["totalmass"] = data_tmp["Number of Protons"][1] * \
                # 938.272013 + data_tmp["Number of Neutrons"][1] * 939.565346
            # data[file] = data_tmp
            
            if ( _system == system):
                print("System condition filled")
            if ( _functional == functional ):
                print("Functional condition filled")
            if ( b[0] <= _b <= b[1]):
                print("Impact parameter condition filled")
            if ( phase[0] <= _phase <= phase[1] ):
                print("Phase condition filled")
            if ( ecms[0] <= _ecm <= ecms[1] ):
                print("Energy condition filled")
                
        if button == 0:
            raise PreventUpdate
            return system,method,functional,phase 
        else: 
            print(ecms[0])
            print (system,method,functional,phase,ecms,b)
            return system,method,functional,phase #input_value,ip,im #print(input_value,ip,im)