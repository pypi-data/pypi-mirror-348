#!/usr/bin/env python3
""" tests for uica """

from machine_code_analyzer.uica_wrapper import uiCA_wrapper


def test1():
    """ simple test, if this fails something is really off """
    test = "l: add rax, rbx; add rbx, rax; dec r15; jnz l"
    o = uiCA_wrapper(test)
    t = o.run()

    # print(t)
    assert t == 2.


def test2():
    """ simple test, if this fails something is really off """
    a = ["lea rax, -1040[rbp]", 
         "mov rsi, rax",
         "lea rax, .LC0[rip]",
         "mov rdi, rax"]
    test = "\n".join(a)
    o = uiCA_wrapper(test)
    t = o.run()

    # print(t)
    assert t == 1.25


if __name__ == "__main__":
    test1()
    test2()
