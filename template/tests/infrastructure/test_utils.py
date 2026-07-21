"""
Test stack naming helpers
"""

import infrastructure.constants as constants
from infrastructure.utils import get_monitoring_stack_name, get_stack_name


def test_stack_name_is_environment_prefixed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "staging")
    assert get_stack_name() == f"staging-{constants.PROJECT_NAME}"


def test_monitoring_stack_name_is_environment_prefixed(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "staging")
    assert get_monitoring_stack_name() == f"staging-monitoring-{constants.PROJECT_NAME}"


def test_stack_name_defaults_to_dev(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    assert get_stack_name() == f"dev-{constants.PROJECT_NAME}"


def test_monitoring_stack_name_defaults_to_dev(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    assert get_monitoring_stack_name() == f"dev-monitoring-{constants.PROJECT_NAME}"


def test_stack_names_are_distinct(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    assert get_stack_name() != get_monitoring_stack_name()
    # the monitoring stack must not be matched by a plain "<env>-<project>" lookup
    assert not get_monitoring_stack_name().startswith(get_stack_name())
