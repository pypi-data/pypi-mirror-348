# -*- coding: utf-8 -*-
# SPDX-License-Identifier: EUPL-1.2
#  
#  Copyright (c) 2024  Marc van der Sluys - Nikhef/Utrecht University - marc.vandersluys.nl
#  
#  This file is part of the evTool Python package:
#  Analyse and display output from the binary stellar-evolution code ev (a.k.a. STARS or TWIN).
#  See: https://github.com/MarcvdSluys/evTool
#  
#  This is free software: you can redistribute it and/or modify it under the terms of the European Union
#  Public Licence 1.2 (EUPL 1.2).  This software is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE.  See the EU Public Licence for more details.  You should have received a copy of the European
#  Union Public Licence along with this code.  If not, see <https://www.eupl.eu/1.2/en/>.


""" Code to deal with ev/STARS/TWIN plt files.
    2023-09-08, MvdS: initial version.
"""


import pandas as _pd
import sluyspy.cli as _scli


def read_plt(plt_name, verbosity=0):
    """Read an ev/STARS/TWIN .plt[12] file containing global/stellar-evolution variables and return a Pandas
    DataFrame.
    
    Args:
      plt_name (str):   Name of the input .plt? file.
      verbosity (int):  Output verbosity (0-3).  Optional, defaults to 0 (silent).
    
    Returns:
      pandas.DataFrame:  Pandas DataFrame containing the stellar-evolution data.
    
    """
    
    if verbosity>0:
        print('\nread_plt():')
        print('Reading file: '+plt_name)
        
    input_file = open(plt_name,'r')
    
    import fortranformat as ff
    format_header = ff.FortranRecordReader('(I4)')                        # Header format
    # format_body   = ff.FortranRecordReader('(I6,E17.9,E14.6,20E13.5)')  # Body format 1+1+1+84=87 columns
    
    line = input_file.readline()
    ncols = format_header.read(line)[0]
    if verbosity>1: print('Number of columns: ', ncols)
    
    if ncols==81:
        format_body   = ff.FortranRecordReader('(I6,E17.9,E14.6, 11F9.5, 7E12.4, 3F9.5, 16E12.4, F8.4, 21E13.5, 18F9.5, E14.6)')  # Body format 81 columns (2003)
        
        col_names = ['nr','age','dt','M','MHe','MCO','MONe','logR','logL','logTeff','logTc','logTmax',
                     'logrhoc','logrhoTmax','Ubind','LH','LHe','LC','Lnu','Lth','Prot','VK2','Rcz','dRcz',
                     'TET','RAF','BP','Porb','FLR','F1','dM_dt','dMwind_dt','dMmt_dt','Horb','dHorb_dt',
                     'dHgw_dt','dHwi_dt','dHso_dt','dHml_dt','Mcomp','e','H_srf','He_srf','C_srf','N_srf',
                     'O_srf','Ne_srf','Mg_srf','H_tmax','He_tmax','C_tmax','N_tmax','O_tmax','Ne_tmax',
                     'Mg_tmax','H_ctr','He_ctr','C_ctr','N_ctr','O_ctr','Ne_ctr','Mg_ctr','mcb_1s','mcb_1e',
                     'mcb_2s','mcb_2e','mcb_3s','mcb_3e','msb_1s','msb_1e','msb_2s','msb_2e','msb_3s','msb_3e',
                     'nuc_1s','nuc_1e','nuc_2s','nuc_2e','nuc_3s','nuc_3e','Qconv']
        
    elif ncols==87:
        # format_body = ff.FortranRecordReader('(I6,E17.9,E14.6, 12E13.5, 7E12.4, 3E13.5, 16E12.4, 37E13.5, I2, 4E13.5)')  # Body format 87 columns (2005?)
        format_body   = ff.FortranRecordReader('(I6,E17.9,E14.6, 12E13.5, 7E12.4, 3E13.5, 16E12.4, 39E13.5, E14.6,E13.5, I2, 4ES13.5)')  # Body format 87 columns (2005?)
        
        col_names = ['nr','age','dt','M','MHe','MCO','MONe','logR','logL','logTeff','logTc','logTmax',
                     'logrhoc','logrhoTmax','Ubind','LH','LHe','LC','Lnu','Lth','Prot','VK2','Rcz','dRcz',
                     'TET','RAF','BP','Porb','FLR','F1','dM_dt','dMwind_dt','dMmt_dt','Horb','dHorb_dt',
                     'dHgw_dt','dHwi_dt','dHso_dt','dHml_dt','Mcomp','e','H_srf','He_srf','C_srf','N_srf',
                     'O_srf','Ne_srf','Mg_srf','H_tmax','He_tmax','C_tmax','N_tmax','O_tmax','Ne_tmax',
                     'Mg_tmax','H_ctr','He_ctr','C_ctr','N_ctr','O_ctr','Ne_ctr','Mg_ctr','mcb_1s','mcb_1e',
                     'mcb_2s','mcb_2e','mcb_3s','mcb_3e','msb_1s','msb_1e','msb_2s','msb_2e','msb_3s','msb_3e',
                     'nuc_1s','nuc_1e','nuc_2s','nuc_2e','nuc_3s','nuc_3e','Qconv','Pc','strmdl','BE0','BE1',
                     'BE2','BE3']  # for 89-column version, add - 'Sc','ST1e5K' ?
        
    elif ncols==92:
        format_body   = ff.FortranRecordReader('(I6,E17.9,E14.6, 12E13.5, 7E12.4, 3E13.5, 16E12.4, 39E13.5, E14.6,E13.5,E14.6, 8E13.5,F5.1)')    # Body format 92 columns (MvdS git, 2023)
        
        col_names = ['nr','age','dt','M','MHe','MCO','MONe','logR','logL','logTeff','logTc','logTmax',
                     'logrhoc','logrhoTmax','Ubind','LH','LHe','LC','Lnu','Lth','Prot','VK2','Rcz','dRcz',
                     'TET','RAF','BP','Porb','FLR','F1','dM_dt','dMwind_dt','dMmt_dt','Horb','dHorb_dt',
                     'dHgw_dt','dHwi_dt','dHso_dt','dHml_dt','Mcomp','e','H_srf','He_srf','C_srf','N_srf',
                     'O_srf','Ne_srf','Mg_srf','H_tmax','He_tmax','C_tmax','N_tmax','O_tmax','Ne_tmax',
                     'Mg_tmax','H_ctr','He_ctr','C_ctr','N_ctr','O_ctr','Ne_ctr','Mg_ctr','mcb_1s','mcb_1e',
                     'mcb_2s','mcb_2e','mcb_3s','mcb_3e','msb_1s','msb_1e','msb_2s','msb_2e','msb_3s','msb_3e',
                     'nuc_1s','nuc_1e','nuc_2s','nuc_2e','nuc_3s','nuc_3e','Qconv','Pc','Protc','BE0','BE1',
                     'BE2','BE3','Sc','ST1e5K','RHe','RCO','strmdl']
        
    else:
        _scli.error('read_plt(): unsupported number of columns for '+plt_name+': '+str(ncols))
        
    
    iline = 0
    df = _pd.DataFrame()
    while True:
        iline += 1
        line = input_file.readline()
        # print(iline, line)
        if line=='': break  # EoF
        
        arr = format_body.read(line)
        if iline==1:
            df = _pd.DataFrame([arr])
        else:
            df.loc[len(df.index)] = arr
        
    df.columns = col_names
    
    return df


if __name__ == '__main__':
    pass

