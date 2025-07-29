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

from omicron_utils.conda_fns import get_conda_run
from omicron_utils.omicron_config import OmicronConfig


def test_config():
    """
    Omicron control program configration, not the Omcrong trigger generator's config
    :return: None
    """
    omicron_config = OmicronConfig()
    assert omicron_config is not None

    config = omicron_config.get_config(save_if_none=False)
    getenv = config['condor']['getenv']
    assert getenv is not None
    pass


def test_get_conda_run():
    """
    try to get conda prefix
    :return: None
    """
    omicron_config = OmicronConfig()
    assert omicron_config is not None

    config = omicron_config.get_config(save_if_none=False)

    env1 = 'ligo-omicron-3.10'
    prefix = get_conda_run(config, env1)
    assert prefix is not None
    pass
