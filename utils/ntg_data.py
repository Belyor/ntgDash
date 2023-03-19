from collections import defaultdict
from dash import Dash, dcc, html, ctx, Input, Output, State
import glob
import pandas as pd
import os
from dash.exceptions import PreventUpdate

DATA = 1  # 1: Test Data, 0: All NTG data
global col_results
global col_postprocess
data_one=[]
data_two=[]
data_three=[]
data_four=[]
data_five=[]

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
    metadata=[]
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
        metadata.append([_system,_functional,_gp,_gn, _b,_phase,_ecm])
        data_tmp["totalmass"] = data_tmp["Number of Protons"][1] * \
           938.272013 + data_tmp["Number of Neutrons"][1] * 939.565346
        data[file] = data_tmp
    
    return data,metadata #_system, _ecm,_b,_functional
    
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
        _ecm1=[]
        _phase1=[]
        _functional1=[]
        _b1=[]
        _system1=[]
        if button == 0:
            raise PreventUpdate
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
            _phase =dns[5].split('PIPhase')[0].split("-")
            #print(_phase)
            #print(type(_phase))
            if _phase[0] == '0Phase':
                _phase=' '.join(map(str,_phase))
                #print(_phase)
               # print(type(_phase))
                _phase=_phase.replace('Phase','')
                _phase=float(_phase)
            else:
               # print(_phase)
               # print(type(_phase[0]))
                if _phase[0]=='':
                    _phase=0
                else:
                    _phase[0]=float(_phase[0])
                    _phase[1]=float(_phase[1])
                    #print(_phase[0])
                    _phase=_phase[0]/_phase[1] 
            _ecm = float(dns[6].split('MeV')[0])
            if ( _system == system[0]):
                #print("System condition filled")
                #print (_system)
                _system1.append(_system)
            if ( _functional == functional[0] ):
                #print("Functional condition filled")
                #print (_functional)
                _functional1.append(_functional)
            if ( b[0] <= _b <= b[1]):
                #print("Impact parameter condition filled")
                #print (_b)
                _b1.append(_b)

            if ( phase[0] <= _phase <= phase[1] ):
                #print("Phase condition filled")
                ##print(_phase)
                _phase1.append(_phase)
            if ( ecms[0] <= _ecm <= ecms[1] ):
                #print("Energy condition filled")
                #print(_ecm)
                _ecm1.append(_ecm)
                
        #print(_ecm1)
       # print(_b1)
       # print(_phase1)
       # print(_functional1)
       # print(_system1)
        tab3 = list(set(_ecm1)) #tablice z przefiltrowanymi wartościami
        tab4 = list(set(_b1))
        tab5 = list(set(_phase1))
        tab6 = list(set(_functional1))
        tab7 = list(set(_system1))
        #data_one=tab3
        #data_two=tab4
        #data_three=tab5
        #data_four=tab6
        #data_five=tab7
        #print(data_one)
        #print(tab3)
        #print(tab4)
        #print(tab5)
        #print(tab6)
        #print(tab7)
            #print(ecms[0])
            #print (system,method,functional,phase,ecms,b)
        return tab3, method,functional,phase #input_value,ip,im #print(input_value,ip,im)
    return #,data_two,data_three,data_four,data_five      
