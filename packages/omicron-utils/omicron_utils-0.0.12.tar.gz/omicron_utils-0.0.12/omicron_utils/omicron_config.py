#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2024 Joseph Areeda <joseph.areeda@ligo.org>
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
""""""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import configparser
import logging
import os
import re
import sys
from pathlib import Path


class OmicronConfig:
    """
    Representing the configuration of all LSC Omicron programs in one place.
    The hierarchy of where to get the information. First one of ther list found.
    1. File path passed in creation or in set_file method
    2. Environment variable OMICRON_CONFIG
    3.
    4. Internal defaults. See ligoomicron.ini in this project.

    Our philosophy is to put as many options as we can into the configuration.
    """

    @staticmethod
    def get_default_config_path():
        """
        Standardize where we look for our config file if not specified
        :return str: absolute path to config file
        """
        default_path = Path.home() / '.ligo_omicron.ini'
        return str(default_path.absolute())

    @staticmethod
    def get_internal_config_path():
        """
        The internal config file is our best guess for default values at release thime
        :return str: absolute path to config file
        """
        me = Path(__file__)
        mydir = me.parent
        path = mydir / 'ligoomicron.ini'
        return str(path.absolute())

    def __init__(self, path=None, logger=None):
        """

        :param Path|str|None path: path to configuration file
        :param logging.Logger logger: program logger
        """
        self.config = None
        if logger is None:
            # global logger
            log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
            log_file_date_format = '%m-%d %H:%M:%S'
            logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
            self.logger = logging.getLogger('OmicronConfig')
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger
        if path is None:
            self.path = self.get_default_config_path()
        else:
            self.path = Path(path)
            self.set_file(path)

    def set_file(self, path):
        """
        Read the configuration file replacing any existing values
        :param Path|str path: path to configuration file
        :return configparser.ConfigParser: copy of the config
        """
        if path is None or not Path(path).is_file() or not Path(path).exists():
            raise FileNotFoundError(f'{path} does not exist')
        self.path = Path(path)
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.logger.debug(f'Configuration read from {self.path.absolute()}')
        return self.config

    def get_config(self, save_if_none=True):
        """
        The preferred way to get current configuration. This method looks through list of places we can use
        for configuration file
        :param bool save_if_none: if we don't have confi in home add it
        :return configparser.ConfigParser:

        """
        default_path = Path(OmicronConfig.get_default_config_path())
        if self.config is None:
            path = os.getenv('OMICRON_CONFIG', None)
            if path is None:
                path = default_path
            if path is None or not path.exists():
                path = OmicronConfig.get_internal_config_path()
            path = Path(path)
            self.logger.debug(f'Read config file {path.absolute()}')

            if path.exists():
                config = configparser.ConfigParser()
                config.read(path)
                self.config = config
                self.path = path
                # remove line breaks from  continuation lines
                for section in self.config.sections():
                    for option in self.config.options(section):
                        new_option = config[section][option]
                        new_option_lst = [item for item in new_option.strip().split('\n')]
                        new_option = str(" ".join(new_option_lst))
                        new_option = new_option.replace('\\', '')
                        self.config[section][option] = str(new_option)

                if not default_path.exists() and save_if_none:
                    with default_path.open('w') as cfp:
                        self.config.write(cfp)
            else:
                raise FileNotFoundError('No configuration file found')
        return self.config

    def print_config(self, out=None):
        """
        pretty print the current configuration
        :param str | Path | None out: output file path, None for stdout
        :return: None
        """
        try:
            if out is None:
                print(f'Omicron configuraton in file: {self.path.absolute()}\n')
                self.config.write(sys.stdout)
            else:
                with Path(out) as fp:
                    self.config.write(fp)
        except (TypeError, FileNotFoundError, IOError, IsADirectoryError, OSError) as e:
            self.logger.error(f'Error while printing configuration: {e}')

    def get_option(self, section, option):
        """
        Return an option in the configuration we have read handling multi-line
        :param str section: section name
        :param str option: option name
        :return str: option value
        """
        ret = self.config.get(section, option)
        ret = ret.strip()
        ret = re.sub('\\s+', ' ', ret)
        return ret
