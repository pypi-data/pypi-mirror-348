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

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import argparse
from pathlib import Path, PosixPath

from omicron_utils.omicron_config import OmicronConfig

# these command line arguments came from debugger breakpoint in pyomicron running on Joe's
# home workstation

dummy_args_home = {'archive': False, 'auth_type': 'x509', 'cache_file': None,
              'conda_env': 'ligo-omicron-3.10',
              'condor_accounting_group': 'ligo.prod.o4.detchar.transient.omicron',
              'condor_accounting_group_user': 'areeda', 'condor_command': [],
              'condor_request_disk': '20G', 'condor_retry': 2,
              'config_file': '/Volumes/Data2/omicron/omicron/online/h1-channels.ini',
              'dagman_option': ['force', 'import_env'], 'exclude_channel': [],
              'executable': '/Users/areeda/miniforge3/envs/ligo-omicron-3.10-test/bin/omicron',
              'file_tag': 'PEM1', 'gps': None, 'group': 'PEM1', 'ifo': 'H1',
              'log_file': None, 'max_channels_per_job': 10, 'max_chunks_per_job': 4,
              'max_concurrent': 64, 'max_online_lookback': 43200, 'no_segdb': False,
              'no_submit': True, 'output_dir': PosixPath('/Users/areeda/t/omicron/online-h1'),
              'reattach': False, 'rescue': False, 'skip_gzip': False, 'skip_hdf5_merge': False,
              'skip_ligolw_add': False, 'skip_omicron': False, 'skip_postprocessing': False, 'skip_rm': False,
              'skip_root_merge': False, 'submit_rescue_dag': 0, 'universe': 'vanilla', 'use_dev_shm': False,
              'verbose': 5}


def test_getsubmit():
    '''
    Simulate using config file, command line arguments, etc. to generate the parameters for our submit file
    :return: assert results are produced tested at least a little
    '''
    args = argparse.Namespace(**dummy_args_home)
    config_path = OmicronConfig.get_default_config_path()
    assert config_path is not None
    home = str(Path.home().absolute())
    symbols = {'HOME': home}
    pro = ''

