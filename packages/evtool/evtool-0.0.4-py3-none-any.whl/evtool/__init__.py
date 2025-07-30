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


"""evTool package

Analyse and display output from the binary stellar-evolution code ev (a.k.a. STARS or TWIN).

The code is being developed by `Marc van der Sluys <http://marc.vandersluys.nl>`_ of the Department of Physics
at Utrecht University in the Netherlands, and the Netherlands Institute of Nuclear and High-Energy Physics
(Nikhef) in Amsterdam.  The evTool package can be used under the conditions of the EUPL 1.2 licence.  These
pages contain the API documentation.  For more information on the Python package, licence and source code, see
the `evTool GitHub page <https://github.com/MarcvdSluys/evTool>`_.

"""


name = 'evtool'
__author__ = 'Marc van der Sluys - Nikhef/Utrecht University - marc.vandersluys.nl'

from .plt      import *
from .mdl      import *
