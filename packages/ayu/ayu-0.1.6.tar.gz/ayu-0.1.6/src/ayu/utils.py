from typing import Any
import os
import shutil
import re
from enum import Enum
from pathlib import Path
import subprocess

import asyncio
from pytest import Item, Class, Function
from _pytest.nodes import Node

from ayu.constants import WEB_SOCKET_PORT, WEB_SOCKET_HOST


class NodeType(str, Enum):
    DIR = "DIR"
    MODULE = "MODULE"
    CLASS = "CLASS"
    FUNCTION = "FUNCTION"
    COROUTINE = "COROUTINE"


class EventType(str, Enum):
    COLLECTION = "COLLECTION"
    SCHEDULED = "SCHEDULED"
    OUTCOME = "OUTCOME"
    REPORT = "REPORT"
    COVERAGE = "COVERAGE"
    DEBUG = "DEBUG"


class TestOutcome(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    QUEUED = "QUEUED"
    # handle those
    XFAILED = "XFAILED"
    XPASSED = "XPASSED"
    ERROR = "XPASSED"


def run_test_collection(tests_path: str | None = None):
    """Collect All Tests without running them"""
    if ayu_is_run_as_tool():
        command = "uv run --with ayu pytest --co".split()
    else:
        command = "uv run pytest --co".split()

    if tests_path:
        command.extend([tests_path])

    return subprocess.run(
        command,
        capture_output=True,
    )


async def run_all_tests(
    tests_path: str | None = None, tests_to_run: list[str] | None = None
):
    """Run all selected tests"""
    if ayu_is_run_as_tool():
        command = "uv run --with ayu pytest "
    else:
        command = "uv run python -m pytest "

    if tests_to_run:
        command += " ".join(tests_to_run)
    else:
        if tests_path:
            command += tests_path
    return await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )


def get_nice_tooltip(node_data: dict) -> str | None:
    tooltip_str = ""
    # tooltip_str = f"{node_data['name'].replace("[", "\["):^20}\n"
    # tooltip_str += f"[red strike]{node_data['name'].replace('[', '\['):^20}[/]\n"
    #
    # status = node_data["status"].replace("[", "\[")
    # tooltip_str += f"\n[yellow]{status}[/]\n\n"
    return tooltip_str


def get_preview_test(file_path: str, start_line_no: int) -> str:
    """Read the test file from nodeid and use the linenumber
    and some rules to display the test function"""
    with open(Path(file_path), "r") as file:
        file_lines = file.readlines()
        last_line_is_blank = False
        end_line_no = None
        for line_no, line in enumerate(file_lines[start_line_no:], start=start_line_no):
            if not line.strip():
                last_line_is_blank = True
                continue
            if (
                line.strip().startswith(("def ", "class ", "async def ", "@"))
                and last_line_is_blank
            ):
                end_line_no = line_no - 1
                break
            last_line_is_blank = False
        return "".join(file_lines[start_line_no:end_line_no]).rstrip()


def get_ayu_websocket_host_port() -> tuple[str, int]:
    host: str = os.environ.get("AYU_HOST", WEB_SOCKET_HOST)
    port: int = int(os.environ.get("AYU_PORT", WEB_SOCKET_PORT))
    return host, port


def remove_ansi_escapes(string_to_remove: str) -> str:
    """Remove ansi escaped strings from colored pytest output"""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", string_to_remove)


def uv_is_installed():
    if shutil.which("uv"):
        return True
    return False


def project_is_uv_managed():
    toml_path = Path.cwd() / "pyproject.toml"
    return toml_path.exists()


def ayu_is_run_as_tool():
    result = subprocess.run(
        "uv tree --package ayu".split(), capture_output=True, text=True
    )
    if result.stdout:
        return False
    return True


def build_dict_tree(items: list[Item]) -> dict:
    markers = set()

    def create_node(node: Node) -> dict[Any, Any]:
        markers.update([mark.name for mark in node.own_markers])
        return test_node_to_dict(node=node)

    def add_node(node_list: list[Node], sub_tree: dict):
        if not node_list:
            return

        # take root node
        current_node = node_list.pop(0)
        node_dict = create_node(node=current_node)

        existing_node = next(
            (
                node
                for node in sub_tree["children"]
                if node["nodeid"] == current_node.nodeid
            ),
            None,
        )

        if existing_node is None:
            sub_tree["children"].append(node_dict)
            existing_node = node_dict

        add_node(
            node_list=node_list,
            sub_tree=existing_node,
        )

    tree: dict[Any, Any] = {}
    root = items[0].listchain()[1]
    tree[root.name] = create_node(node=root)

    for item in items:
        # gets all parents except session
        parts_to_collect = item.listchain()[1:]
        add_node(node_list=parts_to_collect[1:], sub_tree=tree[root.name])

    return {"tree": tree, "meta": {"test_count": len(items), "markers": list(markers)}}


def get_coverage_data(coverage_file=".coverage"):
    import coverage

    cov = coverage.Coverage(data_file=coverage_file)
    cov.load()

    report_dict = {}

    all_files = cov.get_data().measured_files()
    for file_path in sorted(all_files):
        file_data = cov.analysis2(file_path)
        # analysis2 returns: (0:filename, 1:statements, 2:excluded, 3:missing, 4:partial)
        total_statements = len(file_data[1])  # All statements
        missing_statements = len(file_data[3])  # Uncovered statements
        coverage_percent = (
            (total_statements - missing_statements) / total_statements * 100
            if total_statements > 0
            else 0
        )

        # Store data for this file
        displayed_path = Path(file_path).relative_to(Path.cwd()).as_posix()
        report_dict[displayed_path] = {
            "n_statements": total_statements,
            "n_missed": missing_statements,
            "percent_covered": round(coverage_percent, 2),
            "lines_missing": file_data[3],  # List of uncovered line numbers
        }

    return report_dict


def test_node_to_dict(node: Node) -> dict[str, Any]:
    return {
        "name": node.name,
        "nodeid": node.nodeid,
        "markers": [mark.name for mark in node.own_markers],
        "path": node.path.as_posix(),
        "lineno": node.reportinfo()[1]
        if isinstance(node, Class)
        else (node.location[1] if isinstance(node, Function) else 0),
        "parent_name": node.parent.name if node.parent else None,
        "parent_type": type(node.parent).__name__.upper() if node.parent else None,
        "type": type(node).__name__.upper(),
        "favourite": False,
        "status": "",
        "children": [],
    }


def build_bar(percentage: float) -> str:
    SEGS = ["▉", "▊", "▋", "▌", "▍", "▎", "▏", " "]
    tens = int(percentage // 10)
    rest = int(percentage - tens)
    not_tens = int((100 - percentage) // 10)

    tens_bar = f"[green on green]{tens * ' '}[/]"
    rest_bar = f"[green on red]{SEGS[2]}[/]" if rest else ""
    not_tens_bar = f"[on red]{not_tens * ' '}[/]"
    return tens_bar + rest_bar + not_tens_bar
