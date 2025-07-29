import json
from pathlib import Path

import pytest
import rule_engine

from .utils import check_values_in_list, ensure_list, load_yaml


class MarkerLocationFileNotFoundError(Exception): ...  # noqa: E701


class InvalidMarkerValueError(AssertionError): ...  # noqa: E701


class MissingMandatoryMarkerError(AssertionError): ...  # noqa: E701


class MissingDependencyMarkerError(AssertionError): ...  # noqa: E701


class FilterLocationFileNotFoundError(Exception): ...  # noqa: E701


class BadJSONFormatError(Exception): ...  # noqa: E701


class CoverageMarkers:
    COVERAGEMARKERS_ON_CONFIG_ATTR = "coveragemarkers_enabled"
    COVERAGEMARKERS_OFF_OPTION = "--disable-coveragemarkers"
    COVERAGEMARKERS_OFF_HELP = "Flag to disable coveragemarkers functionality."
    COVERAGEMARKERS_OFF_DEST = "coveragemarkers_disabled"
    MARKERS_LOCATION_HELP = "Yaml File location of marker specifications."
    MARKERS_LOCATION_OPTION = "--markers-location"
    MARKERS_LOCATION_INI_KEY = "MarkersLocation"
    MARKERS_LOCATION_DEST = "markerslocation"
    COVERAGEMARKERS_ALL_CONFIG_ATTR = "coveragemarkers"
    COVERAGEMARKERS_ITEM_ATTR = "coveragemarkers"

    def __init__(self):
        self.enabled = None

    def _is_coveragemarkers_enabled(self, *, config):
        if not hasattr(config, self.COVERAGEMARKERS_ON_CONFIG_ATTR):
            setattr(
                config,
                self.COVERAGEMARKERS_ON_CONFIG_ATTR,
                not config.option.coveragemarkers_disabled,
            )
        self.enabled = config.coveragemarkers_enabled

    def coveragemarker_pytest_addoption(self, *, group, parser):
        group.addoption(
            self.COVERAGEMARKERS_OFF_OPTION,
            action="store_true",
            dest=self.COVERAGEMARKERS_OFF_DEST,
            default=False,
            help=self.COVERAGEMARKERS_OFF_HELP,
        )

        group.addoption(
            self.MARKERS_LOCATION_OPTION,
            action="store",
            dest=self.MARKERS_LOCATION_DEST,
            help=self.MARKERS_LOCATION_HELP,
        )
        parser.addini(
            self.MARKERS_LOCATION_INI_KEY,
            help=self.MARKERS_LOCATION_HELP,
        )

    @staticmethod
    def update_mandatory_markers(*, config, marker):
        if marker.get("mandatory", False):
            mandatory_markers = set(getattr(config, "mandatory_markers", []))
            mandatory_markers.add(marker.get("name"))
            setattr(config, "mandatory_markers", list(mandatory_markers))

    @staticmethod
    def check_marker_dependencies(*, markers):
        all_marker_names = {name for name in markers.keys()}
        if not all_marker_names:
            return

        dep_names = set()
        for name, details in markers.items():
            dep_names.update(details.get("dependents", []))

        if not dep_names <= all_marker_names:
            missing = dep_names - all_marker_names
            raise MissingDependencyMarkerError(f"Missing Dependency Markers {missing}.")

    def coveragemarker_pytest_configure(self, *, config):
        self._is_coveragemarkers_enabled(config=config)
        if not self.enabled:
            return

        markers = getattr(config, self.COVERAGEMARKERS_ALL_CONFIG_ATTR, {})
        for _, details in markers.items():
            self._include_coveragemarker(marker=details, config=config)
            self.update_mandatory_markers(config=config, marker=details)

        for marker in self._get_known_coveragemarkers(config=config).get("markers", []):
            markers.update(self._include_coveragemarker(marker=marker, config=config))
            self.update_mandatory_markers(config=config, marker=marker)
        self.check_marker_dependencies(markers=markers)
        setattr(config, self.COVERAGEMARKERS_ALL_CONFIG_ATTR, markers)

    def coveragemarker_pytest_collectreport(self, *, report):
        """
        Record coverage marker details on each item in the collection report.
        This is so collect-only output shows cov markers too
        """
        for item in report.result:
            if not hasattr(item, self.COVERAGEMARKERS_ITEM_ATTR):
                setattr(item, self.COVERAGEMARKERS_ITEM_ATTR, {})
            for mark in item.iter_markers():
                if self._is_coverage_marker(marker=mark, config=item.config):
                    updates_ = self._reformat_coveragemarker(marker=mark)
                    existing = getattr(item, self.COVERAGEMARKERS_ITEM_ATTR)
                    existing.update(updates_)
                    setattr(item, self.COVERAGEMARKERS_ITEM_ATTR, existing)

    def check_for_mandatory_markers(self, *, request):
        if mandatory_markers := getattr(request.config, "mandatory_markers", False):
            marker_names = {mark.name for mark in request.node.iter_markers()}

            good = set(mandatory_markers) <= marker_names

            if not good:
                raise MissingMandatoryMarkerError(
                    f"Mandatory Markers {mandatory_markers} not found in "
                    f"{marker_names} on {request.node.name}"
                )

    def check_for_dependency_markers(self, *, request):
        applied_markers = [mark.name for mark in request.node.iter_markers()]
        for mark in applied_markers:
            try:
                deps = request.config.coveragemarkers[mark].get("dependents", None)
                if deps:
                    for dep in deps:
                        if dep not in applied_markers:
                            raise MissingDependencyMarkerError(
                                f"Missing Dependency Marker {dep}"
                            )
            except KeyError:
                # Not a CoverageMarker marker
                pass

    def validate_marker_values(self, *, request):
        for mark in request.node.iter_markers():
            if not self._is_coverage_marker(marker=mark, config=request.config):
                break

            allowed_values = request.config.coveragemarkers.get(mark.name, {}).get(
                "allowed", []
            )

            # no allowed_value so let everything through
            if not allowed_values:
                continue

            marker_args = self._reformat_coveragemarker_args(marker=mark)

            if not check_values_in_list(
                source_value=marker_args, allowed_values=allowed_values
            ):
                raise InvalidMarkerValueError(
                    "{} on {}: {} not in {}".format(
                        mark.name, request.node.name, marker_args, allowed_values
                    )
                )

        self.check_for_mandatory_markers(request=request)
        self.check_for_dependency_markers(request=request)

    def update_test_with_coveragemarkers(self, *, items):
        """
        Loop through all test items and update their metadata
        """

        for item in items:
            if not hasattr(item, self.COVERAGEMARKERS_ITEM_ATTR):
                item.coveragemarkers = {}
            for mark in item.iter_markers():
                if self._is_coverage_marker(marker=mark, config=item.config):
                    updates_ = self._reformat_coveragemarker(marker=mark)
                    item.coveragemarkers.update(updates_)
            # output to json report
            content = json.dumps(item.coveragemarkers)
            item.add_report_section("setup", "_metadata", content)

    def get_coveragemarkers_from_test(self, *, item):
        return (
            {"coveragemarkers": item.coveragemarkers}
            if hasattr(item, self.COVERAGEMARKERS_ITEM_ATTR)
            else {}
        )

    def _get_supplied_marker_location(self, *, config):
        try:
            return (
                config.getoption(self.MARKERS_LOCATION_OPTION)
                or config.getini(self.MARKERS_LOCATION_INI_KEY)
                or None
            )
        except (KeyError, ValueError):
            return None

    @staticmethod
    def _get_marker_location_path(*, config, location):
        # was absolute path provided
        location_file = Path(location)
        if location_file.is_file():
            return str(location_file)

        # no luck so far so lets try adding root_dir to location
        location_file = Path(config.rootdir) / location
        if location_file.is_file():
            return str(location_file)

        # third time lucky
        location_file = Path(config.rootdir) / "pytest_coveragemarkers" / location
        if location_file.is_file():
            return str(location_file)

        raise MarkerLocationFileNotFoundError(location)

    def _get_marker_path_from_location(self, *, config):
        location = self._get_supplied_marker_location(config=config)
        if location:
            return self._get_marker_location_path(config=config, location=location)

    def _get_known_coveragemarkers(self, *, config):
        markers_spec = dict()
        markers_location = self._get_marker_path_from_location(config=config)
        if markers_location:
            load_yaml(markers_spec, markers_location)
        return markers_spec

    def _include_coveragemarker(self, *, marker, config):
        if marker_name := marker.get("name", ""):
            config.addinivalue_line("markers", marker_name)
            return {marker_name: marker}
        return {}

    def _reformat_coveragemarker_args(self, *, marker):
        """
        Processes the args supplied to a fixture in order to return a simplified
        list containing the args

        """
        simplified = []
        marker_args = ensure_list(marker.args)

        for arg in marker_args:
            if arg:
                if isinstance(arg, list):
                    simplified.extend(arg)
                else:
                    simplified.append(arg)
        if not isinstance(simplified, list):
            # single value so wrap in list
            simplified = [simplified]
        return simplified

    def _reformat_coveragemarker(self, *, marker):
        arguments = {}
        for val in self._reformat_coveragemarker_args(marker=marker):
            arguments[val] = True
        return {marker.name: arguments}

    def _is_coverage_marker(self, *, marker, config):
        if not self._is_coveragemarkers_enabled:
            return False

        if marker.name in list(config.coveragemarkers.keys()):
            return True
        return False

    def merge_multiple_marker_yaml(self, *, config, other_yaml_filepath: str):
        markers = self._get_known_coveragemarkers(config=config)

        other_yaml_file = self._get_marker_location_path(
            config=config, location=other_yaml_filepath
        )
        load_yaml(markers, other_yaml_file)

        markers = {m["name"]: m for m in markers.get("markers")}
        setattr(config, self.COVERAGEMARKERS_ALL_CONFIG_ATTR, markers)


