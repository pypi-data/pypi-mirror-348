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
Class to facilitate using ANSI terminal formatting codes
"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

ansi_term_codes = {
    'reset': "\x1b[m",  # ANSI CODE 0   → resets all styles, it's the same of \x1b[0m

    'bold': "\x1b[1m",  # ANSI CODE 1   → increases intensity, with a slight color change
    'rbold': "\x1b[22m",  # ANSI CODE 22  → resets bold or dim (they are mutually exclusive styles)

    'dim': "\x1b[2m",  # ANSI CODE 2   → decreases intensity, with a slight color change
    'rdim': "\x1b[22m",  # ANSI CODE 22  → resets bold or dim (they are mutually exclusive styles)

    'italic': "\x1b[3m",  # ANSI CODE 3   → italic
    'ritalic': "\x1b[23m",  # ANSI CODE 23  → resets italic

    'underline': "\x1b[4m",  # ANSI CODE 4   → underline
    'runderline': "\x1b[24m",  # ANSI CODE 24  → resets underline or doubleunderline (they are mutually exclusive styles)

    'doubleunderline': "\x1b[21m",  # ANSI CODE 21  → double underline (not supported by Konsole)
    'rdoubleunderline': "\x1b[24m",
    # ANSI CODE 24  → resets underline or doubleunderline (they are mutually exclusive styles)

    'curlyunderline': "\x1b[4:3m",  # ANSI CODE 4:3 → curly underline (not supported by Konsole)
    'rcurlyunderline': "\x1b[4:0m",  # ANSI CODE 4:0 → resets curly underline

    'blink': "\x1b[5m",  # ANSI CODE 5   → blink
    'rblink': "\x1b[25m",  # ANSI CODE 25  → resets blink

    'reverse': "\x1b[7m",  # ANSI CODE 7   → swaps text and background colors
    'rreverse': "\x1b[27m",  # ANSI CODE 27  → resets reverse

    'hidden': "\x1b[8m",  # ANSI CODE 8   → characters not displayed, helpful for passwords
    'rhidden': "\x1b[28m",  # ANSI CODE 28  → resets hidden

    'strikethrough': "\x1b[9m",  # ANSI CODE 9   → characters crossed by a central line
    'rstrikethrough': "\x1b[29m",  # ANSI CODE 29  → resets strikethrough

    'overline': "\x1b[53m",  # ANSI CODE 53 → overline
    'roverline': "\x1b[55m",  # ANSI CODE 55 → resets overline
}
ansi_color_codes = {
    # colors
    'yellowText': "\x1b[38;2;255;255;0m",
    'yellowBg': "\x1b[48;2;255;255;0m",
    'redText': "\x1b[38;2;255;0;0m",
    'redBg': "\x1b[48;2;255;0;0m",
    'greenText': "\x1b[38;2;0;255;0m",
    'greenBg': "\x1b[48;2;0;255;0m",
    'blueText': "\x1b[38;2;100;100;255m",
    'blueBg': "\x1b[48;2;0;0;255m",
    'blackText': "\x1b[38;2;0;0;0m",
    'blackBg': "\x1b[48;2;0;0;0m",
    'whiteText': "\x1b[38;2;255;255;255m",
    'whiteBg': "\x1b[48;2;255;255;255m",
}


def format_str(fmt_code, string):
    """
    Add Ansi codes to format a string and reset afterward
    :param str | list[str] fmt_code: one or more available format codes
    :param str string: what to format
    :return str: what to print after formatting eg: <start format>string<reset format>
    """
    ret = string
    if fmt_code is not None:
        if isinstance(fmt_code, str):
            fmt_list = [fmt_code]
        else:
            fmt_list = fmt_code

        rfmt = ""
        sfmt = ''
        err_fmt = ''

        for fmt in fmt_list:
            if fmt in ansi_term_codes.keys():
                sfmt += ansi_term_codes[fmt]
                rfmt += ansi_term_codes['r' + fmt]
            else:
                err_fmt += fmt + ', '

        if err_fmt != '':
            raise KeyError(f' Unknown format code(s) {err_fmt}')

        ret = f'{sfmt}{string}{rfmt}'

    return ret


def get_color(color, fg_bg='fg'):
    """
    Translate color to ansi color escape code
    :param str color: known color or 0xRRBBGG
    :param str fg_bg: "fg" or "bg" for foreground or background color
    :return str: ansi color escape code
    """
    if color is None:
        ret = ''
    elif isinstance(color, int) or color.startswith("0x"):
        c = int(color)
        r = (c & 0xFF0000) >> 16
        g = (c & 0x00FF00) >> 8
        b = (c & 0x0000FF)

        code = 38 if fg_bg.lower() == "fg" else 48
        ret = f"\x1b[{code};2;{r};{g};{b}m"
    else:
        if fg_bg.lower() == "bg":
            color_code = f'{color}Bg'
        elif fg_bg.lower() == "fg":
            color_code = f'{color}Text'
        else:
            raise KeyError(f' Unknown foreground/background code(s) {fg_bg}')
        if color_code not in ansi_color_codes.keys():
            raise KeyError(f' Unknown color code(s) {color}. You may specify colors as"0xRRGGBB"')
        ret = ansi_color_codes[color_code]
    return ret


def ansi_color_text(string, color=None, backgrond=None, reset=True):
    """
    Add color codes to a string, reset optionally inserted
    Colors can be Red, Green, Blue, Black, White, Yellow, or 0xRRGGBB
    :param str string: what to color
    :param str | int | None color: foreground color
    :param str | int |None backgrond: background color
    :param bool reset: reset option
    :return str: string with color codes for printng
    """

    fg = get_color(color, 'fg')
    bg = get_color(backgrond, 'bg')
    ret = f'{fg}{bg}{string}' + ansi_term_codes['reset'] if reset else ''
    return ret
