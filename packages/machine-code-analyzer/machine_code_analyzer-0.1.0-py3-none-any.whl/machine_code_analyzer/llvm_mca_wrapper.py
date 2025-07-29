#!/usr/bin/env python3
""" main wrapper around llvm-mca """

from subprocess import Popen, PIPE, STDOUT
import logging
import re
import json
import tempfile
import os
from pathlib import Path
from typing import Tuple, Union, List
from types import SimpleNamespace


class SimulationParameters:
    """wrapper around the output field of `llvm-mca` 
    "SimulationParameters": {
        "-march": "i386",
        "-mcpu": "znver4",
        "-mtriple": "i386-unknown-linux-gnu"
    },  
    """
    def __init__(self, parsed):
        """
        :param parsed: 
        """
        self.__parsed = vars(parsed)
        self.__arch = self.__parsed["-march"]
        self.__cpu = self.__parsed["-mcpu"]
        self.__triple = self.__parsed["-mtriple"]

    def get_arch(self):
        """
        :return __arch
        """
        return self.__arch

    def get_cpu(self):
        """
        :return __cpu
        """
        return self.__cpu

    def get_triple(self):
        """
        :return __triple
        """
        return self.__triple

    def __str__(self) -> str:
        return str(self.__parsed)

    def __repr__(self) -> str:
        return str(self.__dict__)


class TargetInfo:
    """wrapper around the output field with the same name.
    Something like this:

     "TargetInfo": {
        "CPUName": "znver4",
        "Resources": [
            "Zn4AGU0",
            "Zn4AGU1",
            "Zn4AGU2",
            "Zn4ALU0",
            "Zn4ALU1",
            "Zn4ALU2",
            "Zn4ALU3",
            "Zn4BRU1",
            "Zn4FP0",
            "Zn4FP1",
            "Zn4FP2",
            "Zn4FP3",
            "Zn4FP45.\u0000",
            "Zn4FP45.\u0001",
            "Zn4FPSt",
            "Zn4LSU.\u0000",
            "Zn4LSU.\u0001",
            "Zn4LSU.\u0002",
            "Zn4Load.\u0000",
            "Zn4Load.\u0001",
            "Zn4Load.\u0002",
            "Zn4Store.\u0000",
            "Zn4Store.\u0001"
        ]
    }
    """
    def __init__(self, parsed):
        """ """
        self.__parsed = vars(parsed)
        self.__cpuname = self.__parsed["CPUName"]
        self.__resources = self.__parsed["Resources"]

    def get_resources(self, i: Union[int, None] = None):
        """
        :param i:
        :return:
        """
        if i is not None:
            return self.__resources[i] if i < len(self.__resources) else None
        return self.__resources

    def get_cpuname(self):
        """
        :return the 'cpuname'
        """
        return self.__cpuname

    def __str__(self):
        return str(self.__parsed)

    def __repr__(self) -> str:
        return str(self.__dict__)


class StallDispatchStatistic:
    """

    :param group:
    :param lq: load queue
    :param rat: register unavailable
    :param rcu: retire tokens unavailable
    :param schedq: scheduler full
    :param sq: storage queue full
    :param ush: uncategorized structural hazard
    """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        # stall information: why an instruction was stalled
        # static restrictions on the dispatch group
        self.group = self.__parsed["GROUP"]
        # load queue full
        self.lq = self.__parsed["LQ"]
        # register unavailable
        self.rat = self.__parsed["RAT"]
        # retire tokens unavailable
        self.rcu = self.__parsed["RCU"]
        # scheduler full
        self.schedq = self.__parsed["SCHEDQ"]
        # store queue full
        self.sq = self.__parsed["SQ"]
        # uncategorized structural hazard
        self.ush = self.__parsed["USH"]

    def __repr__(self) -> str:
        return str(self.__dict__)


class Instruction:
    """
    something like: (part of the `InstructionInfoView`)
        {
          "Instruction": 0,
          "Latency": 3,
          "NumMicroOpcodes": 1,
          "RThroughput": 0.5,
          "hasUnmodeledSideEffects": false,
          "mayLoad": false,
          "mayStore": false
        },
    """
    def __init__(self, parsed, assembly: str):
        self.__parsed = vars(parsed)
        self.__assembly = assembly
        self.instruction = self.__parsed["Instruction"]
        self.latency = self.__parsed["Latency"]
        self.num_microppcodes = self.__parsed["NumMicroOpcodes"]
        self.rthroughput = self.__parsed["RThroughput"]
        self.has_unmodeled_side_effects = self.__parsed["hasUnmodeledSideEffects"]
        self.may_load = self.__parsed["mayLoad"]
        self.may_store = self.__parsed["mayStore"]

    def __repr__(self) -> str:
        return str(self.__dict__)


