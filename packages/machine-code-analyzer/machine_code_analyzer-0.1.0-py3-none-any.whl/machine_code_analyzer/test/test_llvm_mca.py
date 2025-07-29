#!/usr/bin/env python3
""" tests for the python_mca_wrapper.py """

import os
from machine_code_analyzer import LLVM_MCA


def test_version():
    """ tests only the __version__() function """
    a = LLVM_MCA("")
    assert a.__version__()


def test_arch():
    """ tests only the __arch__() function """
    a = LLVM_MCA("")
    arch = a.__arch__()
    assert len(arch) > 0


def test_cpu():
    """ tests only the __cpu__() function """
    a = LLVM_MCA("")
    cpus, features = a.__cpu__()
    assert len(cpus) > 0
    assert len(features) > 0


def test_execute():
    """ """
    a = LLVM_MCA("files/avx_short.s")
    t = a.execute()
    print(t)


def test_simple():
    """ """
    bla = os.path.dirname(os.path.abspath(__file__))
    a = LLVM_MCA(bla + "/../test/avx_short.s")
    print(a.execute())


if __name__ == "__main__":
    test_version()
    test_arch()
    test_cpu()
    test_execute()
    test_simple()
