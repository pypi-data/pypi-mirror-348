#!/usr/bin/env python3

# FStringInterpolation - configparser with f-strings

# BSD 3-Clause License
# ====================
#
# _Copyright © 2025, IOhannes m zmölnig <zmoelnig@iem.at>
# _All rights reserved._
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the `<organization>` nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL `<COPYRIGHT HOLDER>` BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import builtins as _builtins
import configparser

# base on https://stackoverflow.com/a/54700827/1169096
def _fstr_eval(
    _s: str, globals=None, locals=None, raw_string=False, eval=_builtins.eval
):
    r"""str: Evaluate a string as an f-string literal.

    Args:
       _s (str): The string to evaluate.
       The globals must be a dictionary and locals can be any mapping,
          defaulting to the current globals and locals.
          If only globals is given, locals defaults to it.
       raw_string (bool, optional): Evaluate as a raw literal
           (don't escape \). Defaults to False.
       eval (callable, optional): Evaluation function. Defaults
           to Python's builtin eval.

    Raises:
        ValueError: Triple-apostrophes ''' are forbidden.
    """
    # Prefix all local variables with _ to reduce collisions in case
    # eval is called in the local namespace.
    _TA = "'''"  # triple-apostrophes constant, for readability
    if _TA in _s:
        raise ValueError(
            "Triple-apostrophes ''' are forbidden. " + 'Consider using """ instead.'
        )

    # Strip apostrophes from the end of _s and store them in _ra.
    # There are at most two since triple-apostrophes are forbidden.
    if _s.endswith("''"):
        _ra = "''"
        _s = _s[:-2]
    elif _s.endswith("'"):
        _ra = "'"
        _s = _s[:-1]
    else:
        _ra = ""
    # Now the last character of s (if it exists) is guaranteed
    # not to be an apostrophe.

    _prefix = "rf" if raw_string else "f"
    return eval(_prefix + _TA + _s + _TA, globals=globals, locals=locals) + _ra


class FStringInterpolation(configparser.Interpolation):
    """Interpolation that can use f-strings"""

    def before_get(self, parser, section, option, value, defaults):
        v0 = value
        v1 = None
        depth = 0
        ex = None
        try:
            while v0 != (v1 := _fstr_eval(v0, {}, defaults)):
                v0 = v1
                depth += 1
                if depth > configparser.MAX_INTERPOLATION_DEPTH:
                    raise InterpolationDepthError(option, section, value)
        except SyntaxError as e:
            raise configparser.InterpolationSyntaxError(option, section, str(e))
        except NameError as e:
            ex = configparser.InterpolationMissingOptionError(
                option, section, value, str(e)
            )
        except TypeError as e:
            ex = configparser.InterpolationError(option, section, str(e))
        except ValueError as e:
            # raise ValueError(f"eval({v0!r}, locals={defaults}) -> {e!s}")
            ex = configparser.InterpolationError(option, section, str(e))

        if ex is not None:
            raise ex

        return v0

    def before_set(self, parser, section, option, value):
        try:
            _fstr_eval(value, {}, {})
        except SyntaxError:
            raise ValueError(f"invalid f-expression {value!r}")
        return value


def _main():
    import sys

    def _dump(cfg, configfiles=[], configstring=""):
        if not cfg.read(configfiles):
            cfg.read_string(configstring)
        for s in cfg.sections():
            print(f"\n[{s}]")
            for k, v in cfg[s].items():
                print(f"{k} = {v}")

    myini = """
[DEFAULT]
value = 77.1230

[fstring]
value1 = {value}
value2 = two_{value}
value3 = three_{value2}
value_raw = {value!r}
value_int = {int(float(value))}

[basic]
value2 = two_%(value)s
value3 = three_%(value2)s

    """

    for interpolation in [configparser.BasicInterpolation, FStringInterpolation]:
        print(f"\n==================== {interpolation} =============")
        cfg = configparser.ConfigParser(interpolation=interpolation())
        _dump(cfg, sys.argv[1:], myini)


if __name__ == "__main__":
    _main()