class ResourcePressureInfo:
    """
    Something like:
    {
        "InstructionIndex": 0,
        "ResourceIndex": 8,
        "ResourceUsage": 0.5
    },
    """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.instruction_index = self.__parsed["InstructionIndex"]
        self.resource_index = self.__parsed["ResourceIndex"]
        self.resource_usage = self.__parsed["ResourceUsage"]

    def __repr__(self) -> str:
        return str(self.__dict__)


class ResourcePressureView:
    """
    Something like this
    "ResourcePressureView": {
        "ResourcePressureInfo": [
            {
                "InstructionIndex": 0,
                "ResourceIndex": 8,
                "ResourceUsage": 0.5
            },
            ...
            {
                "InstructionIndex": 3,
                "ResourceIndex": 10,
                "ResourceUsage": 4
            }
        ]
    },
    """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.resource_pressure_info = [ResourcePressureInfo(a)
            for a in self.__parsed["ResourcePressureView"]]


class SummaryView:
    """
    "SummaryView": {
        "BlockRThroughput": 4,
        "DispatchWidth": 6,
        "IPC": 0.73529411764705888,
        "Instructions": 300,
        "Iterations": 100,
        "TotalCycles": 408,
        "TotaluOps": 700,
        "uOpsPerCycle": 1.7156862745098038
    },
    """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.block_rt_throughput = self.__parsed["BlockRThroughput"]
        self.dispatch_width = self.__parsed["DispatchWidth"]
        self.ipc = self.__parsed["IPC"]
        self.instructions = self.__parsed["Instructions"]
        self.iterations = self.__parsed["Iterations"]
        self.total_uops = self.__parsed["TotaluOps"]
        self.uops_per_cycle = self.__parsed["uOpsPerCycle"]

    def __repr__(self) -> str:
        return str(self.__dict__)


class TimelineInfo:
    """ something like:
          {
            "CycleDispatched": 0,
            "CycleExecuted": 4,
            "CycleIssued": 1,
            "CycleReady": 0,
            "CycleRetired": 5
          },
    """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.cycle_dispatched = self.__parsed["CycleDispatched"]
        self.cycle_executed = self.__parsed["CycleExecuted"]
        self.cycle_issued = self.__parsed["CycleIssued"]
        self.cycle_ready = self.__parsed["CycleReady"]
        self.cycle_retired = self.__parsed["CycleRetired"]

    def __repr__(self) -> str:
        return str(self.__dict__)


class TimelineView:
    """ something like:
        [
            TimelineInfo1,
            TimelineInfo2,
            ...
        ]
    """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.timeline_infos = [TimelineInfo(a) for a in self.__parsed["TimelineInfo"]]

    def __repr__(self) -> str:
        return str(self.__dict__)


class LLVM_MCA_Data:
    """
    :param SimulationParameters
    """
    def __init__(self, parsed_json):
        """
        :param_json: output of the `llvm-mca`
        """
        self.parsed_json = parsed_json
        if len(parsed_json.CodeRegions) != 0:
            raise Exception("only a single region is supported")
        cr = parsed_json.CodeRegions[0]

        self.simulation_parameters = SimulationParameters(parsed_json.SimulationParameters)
        self.target_info = TargetInfo(parsed_json.TargetInfo)
        self.stall_info = StallDispatchStatistic(cr.DispatchStatistics)
        self.summary_view = SummaryView(cr.SummaryView)
        self.timeline_view = TimelineView(cr.TimelineView)

        # wrapper around `InstructionInfoView`
        self.instructions = []

        assert len(cr.InstructionInfoView.InstructionList) == \
               len(cr.Instructions)
        for i in range(len(cr.Instructions)):
            self.instructions.append(Instruction(cr.InstructionInfoView.InstructionList[i],
                                                 cr.Instructions[i]))

    def print_ressource_pressure_by_instruction(self) -> str:
        """
        :return
        """
        raise NotImplementedError

    def __str__(self):
        return str(self.parsed_json)


