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

""""""

import time

from omicron_utils.TerminalFormat import ansi_color_text
from omicron_utils.omicron_config import OmicronConfig

start_time = time.time()

import argparse
import logging
from pathlib import Path
import sys
import traceback

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None


def parser_add_args(parser):
    """
    Set up command parser
    :param argparse.ArgumentParser parser:
    :return: None but parser object is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('--config', type=Path, help='path to config file')
    parser.add_argument('command', type=str, help='command to run',
                        choices=['write', 'merge', 'diff', 'print'])

    epilog =\
        f"""
        By default, most LIGO omicron process get their parameters from a configuration file. We are still working
        to move any internal defaults to the config file. The hierarchy of parameter is 1) The internal defaults,
        2) the external config file by default {OmicronConfig.get_default_config_path()} or specified as acommand
        line argument 3) any relevant command line arguments.

        This program is meant to aid in maintaining the external config file as we update the programs,
        adding options and changing defaults.
        """
    parser.epilog = epilog


def internal_color(string):
    """
    Adds terminal control codes to idenntify string as belonging to internal (default) config
    :param str string: string to colorize
    :return str: colorized string
    We currentl use blue text on black background
    """
    ret = ansi_color_text(string, 'blue', 'black', True)
    return ret


def external_color(string):
    """
    Adds terminal control codes to idenntify string as belonging to external (Editable) config
    :param str string: string to colorize
    :return str: colorized string
    We currentl use green text on black background
    """
    ret = ansi_color_text(string, 'green', 'black', True)
    return ret


def show_diff(internal_config, current_config):
    """
    Display difference between internal and external configurations
    :param OmicronConfig internal_config: our defaults
    :param  OmicronConfig current_config: external config usually the default one
    :return bool: True if objects are different
    """
    print(f'Comparing {internal_color("Internal defaults")} with {external_color(current_config.path)}')
    internal_sections = list(internal_config.config.sections())
    internal_sections.sort()
    external_sections = list(current_config.config.sections())
    external_sections.sort()
    common_sections = list(set(internal_sections).intersection(external_sections))
    internal_only_sections = list(set(internal_sections) - set(common_sections))
    external_only_sections = list(set(external_sections) - set(common_sections))
    if internal_only_sections:
        for section in internal_only_sections:
            print(f'{internal_color(section)} only in internal config')
    if external_only_sections:
        for section in external_only_sections:
            print(f'{external_color(section)} only in external config')

    for section in common_sections:
        internal_options = list(internal_config.config.options(section))
        internal_options.sort()
        external_options = list(current_config.config.options(section))
        external_options.sort()

        internal_only_options = list(set(internal_options) - set(external_options))
        external_only_options = list(set(external_options) - set(internal_options))
        common_options = list(set(internal_options).intersection(external_options))

        if internal_only_options:
            print(f'Section {section} has these options in internal config only:')
            for opt in internal_only_options:
                opt_txt = f'   {opt} = {internal_config.get_option(section, opt)}'
                print(internal_color(opt_txt))

        if external_only_options:
            print(f'Section {section} has these options in external config only:')
            for opt in external_only_options:
                opt_txt = f'   {opt} = {current_config.get_option(section, opt)}'
                print(external_color(opt_txt))

        need_section_title = True
        for opt in common_options:
            internal_value = internal_config.get_option(section, opt)
            current_value = current_config.get_option(section, opt)
            if internal_value != current_value:
                if need_section_title:
                    need_section_title = False
                    print(f'Section {section} has differences in these options:')
                current_text = f'  file:       {opt} = {current_value}'
                internal_text = f' internal:   {opt} = {internal_value}'
                print(f'{internal_color(internal_text)}')
                print(f'{external_color(current_text)}')

        if not need_section_title:
            print('---')


def main():
    global logger

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_add_args(parser)
    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    internal_config_path = Path(OmicronConfig.get_internal_config_path())
    if internal_config_path is None or not internal_config_path.exists():
        raise FileNotFoundError(f'The internal (default) configuration file {internal_config_path} does not exist')

    if args.config:
        current_config_path = Path(args.config)
        if not current_config_path.exists():
            raise FileNotFoundError(f'Specified configuration: {current_config_path} does not exist')
    else:
        current_config_path = Path(OmicronConfig.get_default_config_path())
        if not current_config_path.exists():
            logger.critical(f'Current configuration: {current_config_path} does not exist, it will be created with '
                            f'default values')
    if current_config_path.exists():
        current_config = OmicronConfig(current_config_path, logger=logger)
    else:
        current_config = OmicronConfig(logger=logger)
    current_config.get_config(save_if_none=True)

    internal_config = OmicronConfig(internal_config_path, logger=logger)
    internal_config.get_config(save_if_none=False)

    if not current_config_path.exists():
        logger.critical(f'Specified configuration: {current_config_path} still does not exist')
    else:
        current_config = OmicronConfig(current_config_path, logger=logger)
        current_config.get_config(save_if_none=False)

        if args.command.lower() == 'print':
            current_config.print_config()
        elif args.command.lower() == 'merge':
            pass
        elif args.command.lower() == 'diff':
            show_diff(internal_config, current_config)
        else:
            pass


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
