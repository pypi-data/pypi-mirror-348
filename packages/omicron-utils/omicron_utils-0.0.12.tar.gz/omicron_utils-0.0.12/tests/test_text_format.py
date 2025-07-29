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

from omicron_utils.TerminalFormat import format_str, ansi_color_text


def test_format():
    bold = format_str('bold', "bold")
    print(f'\nThis is {bold} text')
    print(f'This is {format_str("reverse", "reverse")} text')


def test_format_color():
    print()
    print(f'Thus is {ansi_color_text("yellow", "yellow")} text')
    print(f'Thus is {ansi_color_text("red", "red")} text')
    print(f'Thus is {ansi_color_text("green", "green")} text')
    print(f'Thus is {ansi_color_text("blue", "blue")} text')
    print(f'Thus is {ansi_color_text("white", "white")} text')
    print(f'Thus is {ansi_color_text("black", "black", "red")} text on red background')
    print(f'Thus is {ansi_color_text("black", "black", "green")} text on green background')
    print(f'Thus is {ansi_color_text("black", "black", "blue")} text on blue background')
    print(f'Thus is {ansi_color_text("black", "black", "yellow")} text on yellow background')
    print(f'Thus is {ansi_color_text("black", "black", "white")} text on white background')
    print(f'Thus is {ansi_color_text("white", "white", "black")} text on black background')
    print(f'This is {ansi_color_text("purple", 0xFF00FF)} text')
    print(f'This is {ansi_color_text("red", 0xFF0000)} text')
    print(f'This is {ansi_color_text("red", 0xFF0000, 0xFFFFFF)} text on white background')
