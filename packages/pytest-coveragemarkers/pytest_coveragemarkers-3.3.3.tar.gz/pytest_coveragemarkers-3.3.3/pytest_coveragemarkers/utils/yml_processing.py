import codecs
import os
import re

from .checks import merge_dict

ENV_TAG = "!ENV"
ENV_PATTERN = re.compile(r".*?\${(\w+)}.*?")
FILE_TAG = "!YML"


def parse_config(path=None, encoding="UTF-8", data=None):
    """
    Load a yaml configuration file and resolve any environment variables.

    The environment variables must have !ENV before them and be in this format
    to be parsed: ${VAR_NAME}.
    E.g.:
    database:
        host: !ENV ${HOST}
        port: !ENV ${PORT}
    app:
        log_path: !ENV "/var/${LOG_PATH}"
        something_else: !ENV "${AWESOME_ENV_VAR}/var/${A_SECOND_AWESOME_VAR}"
    :param str path: the path to the yaml file
    :param str encoding: string encoding value
    :param str data: the yaml data itself as a stream
    :return: the dict configuration
    :rtype: dict[str, T]
    """
    try:
        import yaml
    except ImportError:
        raise Exception("unable to import YAML package. Can not continue.")

    loader = yaml.SafeLoader

    # the tag will be used to mark where to start searching for the pattern
    # e.g. somekey: !ENV somestring${MYENVVAR}blah blah blah
    loader.add_implicit_resolver(ENV_TAG, ENV_PATTERN, None)

    loader.add_constructor(ENV_TAG, constructor_env_variables)
    loader.add_constructor(FILE_TAG, constructor_file_includer)

    if path:
        with codecs.open(os.path.expanduser(path), "r", encoding) as conf_data:
            return yaml.load(conf_data, Loader=loader)
    elif data:
        return yaml.load(data, Loader=loader)
    else:
        raise ValueError("Either a path or data should be defined as input")


def constructor_env_variables(loader, node):
    """
    Extract the environment variable from the node's value.

    :param yaml.Loader loader: the yaml loader
    :param node: the current node in the yaml
    :return: the parsed string that contains the value of the environment
    variable
    """
    value = loader.construct_scalar(node)
    match = ENV_PATTERN.findall(value)  # to find all env variables in line
    if match:
        for g in match:
            value = value.replace(f"${{{g}}}", os.environ.get(g, ""))
        if value.startswith(f"{ENV_TAG} "):
            value = value[len(ENV_TAG) + 1:]  # fmt: skip
    return value


def constructor_file_includer(loader, node):
    """
    Extract the name of the file from the node's value.

    :param yaml.Loader loader: the yaml loader
    :param node: the current node in the yaml
    :return: the parsed string that contains the value of the environment
    variable
    """
    value = loader.construct_scalar(node)
    if ENV_TAG in value:
        value = constructor_env_variables(loader, node)

    marker_filepath = os.path.dirname(node.start_mark.name)
    file_to_load = os.path.join(marker_filepath, value)
    if os.path.isfile(file_to_load):
        return parse_config(path=file_to_load)
    raise Exception(f"file {file_to_load} does not exist")


def flatten_markers(markers):
    flattened_marks = list()
    for marker in markers.get("markers"):
        if isinstance(marker, list):
            for mark in marker:
                flattened_marks.append(mark)
        else:
            flattened_marks.append(marker)
    return {"markers": flattened_marks}


def load_yaml(config, yaml_file, encoding="UTF-8"):
    """Load the passed in yaml configuration file."""

    parsed_config = parse_config(path=yaml_file, encoding=encoding)
    parsed_config = flatten_markers(parsed_config)

    merge_dict(config, parsed_config)
