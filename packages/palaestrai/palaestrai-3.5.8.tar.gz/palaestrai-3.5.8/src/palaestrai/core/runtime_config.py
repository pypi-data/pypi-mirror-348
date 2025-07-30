from __future__ import annotations

import logging
from io import TextIOWrapper
from os import getcwd
from pathlib import Path
from typing import Any, Dict, Union, TextIO

import appdirs
import ruamel.yaml

LOG = logging.getLogger(__name__)


class DebugLogFilter:
    """Only allows debug messages; works as a filter for the debug_handler"""

    def __call__(self, log_message):
        if log_message.levelno == logging.DEBUG:
            return True
        else:
            return False


class _RuntimeConfig:
    """Application-wide runtime configuration.

    This singleton class provides an application-wide runtime configuration
    and transparently hides all sources from the rest of the application.
    """

    CONFIG_FILE_PATHS = [
        "%s/runtime-conf.yaml"
        % appdirs.site_config_dir("palaestrai", "OFFIS"),
        "%s/runtime-conf.yaml"
        % appdirs.user_config_dir("palaestrai", "OFFIS"),
        "%s/palaestrai.conf" % getcwd(),
        "%s/palaestrai-runtime.conf.yaml" % getcwd(),
        "%s/runtime.conf.yaml" % getcwd(),
    ]
    DEFAULT_CONFIG = {
        "store_uri": "sqlite:///palaestrai.db",
        "time_series_store_uri": "influx+localhost:8086",
        "store_buffer_size": 20,
        "data_path": "./_outputs",
        "broker_uri": "ipc://*",
        "executor_bus_port": 4242,
        "logger_port": 4243,
        "public_bind": False,
        "major_domo_client_timeout": 300_000,
        "major_domo_client_retries": 3,
        "fork_method": "spawn",
        "logging": {
            "version": 1,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(name)s[%(process)d]: "
                    "%(levelname)s - %(message)s"
                },
                "debug": {
                    "format": "%(asctime)s %(name)s[%(process)d]: "
                    "%(levelname)s - %(message)s (%(module)s.%(funcName)s "
                    "in %(filename)s:%(lineno)d)"
                },
                "terminal": {
                    "class": "palaestrai.cli.terminal_formatter.TerminalFormatter",
                },
            },
            "filters": {
                "debug_filter": {
                    "()": "palaestrai.core.runtime_config.DebugLogFilter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout",
                },
                "console_debug": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "debug",
                    "filters": ["debug_filter"],
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "palaestrai.agent": {"level": "ERROR"},
                "palaestrai.agent.brain": {"level": "ERROR"},
                "palaestrai.agent.muscle": {"level": "ERROR"},
                "palaestrai.agent.agent_conductor": {"level": "ERROR"},
                "palaestrai.core": {"level": "ERROR"},
                "palaestrai.experiment": {"level": "ERROR"},
                "palaestrai.store": {"level": "ERROR"},
                "palaestrai.environment": {"level": "ERROR"},
                "palaestrai.simulation": {"level": "ERROR"},
                "palaestrai.types": {"level": "ERROR"},
                "palaestrai.util": {"level": "ERROR"},
                "palaestrai.visualization": {"level": "ERROR"},
                "sqlalchemy.engine": {"level": "ERROR"},
            },
            "root": {
                "level": "ERROR",
                "handlers": ["console", "console_debug"],
            },
        },
        "profile": False,
    }
    _instance = None

    def __init__(self):
        self._config_file_path = None
        self.config_search_path = _RuntimeConfig.CONFIG_FILE_PATHS
        # The loaded configuration is what RuntimeConfig.load gave us. It
        # remains immutable after loading.
        self._loaded_configuration = {}

    def _get(self, key: str, default=None, exception=None) -> Any:
        """Retrieves a config key

        Retrieves any config key; if not set, it queries the config dictionary;
        if it isn't present there, it returns the given default value. It also
        sets the value in the current object as a side-effect.
        """
        lkey = "_%s" % key
        if lkey not in self.__dict__:
            try:
                self.__dict__[lkey] = self._loaded_configuration[key]
            except KeyError:
                if default:
                    self.__dict__[lkey] = default
                else:
                    self.__dict__[lkey] = _RuntimeConfig.DEFAULT_CONFIG[key]
                if exception:
                    raise KeyError(exception)
        return self.__dict__[lkey]

    def reset(self):
        """Resets the runtime configuration to empty state"""
        for key in list(self._loaded_configuration.keys()) + list(
            _RuntimeConfig.DEFAULT_CONFIG.keys()
        ):
            try:
                del self.__dict__[f"_{key}"]
            except KeyError:
                pass
        self._loaded_configuration = {}
        self._config_file_path = None

    @property
    def logging(self) -> Dict:
        """Configuration of all subsystem loggers

        The logging configuration determines how palaestrAI outputs its
        state information.
        The built-in configuration doesn't give much output except for
        warnings and errors (which is akin to the Unix philosophy).
        However, the log level of individual modules can be increased to,
        e.g., ``INFO``.

        The configuration is based on the Python ``logging`` module. Thus,
        generation information can be obtained from
        `Python's official documentation on logging <https://docs.python.org/3/library/logging.config.html#logging-config-dictschemia>`_.

        Returns
        -------
        dict
            The logging configuration

        Examples
        --------

        ``palaestrai runtime-config-show-default`` gives a complete,
        sane default logging config. To get a more colorful output, change it
        to::

            logging:
              version: 1
              root:
                handlers: [console]
                level: ERROR
              filters:
                debug_filter: {(): palaestrai.core.runtime_config.DebugLogFilter}
              formatters:
                debug: {format: '%(asctime)s %(name)s[%(process)d]: %(levelname)s - %(message)s
                    (%(module)s.%(funcName)s in %(filename)s:%(lineno)d)'}
                simple: {format: '%(asctime)s %(name)s[%(process)d]: %(levelname)s - %(message)s'}
                terminal: {class: palaestrai.cli.terminal_formatter.TerminalFormatter}
              handlers:
                console:
                  class: logging.StreamHandler
                  formatter: terminal
                  level: DEBUG
                  stream: 'ext://sys.stdout'
                console_debug:
                  class: logging.StreamHandler
                  filters: [debug_filter]
                  formatter: debug
                  level: DEBUG
                  stream: ext://sys.stdout
              loggers:
                palaestrai.agent: {level: ERROR}
                palaestrai.agent.agent_conductor: {level: INFO}
                palaestrai.agent.brain: {level: INFO}
                palaestrai.agent.muscle: {level: INFO}
                palaestrai.core: {level: INFO}
                palaestrai.environment: {level: INFO}
                palaestrai.experiment: {level: INFO}
                palaestrai.simulation: {level: INFO}
                palaestrai.store: {level: ERROR}
                palaestrai.types: {level: ERROR}
                palaestrai.util: {level: ERROR}
                palaestrai.visualization: {level: ERROR}
                sqlalchemy.engine: {level: ERROR}
        """
        return self._get(
            "logging",
            exception="Sorry, no logging config in the config file",
        )

    @property
    def time_series_store_uri(self) -> str:
        """URI to the time series database for results

        This must be any standards-compliant string in the form of
        `influxdb+user:password@host-or-path:port/db`. For example,
        `elasticsearch+myuser:mypass@localhost/arl`.

        Returns
        -------

        """
        return self._get("time_series_store_uri")

    @property
    def store_uri(self) -> str:
        """URI to the store database for results

        This must be any standards-compliant string in the form of
        `transport://user:password@host-or-path:port/db`. For example,
        `postgresql://myuser:mypass@localhost/arl`.

        Returns
        -------
        str
            The connection string; default: ``sqlite:///palaestrai.db``

        Example
        -------
        ``store_uri: postgresql://palaestrai:Password@localhost:5432/arl``
        """
        return self._get("store_uri")

    @property
    def store_buffer_size(self) -> int:
        """Number of messages buffered before writing to the store

        palaestrAI buffers data before flushing it in bulk to the store.
        This number defines a factor; the number of messages being buffered
        is a multiple of the number of agents and number of environments,
        for technical reasons.

        Writing data in bulk to the database makes the results storage more
        efficient.
        However, caching too many messages before writing will also increase
        the local memory consumption.
        To find a balance, the number is user-configurable.
        The number of messages cached is equal to
        number_of_workers * number_of_environments * store_buffer_size

        Returns
        -------
        int
            Multiplied for the storage buffer, default: 20

        Example
        -------
        ``store_buffer_size: 10``
        """
        return self._get("store_buffer_size")

    @property
    def data_path(self) -> Path:
        """File system path for data storage

        Although the results storage database is the main system for
        storing any result the comes out of a palaestrAI run,
        some data is also dumped to the local disk, either for convenience
        or as backup. A common example are brain dumps (i.e., trained
        agent models).

        Returns
        -------

        pathlib.Path
            The data path, default: ``./_outputs``

        Example
        -------

        ``data_path: /home/myself/palaestrai/results``
        """
        return Path(self._get("data_path"))

    @property
    def broker_uri(self) -> str:
        """Full URI to the Major Domo Protocol broker

        palaestrAI is based on message passing. All subsystems communicate
        with each other through a architecture that is based on the ZeroMQ
        Major Domo Protocol. This architecture uses a central broker to
        route messagees between subsystems.

        This property retrives the full connect URI of the broker.
        It can be explicitly set in the runtime configuration; if not, it is
        derived from :py:attr:`executor_bus_port` and
        :py:attr:`public_bind` properties. The following values are
        recognized by palaestrAI:

        ``broker_uri: ~`` (i.e., ``None``)
            Derives from :py:attr:`executor_bus_port` and
            :py:attr:`public_bind`. If ``public_bind: False``
            (the default), then the broker URI will be
            ``tcp://127.0.0.1:4242``.
        ``broker_uri: tcp://``
            Instructs the major domo broker to pick a random free port.
            Uses :py:attr:`public_bind` to determine whether the broker
            binds to localhost or to all available interfaces.
            Equivalent to ``tcp://*:*``.
        ``broker_uri: tcp://*:4242``
            Explicitly instructs the major domo broker to bind to the given
            port 4242 on all available interfaces.
        ``broker_uri: ipc://``
            Lets the major domo broker pick a random file in a temporary
            directory to use the inter-process communication protocol instead
            of TCP. Ignores the settings in :py:attr:`executor_bus_port`
            and :py:attr:`public_bind`. Equivalent to ``ipc://*``.
        ``broker_uri: ipc:///some/file``
            Explicitly sets a file for IPC transport.

        If the ``broker_uri`` property is set, it overwrites the effects of
        setting :py:attr:`executor_bus_port` and
        :py:attr:`public_bind`.

        Examples
        --------

        The default sets ``public_bind: False``
        and ``executor_bus_port: 4242`` in the runtime config, which creates
        the broker URI ``tcp://127.0.0.1:4242``. This is equivalent to
        creating the following runtime config file entry::

            broker_uri: tcp://127.0.0.1:4242
        """
        address_part = "*" if self.public_bind else "127.0.0.1"
        default_uri = f"tcp://{address_part}:{self.executor_bus_port}"
        uri = self._get("broker_uri", default=default_uri) or default_uri
        self._broker_uri = uri
        return uri

    @broker_uri.setter
    def broker_uri(self, broker_uri: str):
        self.__dict__["_broker_uri"] = broker_uri

    @property
    def executor_bus_port(self) -> int:
        """Port of the executor's messaging bus

        palaestrai needs one bus to start it all, which is managed by the
        executor. All other buses and topics can be communicated over this
        initial bus.

        Returns
        -------

        int
            The bus port; default: 4242

        Example
        -------

        ``executor_bus_port: 4242``
        """
        return self._get("executor_bus_port")

    @property
    def public_bind(self) -> bool:
        """Indicates whether to bind to all public adresses or to localhost

        This configuration setting allows the Executor and all other message
        buses to bind to all public IP addresses if set to True. If not,
        the buses will bind to ``127.0.0.1`` only`.

        Finer-grained control can be excerted by the :py:attr:`broker_uri`
        option, which overwrites whatever setting is made here.

        Returns
        -------

        bool
            If True, the major domo broker binds to all available IP
            addresses. The default is False.

        Example
        -------

        ``public_bind: False``
        """
        return self._get("public_bind")

    @property
    def profile(self) -> bool:
        """Whether to enable profiling or not.

        If enabled, executions of palaestrAI create profiling information in
        ``.prof`` files. This can be important for hunting performance bugs
        and is usually enabled by developers, but not by end users.
        Profiling is based on
        `Python's cProfile module <https://docs.python.org/3/library/profile.html>`_
        and the resulting files can be inspected with tools like
        `Snakeviz <https://jiffyclub.github.io/snakeviz/>`_.

        Returns
        -------

        bool
            If True, profiling is enabled and ``.prof`` files are generated;
            if False, nothing is additionally done.
        """
        return self._get("profile")

    @property
    def major_domo_client_timeout(self) -> int:
        """Timeout used by the MajorDomoClient

        Returns
        -------

        int
            The timeout, in seconds
        """
        return self._get("major_domo_client_timeout")

    @property
    def major_domo_client_retries(self) -> int:
        """Number of connection attempts the major domo client will try

        Returns
        -------

        int
            The number of (re-) tries
        """
        return self._get("major_domo_client_retries")

    @property
    def fork_method(self) -> str:
        """The method for forking child processes palaestrAI should use

        palaestrAI creates a number of subprocesses when it runs.
        Python offers several ways to create new processes. The safest is
        to use the ``spawn`` method, which is the default.
        However, other methods like ``fork`` and ``forkserver`` offer higher
        speed, but are not available on every platform.

        The recommended way is to leave it at ``spawn`` unless you are
        running on a Linux system, e.g., in a docker container.
        Then, ``forkserver`` can offer you a performance boost.
        For more details, see the offical Python documentation on
        `start methods <https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods>`_.

        Returns
        -------

        str
            Either ``spawn``, ``fork``, or ``forkserver``. If the value set
            in the loadable runtime config is not any of these strings, the
            default method of ``spawn`` is returned. Default: ``spawn``.

        """
        method = self._get("fork_method")
        if not any(
            method == x
            for x in (
                "fork",
                "forkserver",
                "spawn",
            )
        ):
            method = "spawn"
        return method

    @property
    def logger_port(self) -> int:
        """Destination port the internal log server should use

        All spawned submodules of palaestrAI communicate their log messages
        back to the main process. This log message receiver binds to the given
        port.

        Returns
        -------

        int
            The port of the internal log server, default: 4243

        Example
        -------

        ``logger_port: 4243``
        """
        return self._get("logger_port")

    def load(
        self, stream_or_dict: Union[dict, TextIO, str, Path, None] = None
    ):
        """Loads the configuration from an external source.

        The runtime configuration is initialized from the default configuration
        in ::`_RuntimeConfig.DEFAULT_CONFIG`. This method then iterates through
        the list in ::`_RuntimeConfig.CONFIG_FILE_PATHS`, subsequently updating
        the existing configuration with new values found. Finally, the given
        ::`stream_or_dict` parameter is used if present, ultimately taking
        preference over all other values.

        That means that each config file can contain only a portion of the
        overall configuration; it gets updated subsequently.

        Parameters
        ----------

        stream_or_dict : Union[dict, TextIO, str, Path, None]
            Loads the runtime configuration directly from a dictionary or as
            YAML-encoded stream. If no stream is given, the default files in
            :py:attr:`_RuntimeConfig.CONFIG_FILE_PATHS`
            will be tried as described.

        Examples
        --------

        ``RuntimeConfig().load()``
            Will initialize the runtime configuration from the default
            configuration, and then try all available configuration files.
            The configuration is updated in a cascading manner.

        ``RuntimeConfig.load({"store_uri": "sqlite:///test.db"})``
            Loads the complete configuration is above, but additionally
            overwrites the ``store_uri`` parameter, setting it to
            ``sqlite:///test.db``.
        """

        if not isinstance(self._loaded_configuration, dict):
            self._loaded_configuration = {}
        if not stream_or_dict and len(self._loaded_configuration) > 0:
            # Don't load a default config if we already have something; use
            # reset() instead.
            return

        yml = ruamel.yaml.YAML(typ="safe")
        has_seen_nondefault_config = False
        self._loaded_configuration.update(_RuntimeConfig.DEFAULT_CONFIG)

        for file in _RuntimeConfig.CONFIG_FILE_PATHS:
            try:
                LOG.debug("Trying to open configuration file: %s", file)
                with open(file, "r") as fp:
                    deserialized = yml.load(fp)
                    if not isinstance(deserialized, dict):
                        LOG.warning(
                            "The contents of %s could not be deserialized "
                            "to dict, skipping it.",
                            file,
                        )
                        continue
                    self._loaded_configuration.update(deserialized)
                    self._config_file_path = file
                    has_seen_nondefault_config = True
            except IOError:
                continue

        if isinstance(stream_or_dict, dict):
            self._loaded_configuration.update(stream_or_dict)
            self._config_file_path = "(dict)"
            return

        if isinstance(stream_or_dict, str):
            stream_or_dict = Path(stream_or_dict)
        if isinstance(stream_or_dict, Path):
            try:
                stream_or_dict = open(stream_or_dict, "r")
            except OSError:
                LOG.warning(
                    "Failed to load runtime configuration from file at %s, "
                    "ignoring.",
                    stream_or_dict,
                )
        if stream_or_dict is not None:
            try:
                deserialized = yml.load(stream_or_dict)  # Can raise
                if not isinstance(deserialized, dict):
                    raise TypeError
                self._loaded_configuration.update(deserialized)
                try:
                    self._config_file_path = stream_or_dict.name
                except AttributeError:
                    self._config_file_path = str(stream_or_dict)
                has_seen_nondefault_config = True
            except TypeError:
                LOG.warning(
                    "Failed to load runtime configuration from stream "
                    'at "%s", ignoring.',
                    repr(stream_or_dict),
                )
            finally:
                if isinstance(stream_or_dict, TextIOWrapper):
                    stream_or_dict.close()

        if not has_seen_nondefault_config:
            LOG.info(
                "No runtime configuration given, loaded built-in defaults."
            )
            self._config_file_path = "(DEFAULT)"

    def to_dict(self) -> Dict:
        return {key: self._get(key) for key in _RuntimeConfig.DEFAULT_CONFIG}

    def __str__(self):
        return "<RuntimeConfig id=0x%x> at %s" % (
            id(self),
            self._config_file_path,
        )

    def __repr__(self):
        return str(self.to_dict())


def RuntimeConfig():
    """RuntimeConfig singleton instance

    Provides API access to palaestrAI's runtime configuration.
    At any time, the configuration is fed from one singleton instance.
    """
    if _RuntimeConfig._instance is None:
        _RuntimeConfig._instance = _RuntimeConfig()
        try:
            _RuntimeConfig._instance.load()
        except FileNotFoundError:
            from copy import deepcopy

            _RuntimeConfig._instance._loaded_configuration = deepcopy(
                _RuntimeConfig.DEFAULT_CONFIG
            )
    return _RuntimeConfig._instance
