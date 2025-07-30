#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2025 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
A class to combine parameter from different sources to create a
"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

class OmicronCondorJob:
    """"
    This class will use multiple sources to generate statements for condor submit files.
    The order of sources is important.
    1. The [condor] section of the config file
    2. The [<program>] section of the config file
    3. Specific command line arguments

    Variable substitution syntax %{<variable name>}. It uses the environment variables ad a user supplied dictionary
    the user dict will take precedence if duplicates exist.
    """

    def __init__(self, config, program, args=None, symbols=None):
        """

        :param  configparser.ConfigParser config: The ligo_omicron config (not the omicron channel config)
        :param str program: program name as used for config section
        :param namespace args: argparser args
        :param dict[str, str] symbols: symbol table used in substitutions
        """
        self.config = config
        self.program = program
        self.args = vars(args) if args else dict()
        self.symbols = symbols if symbols is not None else dict()

    def get_classads(self):
        """
        Combine the layers of inputs to produce
        :return dict[str, str]: The Classad
        """