def _can_use_ddtrace() -> bool:
    try:
        from ddtrace import __version__ as version

        # allow ddtrace 2.6+ to be used
        return version.startswith("2.") and version[2].isdigit() and int(version[2]) >= 6
    except Exception:
        return False


def _can_use_datadog_statsd() -> bool:
    try:
        from datadog.dogstatsd.base import statsd

        _ = statsd
        return True
    except ImportError:
        return False


can_use_ddtrace = _can_use_ddtrace()
can_use_datadog_statsd = _can_use_datadog_statsd()