class CoverageMarkersFilter:
    FILTER_OPTION = "--marker-filter"
    FILTER_DEST = "markerfilter"
    FILTER_HELP = "Filtering of tests by coverage marker."
    FILTER_LOCATION_OPTION = "--filter-location"
    FILTER_LOCATION_INI_KEY = "FilterLocation"
    FILTER_LOCATION_DEST = "filterlocation"
    FILTER_LOCATION_HELP = "JSON File location of filter specifications."

    def filtering_pytest_addoption(self, *, group, parser):
        group.addoption(
            self.FILTER_OPTION,
            action="store",
            dest=self.FILTER_DEST,
            help=self.FILTER_HELP,
        )

        group.addoption(
            self.FILTER_LOCATION_OPTION,
            action="store",
            dest=self.FILTER_LOCATION_DEST,
            help=self.FILTER_LOCATION_HELP,
        )
        parser.addini(
            self.FILTER_LOCATION_INI_KEY,
            help=self.FILTER_LOCATION_HELP,
        )

    def apply_filter_rule(self, *, config, items):
        if not config.coveragemarkers_enabled:
            return

        not_in_group = pytest.mark.skip(
            reason="Test failed to meet filter rule criteria"
        )

        if filter_spec := self._get_marker_filter(config=config):
            for item in items:
                if not self._check_rules(
                    rule_spec=filter_spec, data=item.coveragemarkers
                ):
                    item.add_marker(not_in_group)

    def _get_supplied_filter(self, *, config):
        return config.getoption(self.FILTER_OPTION) or None

    def _get_supplied_filter_location(self, *, config):
        try:
            return (
                config.getoption(self.FILTER_LOCATION_OPTION)
                or config.getini(self.FILTER_LOCATION_INI_KEY)
                or None
            )
        except (KeyError, ValueError):
            return None

    @staticmethod
    def _get_marker_filter_path(*, config, location):
        if not location:
            return

        # was absolute path provided
        filter_file = Path(location)
        if filter_file.is_file():
            return str(filter_file)

        # no luck so far so lets try adding root_dir to location
        filter_file = Path(config.rootdir) / location
        if filter_file.is_file():
            return str(filter_file)

        # third time lucky
        filter_file = Path(config.rootdir) / "pytest_coveragemarkers" / location
        if filter_file.is_file():
            return str(filter_file)

        raise FilterLocationFileNotFoundError(location)

    def _get_marker_filter_from_location(self, *, config, location):
        filter_location = self._get_marker_filter_path(config=config, location=location)
        with Path(filter_location).open(encoding="UTF-8") as source:
            try:
                return json.load(source)  # TODO: filter files no longer in json?
            except json.decoder.JSONDecodeError as exc:
                raise BadJSONFormatError(
                    f"Failed to load JSON from: {location}"
                ) from exc

    def _get_marker_filter(self, config):
        if marker_filter := self._get_supplied_filter(config=config):
            return marker_filter
        if filter_location := self._get_supplied_filter_location(config=config):
            return self._get_marker_filter_from_location(
                config=config, location=filter_location
            )

    def filtering_pytest_report_header(self, config):
        if marker_filter := self._get_supplied_filter(config=config):
            return f"Marker Filter: {marker_filter}"

    @staticmethod
    def _rule(*, spec: str):
        context = rule_engine.Context(default_value=[])
        rule = rule_engine.Rule(spec, context=context)
        return rule

    def _check_rules(self, rule_spec: str, data: dict) -> bool:
        return self._rule(spec=rule_spec).matches(data)
