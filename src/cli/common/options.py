"""
Click options which are common across CLI tools.
"""

from pathlib import Path
from typing import Any, Callable, Dict, Union

import click
import yaml

from .validators import validate_path_is_directory, validate_path_pair


def _validate_dcos_configuration(
    ctx: click.core.Context,
    param: Union[click.core.Option, click.core.Parameter],
    value: Union[int, bool, str],
) -> Dict[str, Any]:
    """
    Validate that a given value is a file containing a YAML map.
    """
    # We "use" variables to satisfy linting tools.
    for _ in (ctx, param):
        pass

    if value is None:
        return {}

    content = Path(str(value)).read_text()

    try:
        return dict(yaml.load(content) or {})
    except ValueError:
        message = '"{content}" is not a valid DC/OS configuration'.format(
            content=content,
        )
    except yaml.YAMLError:
        message = '"{content}" is not valid YAML'.format(content=content)

    raise click.BadParameter(message=message)


def masters_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An option decorator for the number of masters.
    """
    function = click.option(
        '--masters',
        type=click.INT,
        default=1,
        show_default=True,
        help='The number of master nodes.',
    )(command)  # type: Callable[..., None]
    return function


def agents_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An option decorator for the number of agents.
    """
    function = click.option(
        '--agents',
        type=click.INT,
        default=1,
        show_default=True,
        help='The number of agent nodes.',
    )(command)  # type: Callable[..., None]
    return function


def public_agents_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An option decorator for the number of agents.
    """
    function = click.option(
        '--public-agents',
        type=click.INT,
        default=1,
        show_default=True,
        help='The number of public agent nodes.',
    )(command)  # type: Callable[..., None]
    return function


def extra_config_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An option decorator for supplying extra DC/OS configuration options.
    """
    function = click.option(
        '--extra-config',
        type=click.Path(exists=True),
        callback=_validate_dcos_configuration,
        help=(
            'The path to a file including DC/OS configuration YAML. '
            'The contents of this file will be added to add to a default '
            'configuration.'
        ),
    )(command)  # type: Callable[..., None]
    return function


def workspace_dir_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An option decorator for the workspace directory.
    """
    help_text = (
        'Creating a cluster can use approximately 2 GB of temporary storage. '
        'Set this option to use a custom "workspace" for this temporary '
        'storage. '
        'See '
        'https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir '
        'for details on the temporary directory location if this option is '
        'not set.'
    )
    function = click.option(
        '--workspace-dir',
        type=click.Path(exists=True),
        callback=validate_path_is_directory,
        help=help_text,
    )(command)  # type: Callable[..., None]
    return function


def artifact_argument(command: Callable[..., None]) -> Callable[..., None]:
    """
    An argument decorator for a DC/OS artifact.
    """
    function = click.argument(
        'artifact',
        type=click.Path(exists=True),
    )(command)  # type: Callable[..., None]
    return function


def variant_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An argument decorator for a DC/OS variant.
    """
    function = click.option(
        '--variant',
        type=click.Choice(['auto', 'oss', 'enterprise']),
        default='auto',
        help=(
            'Choose the DC/OS variant. '
            'If the variant does not match the variant of the given artifact, '
            'an error will occur. '
            'Using "auto" finds the variant from the artifact. '
            'Finding the variant from the artifact takes some time and so '
            'using another option is a performance optimization.'
        ),
    )(command)  # type: Callable[..., None]
    return function


def license_key_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An argument decorator for passing a license key.
    """
    function = click.option(
        '--license-key',
        type=click.Path(exists=True),
        envvar='DCOS_LICENSE_KEY_PATH',
        help=(
            'This is ignored if using open source DC/OS. '
            'If using DC/OS Enterprise, this defaults to the value of the '
            '`DCOS_LICENSE_KEY_PATH` environment variable.'
        ),
    )(command)  # type: Callable[..., None]
    return function


def security_mode_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An argument decorator for the DC/OS Enterprise security mode.
    """
    function = click.option(
        '--security-mode',
        type=click.Choice(['disabled', 'permissive', 'strict']),
        help=(
            'The security mode to use for a DC/OS Enterprise cluster. '
            'This overrides any security mode set in ``--extra-config``.'
        ),
    )(command)  # type: Callable[..., None]
    return function


def copy_to_master_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    An argument decorator for copying files to master nodes before installing
    DC/OS.
    """
    function = click.option(
        '--copy-to-master',
        type=str,
        callback=validate_path_pair,
        multiple=True,
        help=(
            'Files to copy to master nodes before installing DC/OS. '
            'This option can be given multiple times. '
            'Each option should be in the format '
            '/absolute/local/path:/remote/path.'
        ),
    )(command)  # type: Callable[..., None]
    return function
