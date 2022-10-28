from pprint import pprint
import sys

from functools import reduce
from types import FunctionType

from aoc_inp import boards, draws

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


def problem4_1_get_draw_boards(boards: list[list[list[int]]]) -> list[list[list[tuple[int, bool]]]]:
    return list(map(lambda x: list(map(lambda x: list(map(lambda x: (x, False), x)), x)), boards))

def problem4_1_draw_board(board: list[list[tuple[int, bool]]], draw: int) -> list[list[tuple[int, bool]]]:
    return list(
        map(lambda x: list(map(lambda y: (y[0], True) if y[0] == draw else y, x)), board)) 

def problem4_1_draw_boards(boards: list[list[list[tuple[int, bool]]]], draw: int) -> list[list[list[tuple[int, bool]]]]:
    return list(map(lambda x: problem4_1_draw_board(x, draw), boards))

def problem4_1_check_rows(board: list[list[tuple[int, bool]]]) -> bool:
    return any(map(lambda x: all(map(lambda y: y[1], x)), board))

def problem4_1_check_cols(board: list[list[tuple[int, bool]]]) -> bool:
    return any(all(board[y][x][1] for y in range(len(board))) for x in range(len(board[0])))

def problem4_1_check_win(board: list[list[tuple[int, bool]]]) -> bool:
    return problem4_1_check_rows(board) or problem4_1_check_cols(board)

def problem4_1_get_best_board(boards: list[list[list[tuple[int, bool]]]], draws: list[int]) -> tuple[list[list[tuple[int, bool]]], int]:
    match list(problem4_1_draw_boards(boards, draws[0])):
        case new_boards:
            match list(filter(problem4_1_check_win, new_boards)):
                case [win_board]: 
                    return (win_board, draws[0])
                case [*_]:
                    return problem4_1_get_best_board(new_boards, draws[1:])

def problem4_1_get_score(board: list[list[tuple[int, bool]]], last_draw: int):
    return sum(sum(j[0] if not j[1] else 0 for j in i) for i in board) * last_draw

def problem4_1(boards: list[list[list[int]]], draws: list[int]):
    return problem4_1_get_score(*problem4_1_get_best_board(problem4_1_get_draw_boards(boards), draws))


def problem4_2_get_worst_board(boards: list[list[list[tuple[int, bool]]]], draws: list[int]) -> tuple[list[list[tuple[int, bool]]], int]:
    match list(problem4_1_draw_boards(boards, draws[0])):
        case new_boards:
            match list(filter(lambda x: not problem4_1_check_win(x), new_boards)):
                case []: 
                    return (new_boards[0], draws[0])
                case boards_left:
                    return problem4_2_get_worst_board(boards_left, draws[1:])

def problem4_2(boards: list[list[list[int]]], draws: list[int]):
    return problem4_1_get_score(*problem4_2_get_worst_board(problem4_1_get_draw_boards(boards), draws))