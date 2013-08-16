===============================
The gocept.logging distribution
===============================


This package is compatible with Python version 2.7 and 3.3.


Setup with ini file
===================

::

    [loggers]
    keys = root

    [handlers]
    keys = console, syslog

    [formatters]
    keys = generic, keyvalue

    [logger_root]
    level = INFO
    handlers = console, syslog

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(asctime)s %(levelname)-5.5s %(name)s: %(message)s

    [handler_syslog]
    class = logging.handlers.SysLogHandler
    args = ()
    formatter = keyvalue

    [formatter_keyvalue]
    class = gocept.logging.SyslogKeyValueFormatter


Setup with ZConfig
==================

::

    <eventlog>
      <logfile>
        formatter zope.exceptions.log.Formatter
        format %(asctime)s %(levelname)-5.5s %(name)s: %(message)s
        path STDOUT
      </logfile>
      <syslog>
        formatter gocept.logging.SyslogKeyValueFormatter
      </syslog>
    </eventlog>


Corresponding syslog configuration
==================================

rsyslog::

    $EscapeControlCharactersOnReceive off
    $MaxMessageSize 64k
    user.* @localhost:5140

