from collections import defaultdict
import glob
import pandas as pd
import os

DATA = 1  # 1: Test Data, 0: All NTG data
col_results = ["Time", "Total Energy", "Number of Protons", "Number of Neutrons",
               "X_cm", "Y_cm", "Z_cm",
               "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
               "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
               "Beta", "Flow Energy", "Ground State Enrgy",
               "Quadrupole Moment Q20", "Octupole Moment Q30", "Hexadecupole Moment Q40",
               "Pairing gap for Protons", "Pairing gap for  Neutrons", "Center of Mass Energy"]
col_postprocess = ["time", "Total Energy", "Total Fermi Energy", "Total Fermi Energy 1st correction", "Total Fermi Energy with Pairing and 1st correction",
                   "Number of Protons", "Number of Neutrons",
                   "X_cm of the System", "Y_cm of the System", "Z_cm of the System",
                   "X_cm for Protons", "Y_cm for Protons", "Z_cm for Protons",
                   "X_cm for Neutrons", "Y_cm for Neutrons", "Z_cm for Neutrons",
                   "Beta", "Flow Energy", "Quadrupole Moment Q20",
                   "Velocity in X_cm", "Velocity in Y_cm", "Velocity in Z_cm",
                   "Octupole Moment Q30", "Hexadecupole Moment Q40", "something", "Quadrupole Moment Q22",
                   "Triaxial X", "Triaxial Y", "Triaxial Z",
                   "Pairing gap for Neutrons", "Pairing gap for Protons", "Gradient of Delta for Protons", "Gradient of Delta for Neutrons",
                   "Coulomb Force", "Total Kinetic Energy", "Total Excitation Energy", "CM Distance"]


def load_data():
    project_dir = os.path.join("TestData", "*.dat")

    if DATA == 0:
        project_dir = ""

    data_names = defaultdict(dict)

    files = sorted(glob.glob(project_dir, ))
    data = defaultdict(pd.DataFrame)
    for file in files:
        dns = file.split(os.sep)
        dns = dns[1].split("_")
        data_names[file]['Lnuclei'] = dns[0].split('+')[0]
        data_names[file]['Rnuclei'] = dns[0].split('+')[1]
        data_names[file]['functional'] = dns[1]
        data_names[file]['gp'] = dns[2].split('gp')[1]
        data_names[file]['gn'] = dns[3].split('gn')[1]
        data_names[file]['b'] = dns[4].split('b')[1].replace('-', '.')
        data_names[file]['phase'] = dns[5].split('Phase')[0]
        data_names[file]['ecm'] = dns[6].split('MeV')[0]
        data_tmp = pd.read_csv(file, sep=",", names=col_results)  # READ FILES
        data_tmp["totalmass"] = data_tmp["Number of Protons"][1] * \
            938.272013 + data_tmp["Number of Neutrons"][1] * 939.565346
        data[file] = data_tmp
    return data
