# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 08:59:56 2018

@author: mjigmond
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta as td

xlsFile = 'target_tr.xlsx'
refDate = dt(1990, 4, 1)

xls = pd.read_excel(xlsFile, sheet_name='target', usecols=10)
targ = {}
for r in xls.values:
    if r[0].startswith('Residual'): break
    w = r[0].replace('/','-')
    targ.setdefault(w, [])
    targ[w].append((refDate+td(days=r[1]),r[5],r[6]))

for k, v in targ.items():
    dates, obs, sim = zip(*sorted(v))
    fig, ax = plt.subplots(figsize=(9,6.5))
    ax.set_title(k)
    ax.grid(ls=':')
    ax.plot(dates, obs, label='Measured', marker='o', ms=2.5)
    ax.plot(dates, sim, label='Simulated', ls='--')
    ax.set_xlim(refDate, dt(2018,1,1))
    rng = max(obs+sim) - min(obs+sim)
    if rng < 50:
        llim = min(obs+sim) - (50-rng)*.5
        ulim = max(obs+sim) + (50-rng)*.5
    else:
        llim = min(obs+sim)
        ulim = max(obs+sim)
    if k == 'DM80-2': print(llim, ulim)
    ax.set_ylim(llim, ulim)
    ax.set_ylabel('Water level [feet amsl]')
    ax.legend(loc='lower right')
    plt.savefig(r'hydrographs/{}.png'.format(k), dpi=300)
    plt.close()
