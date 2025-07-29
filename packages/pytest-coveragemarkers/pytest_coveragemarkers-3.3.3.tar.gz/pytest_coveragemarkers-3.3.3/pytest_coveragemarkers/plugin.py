import pytest

from .coveragemarkers import CoverageMarkers, CoverageMarkersFilter

PLUGIN_GROUP = "coveragemarkers"
CM = CoverageMarkers()
CMF = CoverageMarkersFilter()


def pytest_addoption(parser):
    group = parser.getgroup(PLUGIN_GROUP)

    CMF.filtering_pytest_addoption(group=group, parser=parser)
    CM.coveragemarker_pytest_addoption(group=group, parser=parser)


def pytest_configure(config):
    CM.coveragemarker_pytest_configure(config=config)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    if config.coveragemarkers_enabled:
        CM.update_test_with_coveragemarkers(items=items)
        CMF.apply_filter_rule(config=config, items=items)


@pytest.hookimpl(tryfirst=True)
def pytest_collectreport(report):
    """
    Record coverage marker details on each item in the collection report.
    This is so collect-only output shows cov markers too
    """
    CM.coveragemarker_pytest_collectreport(report=report)


@pytest.mark.optionalhook
def pytest_json_runtest_metadata(item):
    return CM.get_coveragemarkers_from_test(item=item)


@pytest.fixture(autouse=True)
def cov_markers(request):
    if request.config.coveragemarkers_enabled:
        CM.validate_marker_values(request=request)