class LLVM_MCA:
    """
    wrapper around the command `llvm-mca`
    """
    BINARY = "llvm-mca"
    LLC = "llc"
    ARGS = ["--all-stats", "--all-views", "--bottleneck-analysis", "--json"]

    def __init__(self, file: Union[str, Path]) -> None:
        """
        :param file:
        """
        self.__file = file.absolute() if isinstance(file, Path) else file
        self.__outfile = tempfile.NamedTemporaryFile(suffix=".json").name
        if os.path.isfile(self.__outfile):
            self.execute()

    def execute(self):
        """
        NOTE: writes the result into a file
        """
        cmd = [LLVM_MCA.BINARY] + LLVM_MCA.ARGS + [self.__file] + ["-o", self.__outfile]
        with Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT) as p:
            while p.returncode is None:
                p.poll()
            assert p.stdout

            if p.returncode != 0 and p.returncode is not None:
                data = p.stdout.read()
                data = str(data).replace("b'", "").replace("\\n'", "").lstrip()
                logging.error(f"couldn't execute: {data}")
                return None

            with open(self.__outfile, "r", encoding="utf-8") as f:
                data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
                return LLVM_MCA_Data(data)

    def __arch__(self):
        """
        returns a list of supported architectures
        e.g:
            [
                ...
                ppc64le
                r600
                riscv32
                riscv64
                sparc
                ...
            ]
        """
        cmd = [LLVM_MCA.BINARY, "--version"]
        data = []
        with Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                   close_fds=True) as p:
            p.wait()
            assert p.stdout

            data = p.stdout.readlines()
            data = [str(a).replace("b'", "")
                          .replace("\\n'", "")
                          .lstrip() for a in data]

            if p.returncode != 0:
                logging.error(cmd, "not available: %s", data)
                return None, None

            assert len(data) > 1
        found = None
        i = 0
        for i, d in enumerate(data):
            if "Registered Targets:" in d:
                found = i + 1
                break

        if not found:
            logging.error("parsing error")
            return []

        cpus = []
        for d in data[found:]:
            t = re.findall(r'\S+', d)
            assert len(t) > 1
            cpus.append(t[0])

        found = None
        for j, d in enumerate(data[i:]):
            if "Registered Targets:" in d:
                found = j + 1

        if not found:
            logging.error("parsing error")
            return [], []

        return cpus

    def __cpu__(self, arch: str = "x86") -> Tuple[List[str], List[str]]:
        """
        returns a list of available cpus and features
        e.g:
            [..., athlon64-sse3, atom, barcelona, bdver1, ...]
        and a list of available cpu features:
            [..., amx-tile, avx, avx2, avx512bf16, ... ]
        """
        cmd = [LLVM_MCA.LLC, f"-march={arch}", "-mcpu=help"]
        data = []
        with Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                   close_fds=True) as p:
            p.wait()
            assert p.stdout

            data = p.stdout.readlines()
            data = [str(a).replace("b'", "")
                    .replace("\\n'", "")
                    .lstrip() for a in data]

            if p.returncode != 0:
                logging.error(cmd, "not available: %s", data)
                return [], []

            assert len(data) > 1
        found = False
        for i, d in enumerate(data):
            if "Available CPUs" in d:
                found = True

        if not found:
            logging.error("starting point not found")
            return [], []

        i = 1
        data = data[i:]
        cpus, features = [], []
        for d in data:
            i += 1
            if "Available features" in d:
                break
            if len(d) == 0:
                continue

            t = re.findall(r'\S+', d)
            assert len(t) > 0
            cpus.append(t[0])

        data = data[i-1:]
        for d in data:
            if len(d) == 0:
                continue
            t = re.findall(r'\S+', d)
            assert len(t) > 0
            features.append(t[0])
        return cpus, features

    def __version__(self):
        """
        returns version as string if valid.
        otherwise `None`
        """
        cmd = [LLVM_MCA.BINARY, "--version"]
        with Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
                   close_fds=True) as p:
            p.wait()
            assert p.stdout

            data = p.stdout.readlines()
            data = [str(a).replace("b'", "")
                          .replace("\\n'", "")
                          .lstrip() for a in data]

            if p.returncode != 0:
                logging.error(cmd, "not available: %s", data)
                return None

            assert len(data) > 1
            for d in data:
                if "LLVM version" in d:
                    ver = re.findall(r'\d.\d+.\d', d)
                    assert len(ver) == 1
                    return ver[0]

        return None
