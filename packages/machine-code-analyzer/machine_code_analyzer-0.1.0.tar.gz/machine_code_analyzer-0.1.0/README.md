uiCA Wrapper:
============

This is just a simple wrapper project around [uiCA](https://github.com/andreas-abel/uiCA)
to be able to simply assemble and analyse instruction.

In comparison to the original project this project contains a class `uiCA_Wrapper` 
which can also analyse assembler instrucitons as strings or list of strings and
not just assembled binary files.

Example:
```python
test = "l: add rax, rbx; add rbx, rax; dec r15; jnz l"
o = uiCA_Wrapper(test)
t = o.run()
print(t)
```

Installation:
=============

To install the package locally run:
```bash
git clone --recursive https://github.com/FloydZ/uiCA_wrapper
cd uiCA_Wrapper
./setup.sh
```

Note the `setup.sh`. This is needed to build `uiCA`.
If you are a windoof user you can instead run 
```bash
cd uiCA_Wrapper/uiCA/
./setup.cmd
```

Restrictions:
=============

Currently, the throughput is calculated by the wrapper class. Everything else
is ignored.

TODO:
=====

llvm_mca wrapper: 
- pass all global information to the code regions, s.t. the same views can be generated.
- instruction: add information like throughput, latency. get from another python package