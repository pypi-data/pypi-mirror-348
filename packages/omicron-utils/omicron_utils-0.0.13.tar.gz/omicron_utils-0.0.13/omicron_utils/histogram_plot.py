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

import logging
from math import sqrt

import numpy as np
from matplotlib import use, pyplot
use('agg')


def histogram_plot(data, outfile, suptitle='', title='', xscale=None, bins=None, logger=None):
    """

    :param data:
    :param outfile:
    :param suptitle:
    :param title:
    :param xscale:
    :param bins:
    :param logger:
    :return:
    """

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger('histogram_plot')
        logger.setLevel(logging.CRITICAL)

    # plot histogram
    pyplot.figure(figsize=(24, 15))
    xmin = data.min()
    xmax = data.max()
    if xscale:
        if '%' in xscale:
            pct = float(xscale.replace('%', ''))
            plt_xmax = np.percentile(data, pct)
        else:
            plt_xmax = float(xscale)
    else:
        plt_xmax = xmax
    logger.info(f'Plot max: {plt_xmax:.1f}')
    new_data = data[data <= plt_xmax]
    nbins = bins if bins else int(max(10, round(sqrt(len(new_data)))))
    logger.info(f'nbins: {nbins}')
    pyplot.hist(new_data, nbins)

    ax = pyplot.gca()
    if suptitle:
        pyplot.suptitle(suptitle)
    if title:
        ax.set_title(title, fontsize=10, y=.97)
    ax.set_xlabel('Time (s) last gps to file write')
    ax.set_ylabel('N')

    ax.set_xlim(xmin, plt_xmax)
    pyplot.savefig(outfile)
    logger.info(f'Saved histogram as: {str(outfile.absolute())}')

    return outfile
