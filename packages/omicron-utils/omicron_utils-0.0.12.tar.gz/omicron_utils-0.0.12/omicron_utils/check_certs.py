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

import os
import shutil
import subprocess
from pathlib import Path


def check_certs(logger):
    """
    Verify current Kerberos, x509 and scitokens, warn if not
    I think it/s best to report missing but let the programs fail.
    :param logging.Logger logger:
    :return bool: TRUE if all checks pass
    """
    x509 = Path.home() / '.private' / 'x509p.pem'
    x509_str = os.getenv('X509_USER_PROXY')
    x509 = Path(x509_str) if x509_str is not None and len(x509_str) > 2 else x509
    if x509.exists():
        os.putenv('X509_USER_PROXY', str(x509.absolute()))
        logger.debug(f'Set environment X509_USER_PROXY={str(x509.absolute())}')
    else:
        logger.error(f'x509 not found at {str(x509.absolute())}')

    eci = shutil.which('ecp-cert-info')
    if eci is None:
        logger.error('Program ecp-cert-info not found')
    else:
        res = subprocess.run([eci], capture_output=True)
        stdout = res.stdout.decode('utf-8')
        stderr = res.stderr.decode('utf-8')
        logger.debug(f'ecp-cert-info returned {res.returncode}\n{stdout}\n{stderr}')
