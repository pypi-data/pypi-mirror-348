import os
import asyncio
import pytest
from pytest import Config, TestReport, Session
from _pytest.terminal import TerminalReporter

from ayu.event_dispatcher import send_event, check_connection
from ayu.classes.event import Event
from ayu.utils import (
    EventType,
    TestOutcome,
    remove_ansi_escapes,
    build_dict_tree,
    # coverage_str_to_dict,
    get_coverage_data,
)

# import logging
# logging.basicConfig(level=logging.DEBUG)


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--disable-ayu",
        "--da",
        action="store_true",
        default=False,
        help="Enable Ayu plugin functionality",
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config) -> None:
    if not config.getoption("--disable-ayu"):
        config.pluginmanager.register(Ayu(config), "ayu_plugin")


class Ayu:
    def __init__(self, config: Config):
        self.config = config
        self.connected = False

        if check_connection():
            print("Websocket connected")
            self.connected = True
        else:
            self.connected = False
            print("Websocket not connected")

        # if self.config.pluginmanager.hasplugin("pytest_cov"):
        #     from pytest_cov.plugin import CovPlugin
        #     self.cov_plugin: CovPlugin = self.config.pluginmanager.get_plugin("pytest_cov").CovPlugin(
        #         options = self.config.option,
        #         pluginmanager = self.config.pluginmanager,
        #     )

    # must tryfirst, otherwise collection-only is returning
    @pytest.hookimpl(tryfirst=True)
    def pytest_runtestloop(self, session: Session):
        if self.connected and session.config.getoption("--collect-only"):
            asyncio.run(
                send_event(
                    event=Event(
                        event_type=EventType.DEBUG,
                        event_payload={"test": "test"},
                        # event_payload={"no_items":session.testscollected,"items":f"{session.items}"},
                    )
                )
                # ,debug_mode=True
            )

    # build test tree
    def pytest_collection_finish(self, session: Session):
        if self.connected:
            print("Connected to Ayu")
            if session.config.getoption("--collect-only"):
                tree = build_dict_tree(items=session.items)
                asyncio.run(
                    send_event(
                        event=Event(
                            event_type=EventType.COLLECTION,
                            event_payload=tree,
                            # event_payload={"items":session.items},
                        )
                    ),
                )
            else:
                asyncio.run(
                    send_event(
                        event=Event(
                            event_type=EventType.SCHEDULED,
                            event_payload=[item.nodeid for item in session.items],
                        )
                    )
                )
        return

    # gather status updates during run
    def pytest_runtest_logreport(self, report: TestReport):
        if self.config.pluginmanager.hasplugin("xdist") and (
            "PYTEST_XDIST_WORKER" not in os.environ
        ):
            return

        is_relevant = (report.when == "call") or (
            (report.when == "setup")
            and (report.outcome.upper() in [TestOutcome.FAILED, TestOutcome.SKIPPED])
        )

        if self.connected and is_relevant:
            asyncio.run(
                send_event(
                    event=Event(
                        event_type=EventType.OUTCOME,
                        event_payload={
                            "nodeid": report.nodeid,
                            "outcome": report.outcome.upper(),
                        },
                    )
                )
            )

    # summary after run for each tests
    @pytest.hookimpl(trylast=True)
    def pytest_terminal_summary(self, terminalreporter: TerminalReporter):
        if self.config.pluginmanager.hasplugin("xdist") and (
            "PYTEST_XDIST_WORKER" not in os.environ
        ):
            return

        if self.config.pluginmanager.hasplugin("_cov"):
            # coverage_str = self.config.pluginmanager.getplugin(
            #     "_cov"
            # ).cov_report.getvalue()

            # coverage_dict = coverage_str_to_dict(coverage_report_str=coverage_str)
            coverage_dict = get_coverage_data()

            if self.connected:
                asyncio.run(
                    send_event(
                        event=Event(
                            event_type=EventType.COVERAGE,
                            event_payload={
                                "coverage_dict": coverage_dict,
                            },
                        )
                    )
                )

        report_dict = {}
        # warning report has no report.when
        for outcome, reports in terminalreporter.stats.items():
            # raise Exception(terminalreporter.stats.keys())
            if outcome in ["", "deselected"]:
                continue
            for report in reports:
                report_dict[report.nodeid] = {
                    "nodeid": report.nodeid,
                    # Not in warning report
                    "when": report.when,
                    "caplog": report.caplog,
                    "longreprtext": remove_ansi_escapes(report.longreprtext),
                    "duration": report.duration,
                    "outcome": report.outcome,
                    "lineno": report.location[1],
                    "otherloc": report.location[2],
                }

        # import json

        if self.connected:
            asyncio.run(
                send_event(
                    event=Event(
                        event_type=EventType.REPORT,
                        event_payload={
                            "report": report_dict,
                        },
                    )
                )
            )
