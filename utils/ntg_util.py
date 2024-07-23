from math import pi

from pathlib import Path

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
