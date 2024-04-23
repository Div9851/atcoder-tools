import argparse
import os
import re
import time
import requests
from enum import Enum, auto
from markdownify import markdownify as md


class ContestType(Enum):
    ABC = auto()
    ARC = auto()
    AGC = auto()

    def to_str(self) -> str:
        if self == ContestType.ABC:
            return "abc"
        elif self == ContestType.ARC:
            return "arc"
        elif self == ContestType.AGC:
            return "agc"


PROBLEM_STATEMENT = re.compile(
    r"<section>\s*<h3>Problem Statement</h3>\s*(?P<problem_statement>.*?)<\/section>",
    flags=re.DOTALL,
)


def get_number_of_problems(contest_type: ContestType, n_th: int) -> int:
    if contest_type == ContestType.ABC:
        if n_th <= 125:
            return 4
        elif n_th <= 211:
            return 6
        elif n_th <= 318:
            return 8
        else:
            return 7
    else:
        raise Exception(f"unsupported contest type: {contest_type.name}")


def extract_problem_statement(text: str) -> str:
    match_result = PROBLEM_STATEMENT.search(text)
    if match_result is None:
        raise Exception("cloud not extract problem statement from the given text")
    return match_result.group("problem_statement")


def parse_contest_type(s: str) -> ContestType:
    if s == "abc":
        return ContestType.ABC
    elif s == "arc":
        return ContestType.ARC
    elif s == "agc":
        return ContestType.AGC
    raise ValueError(f"unknown contest type {s}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contest-type",
        type=parse_contest_type,
        required=True,
    )
    parser.add_argument("--range-start", type=int, required=True)
    parser.add_argument("--range-end", type=int, required=True)
    parser.add_argument("--dest", default="problems")
    args = parser.parse_args()
    contest_type: ContestType = args.contest_type
    range_start: int = args.range_start
    range_end: int = args.range_end
    dest: str = args.dest

    os.makedirs(dest, exist_ok=True)
    for n_th in range(range_start, range_end):
        number_of_problems = get_number_of_problems(contest_type, n_th)
        for i in range(number_of_problems):
            contest_name = f"{contest_type.to_str()}{n_th}"
            problem_name = f"{contest_name}_{chr(ord('a')+i)}"
            save_to = os.path.join(dest, f"{problem_name}.md")
            print(f"save {save_to}")
            if os.path.isfile(save_to):
                print(f"{save_to} already exists")
                continue
            problem_url = (
                f"https://atcoder.jp/contests/{contest_name}/tasks/{problem_name}"
            )
            problem_statement = extract_problem_statement(
                requests.get(problem_url).text
            )
            with open(save_to, "w") as f:
                f.write(md(problem_statement))
            # リクエストを大量に送信しないようにするためスリープする
            time.sleep(1)


if __name__ == "__main__":
    main()
