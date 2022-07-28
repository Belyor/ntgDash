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
col_postprocess = ["time", "total_E", "total_E_TF", "total_E_TF_w-corr", "total_E_TF_w-corr_w-pair",
                   "N_p", "N_n",
                   "x_rcm", "y_rcm", "z_rcm",
                   "x_rcm_p", "y_rcm_p", "z_rcm_p",
                   "x_rcm_n", "y_rcm_n", "z_rcm_n",
                   "beta", "E_flow", "Q_20",
                   "vcm_x", "vcm_y", "vcm_z",
                   "Q_30", "Q_40", "something", "nonaxial_Q22",
                   "triax_x", "triax_y", "triax_z",
                   "av_Delta_n", "av_Delta_p", "delta_grad_p", "delta_grad_n",
                   "cf", "tke", "txe", "distance"]


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
