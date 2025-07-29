#!/usr/bin/env python3
""" main wrapper around uiCA """

import tempfile
from subprocess import Popen, PIPE, STDOUT
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

from .deps.uiCA import uiCA
from .deps.uiCA import microArchConfigs


class uiCA_wrapper():
    """
        this simple wrapper class makes it possible 
        return 0 if everything was good
               else error code of as
    """

    def assemble(self,
                 input_: str,
                 output: str) -> int:
        """
        TODO test if the assember is available
        assembles a file
        :param input_: input file 
        :param output: output file 
        :return 0 on success, else return code of the assembler
        """
        cmd = ["as", input_, "-o", output]
        with Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                   close_fds=True) as p:
            p.wait()
            if p.returncode != 0:
                assert p.stdout
                print("ERROR could not assemble:", p.returncode,
                      p.stdout.read().decode("utf-8"))
                return p.returncode
            return 0

    def run(self):
        """
            needed because constructors are not allowd to return something
        """
        TP = uiCA.runSimulation(self.disas,
                                self.uarch_config,
                                self.alignment_offset,
                                self.init_policy,
                                self.no_micro_fusion,
                                self.no_macro_fusion,
                                self.simple_front_end,
                                self.min_iterations,
                                self.min_cycles,
                                self.tp_only,
                                self.trace,
                                self.graph,
                                self.dep_graph,
                                self.json)
        return TP

    def __init__(self, input_: str, arch="SKL"):
        """
        :param input: input string to assemble and analyse
        """
        self.input = input_
        self.assembler_input_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".asm")
        self.assembler_output_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".o")
        self.arch = arch

        if arch not in microArchConfigs.MicroArchConfigs:
            print("invalid arch", arch)
            return

        self.assembler_input_file.write(".intel_syntax noprefix;\n")
        self.assembler_input_file.write(self.input)
        self.assembler_input_file.flush()

        if self.assemble(self.assembler_input_file.name,
                         self.assembler_output_file.name):
            print("error asm")
            return

        self._raw_binary_data = ""
        with open(self.assembler_output_file.name, "r", encoding="utf-8") as f:
            self._raw_binary_data = f.read()

        # default config from uiCA
        self.raw = False
        self.iaca_markers = False
        self.alignment_offset = 0
        self.init_policy = "diff"
        self.no_micro_fusion = False
        self.no_macro_fusion = False
        self.simple_front_end = False
        self.min_iterations = 10
        self.min_cycles = 500
        self.tp_only = False
        self.trace = None
        self.graph = None
        self.dep_graph = None
        self.json = None

        self.uarch_config = microArchConfigs.MicroArchConfigs[arch]
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.disas = md.disasm(self._raw_binary_data, 0x1000)
        #for i in :

        #self.disas = xed.disasFile(self.assembler_output_file.name, chip=self.uArchConfig.XEDName,
        #                           raw=self.raw,
        #                           useIACAMarkers=self.iacaMarkers)
