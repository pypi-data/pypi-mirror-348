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


""" Code to deal with ev/STARS/TWIN mdl files.
    2024-05-20, MvdS: initial version.
"""


import pandas as _pd
import sluyspy.cli as _scli
import fortranformat as _ff


def read_mdl(mdl_name, imdl, SI=True, verbosity=0):
    """Read an ev/STARS/TWIN .mdl[12] file containing stellar-structure models and return a Pandas
    DataFrame with a selected model.
    
    Args:
      mdl_name (str):   Name of the input .mdl? file.
      imdl (int):       Number of the desired structure model (>=1).
                        This is the sequence number in the file, not the original model number from the evolution code.
      SI (bool):        Convert cgs to SI units.  Optional, returns to True.
      verbosity (int):  Output verbosity (0-3).  Optional, defaults to 0 (silent).
    
    Returns:
      pandas.DataFrame:  Pandas DataFrame containing the stellar-structure data.
    """
    
    if verbosity>0:
        print('\nread_mdl():')
        print('Reading file: '+mdl_name)
    
    
    # Open the .mdl? file and read the first line:
    input_file = open(mdl_name,'r')
    line = input_file.readline()
    format_file_header = _ff.FortranRecordReader('(I6,I6,F7.3)')                        # Header format
    Nmesh, Nvar, mdlVer = format_file_header.read(line)
    if verbosity>1: print('Number of variables/columns: ', Nvar)
    
    
    # Determine the column variables, based on the number of columns:
    if Nvar==21:
        format_body   = _ff.FortranRecordReader('(E13.6, 4E11.4, 16E11.3)')
        
        col_names = ['m', 'r', 'p', 'rho', 't', 'kappa', 'Nad', 'Nad_Nrad', 'H', 'He', 'C', 'N', 'O', 'Ne', 
                     'Mg', 'l', 'Eth', 'Enuc', 'Enu', 'S', 'Uint']
        
    elif Nvar==27:
        format_body   = _ff.FortranRecordReader('(E13.6, 4E11.4, 22E11.3)')
        
        col_names = ['m', 'r', 'p', 'rho', 't', 'kappa', 'Nad', 'Nad_Nrad', 'H', 'He', 'C', 'N', 'O', 'Ne', 
                     'Mg', 'l', 'Eth', 'Enuc', 'Enu', 'S', 'Uint', 'Rpp', 'Rpc', 'Rpng', 'Rpn', 'Rpo', 'Ran']
        
    else:
        _scli.error('read_mdl(): unsupported number of columns for '+mdl_name+': '+str(Nvar))
    
    
    # Read all structure-model blocks until the desired model (imdl) is read:
    iblk = 0
    while iblk < imdl:
        df = _read_mdl_block(input_file, Nmesh, format_body, verbosity)
        iblk += 1
        
    df.columns = col_names
    
    if SI:
        df.p     *= 0.1   # dyn/cm^2 -> N/m^2
        df.rho   *= 1e3   # g/cm^3   -> kg/m^3
        df.kappa *= 0.1   # cm^2/g   -> m^2/kg
        df.Eth   *= 1e-4  # erg/s/g  -> W/kg
        df.Enuc  *= 1e-4  # erg/s/g  -> W/kg
        df.Enu   *= 1e-4  # erg/s/g  -> W/kg
        df.S     *= 1e-4  # erg/g/K  -> J/kg/K
        df.Uint  *= 1e-4  # erg/g    -> J/kg
    return df


def _read_mdl_block(input_file, Nmesh, format_body, verbosity):
    """Read a single stellar-structure block from an ev/STARS/TWIN .mdl[12] file.
    
    Parameters:
      input_file (str):      Name/path of the input file.
      Nmesh (int):           Number of mesh points in the model = rows in the file.
      format_body (float):   Fortran-format format string.
      verbosity (int):       Verbosity (0: quiet).
    
    Returns:  
      (pd.df):  Pandas.DataFrame containing a single stellar-structure model.
    """
    
    line = input_file.readline()
    format_block_header = _ff.FortranRecordReader('(I6,E17.9)')                        # Header format
    iMdl, age = format_block_header.read(line)
    if verbosity>1: print('Model number: %5i;  age: %10.3e' % (iMdl, age))
    
    iline = 0
    df = _pd.DataFrame()
    while iline<Nmesh:
        iline += 1
        line = input_file.readline()
        if line=='': break  # EoF
        
        arr = format_body.read(line)
        if iline==1:
            df = _pd.DataFrame([arr])
        else:
            df.loc[len(df.index)] = arr
        
    return df


if __name__ == '__main__':
    pass

