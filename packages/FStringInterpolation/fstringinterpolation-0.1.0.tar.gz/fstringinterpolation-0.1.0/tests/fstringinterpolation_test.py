#!/usr/bin/env python3

# FStringInterpolation - tests

import configparser
import pytest

import fstringinterpolation

pi = "3.1415926535897932384626433832795"

inistring = """
[DEFAULT]
a = %s
title = {a} is {"more" if float(a) > float(b) else "less"} than {b}
[basic]
b = two_%%(a)s
c = three_%%(b)s
[fstring]
b = two_{a}
c = three_{b}
[more]
b = 0
[more2]
b = {(float(a)-1)}
[less]
b = 42
[less2]
b = {(float(a)+1)}
[shortfloat]
pi = {float(a):.2f}
[shortstring]
pi = {a:.2s}
[halfpi]
halfpi = {float(a)/2}
[badhalfpi]
halfpi = {a/2}
[sum]
a = 4
b = 5
realsum = {sum(float(_) for _ in [a,b])}
[badsum]
b = 5
sum = {sum(float(_) for _ in [a,b])}
""" % (
    pi,
)


## helpers


def config_from_string(configstring: str):
    cfg = configparser.ConfigParser(
        interpolation=fstringinterpolation.FStringInterpolation()
    )
    cfg.read_string(configstring)
    return cfg


def get(section, option):
    cfg = config_from_string(inistring)
    return cfg[section][option]


## the actual tests
def test_basic_a():
    assert get("basic", "a") == pi


def test_basic_b():
    assert get("basic", "b") == f"two_%(a)s"


def test_basic_c():
    assert get("basic", "c") == f"three_%(b)s"


def test_fstring_a():
    assert get("fstring", "a") == pi


def test_fstring_b():
    assert get("fstring", "b") == f"two_{pi}"


def test_fstring_c():
    assert get("fstring", "c") == f"three_two_{pi}"


def test_more_a():
    assert get("more", "a") == pi


def test_more_b():
    assert get("more", "b") == "0"


def test_more_c():
    with pytest.raises(KeyError):
        get("more", "c")


def test_more_title():
    assert get("more", "title") == f"{pi} is more than 0"


def test_more2_a():
    assert get("more2", "a") == pi


def test_more2_b():
    assert float(get("more2", "b")) == float(pi) - 1


def test_more2_c():
    with pytest.raises(KeyError):
        get("more2", "c")


@pytest.mark.skip(reason="needs fixing")
def test_more2_title():
    assert get("more2", "title") == f"{pi} is more than 0"


def test_less_a():
    assert get("less", "a") == pi


def test_less_b():
    assert get("less", "b") == "42"


def test_less_title():
    assert get("less", "title") == f"{pi} is less than 42"


def test_less2_a():
    assert get("less2", "a") == pi


def test_less2_b():
    assert float(get("less2", "b")) == float(pi) + 1


@pytest.mark.skip(reason="needs fixing")
def test_less2_title():
    assert get("less2", "title") == f"{pi} is less than 42"


def test_shortfloat_a():
    assert get("shortfloat", "a") == pi


def test_shortfloat_pi():
    assert get("shortfloat", "pi") == f"{float(pi):.2f}"


def test_shortfloat_title():
    with pytest.raises(configparser.InterpolationMissingOptionError):
        get("shortfloat", "title")


def test_shortstring_a():
    assert get("shortstring", "a") == pi


def test_shortstring_pi():
    assert get("shortstring", "pi") == pi[:2]


def test_shortstring_title():
    with pytest.raises(configparser.InterpolationMissingOptionError):
        get("shortstring", "title")


def test_halfpi_halfpi():
    assert float(get("halfpi", "halfpi")) == float(pi) / 2


def test_badhalfpi_badhalfpi():
    with pytest.raises(configparser.InterpolationError):
        get("badhalfpi", "halfpi")


def test_sum_a():
    assert get("sum", "a") == "4"


def test_sum_b():
    assert get("sum", "b") == "5"


def test_sum_title():
    assert float(get("sum", "realsum")) == 9


def test_badsum_a():
    assert get("badsum", "a") == "3.1415926535897932384626433832795"


def test_badsum_b():
    assert get("badsum", "b") == "5"


def test_badsum_sum():
    with pytest.raises(configparser.InterpolationError):
        get("badsum", "sum")
