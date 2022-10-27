import sys

from functools import reduce
from types import FunctionType

from aoc_inp import inp

sys.setrecursionlimit(1_000_000_000)


def problem1_1_iter(inp: list[int]):
    for i in range(1, len(inp)):
        yield (inp[i-1], inp[i]) 

def problem1_1(inp: list[int]) -> int:
    return sum(map(lambda vals: int(vals[1] > vals[0]), problem1_1_iter(inp)))


def problem1_2(inp: list[int]) -> int:
    return problem1_1([sum(inp[i:i+3]) for i in range(0, len(inp)-2)])


def problem2_1_depth_instr(instr: str) -> int:
    return int(instr.split()[1]) if instr.startswith("down") else -int(instr.split()[1])

def problem2_1(inp: list[str]) -> int:
    return \
        sum((int(instr.split()[1]) for instr in 
            filter(lambda instr: instr.startswith("forward"), inp))) *\
        sum((problem2_1_depth_instr(instr) for instr in 
            filter(lambda instr: not instr.startswith("forward"), inp)))


def problem2_2_exec_instr(op: str, arg: int, state: tuple[int, int, int]):
    match op:
        case "forward": return (state[0]+arg, state[1]+arg*state[2], state[2])
        case "up":      return (state[0],     state[1],              state[2]-arg)
        case "down":    return (state[0],     state[1],              state[2]+arg)

def problem2_2_parse_instr(instr: str) -> tuple[str, int]:
    """
    Returns (op_type, arg) 
    """
    return (instr.split()[0], int(instr.split()[1]))

def problem2_2_exec(inp: list[str], state: tuple[int, int, int]):
    """
    state - (pos_x, pos_y, aim)
    """
    match inp:
        case [instr]: 
            return problem2_2_exec_instr(*problem2_2_parse_instr(instr), state)
        case [instr, *rest]: 
            return problem2_2_exec(rest, problem2_2_exec_instr(*problem2_2_parse_instr(instr), state))

def problem2_2(inp: list[str]):
    match problem2_2_exec(inp, (0, 0, 0)):
        case (x, y, _): return x * y


def problem3_1_get_bit_gamma(bits: list[str]):
    return "1" if reduce(lambda prev, curr: int(prev)+int(curr == "1"), bits) > len(bits) // 2 else "0"

def problem3_1_get_gamma(inp: list[str]) -> str:
    return "".join([problem3_1_get_bit_gamma(list(map(lambda x: x[i], inp))) for i in range(len(inp[0]))])

def problem3_1(inp: list[str]):
    match problem3_1_get_gamma(inp):
        case gamma:
            return int(gamma, 2) * int("".join(map(lambda x: "1" if x == "0" else "0", gamma)), 2)


def problem3_2_get_bit_oxygen(bits: list[str]):
    return "1" if reduce(lambda prev, curr: int(prev)+int(curr == "1"), bits) * 2 >= len(bits) else "0"

def problem3_2_get_bit_co2(bits: list[str]):
    return "0" if reduce(lambda prev, curr: int(prev)+int(curr == "1"), bits) * 2 >= len(bits) else "1"

def problem3_2_get_rate(func: FunctionType, inp: list[str], index: int = 0):
    match inp:
        case [res]: return res
        case _:
            match func(list(map(lambda x: x[index], inp))):
                case bit:
                    return problem3_2_get_rate(func, list(filter(lambda x: x[index] == bit, inp)), index+1)

def problem3_2_get_oxygen_rate(inp: list[str]):
    return problem3_2_get_rate(problem3_2_get_bit_oxygen, inp, 0)

def problem3_2_get_co2_rate(inp: list[str]):
    return problem3_2_get_rate(problem3_2_get_bit_co2, inp, 0)

def problem3_2(inp: list[str]):
    return int(problem3_2_get_oxygen_rate(inp), 2) * int(problem3_2_get_co2_rate(inp), 2) 