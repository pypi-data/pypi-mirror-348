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
"""
Set of functions supporting use of conda
"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import logging
import re
import shutil
import subprocess
from os import getenv

PREFIX_SEARCH_LIST = [
    '${home}/.conda/envs/ligo-summary-3.10',
    '${home}/.conda/envs/ligo-summary-3.10-test',
    '/cvmfs/software.igwn.org/conda/envs/igwn',
    '${home}/mambaforge/envs/ligo-omicron-3.10',
    '${home}/mambaforge/envs/ligo-omicron-3.10-test',
    ''
]


def get_conda_run(config, env=None, logger=None):
    """
    Determine what is needed to run a command in the specified conda environment
    :param configparser.ConfigParser config: our pipeline configuration
    :param str env: cona env name or path
    :param logging.Logger logger:
    :return str, str: path to executable, run arguments
    """

    if logger is None:
        logger = logging.getLogger('get_conda_run')
        logger.setLevel(logging.INFO)

    executable = shutil.which('conda')
    if executable is None:
        executable = shutil.which('mamba')

    ermsg = 'conda program not found' if executable is None else ''

    if env is None:
        env = getenv('CONDA_PREFIX')

    if env is None and config.has_option('conda', 'environment'):
        env = config['conda']['environment']

    if env is None:
        ermsg += 'Unable to determine conda environment for Omicron pipeline'

    if ermsg:
        raise ValueError(ermsg)

    arguments = 'run '
    if '/' in env:
        # assume we have a path
        arguments += f'--prefix {env} '
    else:
        prefix = conda_name_to_prefix(env)
        if prefix is None:
            raise ValueError(f'Unable to find conda prefix for {env}')
        arguments += f'--prefix {prefix} '

    arguments += '--no-capture-output '

    return executable, arguments


def conda_name_to_prefix(conda_name: str, or_current=True) -> str:
    """
    Find the prefix of a conda environment from its name or current environment
    :param str conda_name: conda environment name
    :param bool or_current: if True, return current conda environment if set
    :return str: prefix of conda environment

    :param conda_name:
    :return:
    """
    conda = shutil.which('conda')
    if conda is None:
        conda = shutil.which('mamba')
    if conda is None:
        raise ValueError('Unable to find conda executable')

    cmd = [conda, 'info', '--envs']
    res = subprocess.run(cmd, capture_output=True)

    ret = None

    env_match = re.compile('(\\S+)([\\s\\*]+)(.*)$')
    for line in res.stdout.decode('utf-8').splitlines():
        m = env_match.match(line)
        if m:
            name = m.group(1)
            star = m.group(2)
            prefix = m.group(3)
            if star.find('*') >= 0 and or_current:
                ret = prefix
                break
            elif name == conda_name:
                ret = prefix
                break
            elif prefix.find(conda_name) >= 0:
                ret = prefix

    return ret
