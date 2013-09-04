==============
gocept.logging
==============

.. contents::
   :depth: 2

This package provides infrastructure for semi-structured log messages.

This means appending easily parseable information after the free-text log
message to facilitate analysis of the logs later on. The ``logging`` module of
the Python standard library already has support for this, via the ``extra``
parameter. gocept.logging provides a ``Formatter`` that extracts these
``extra`` values, formats them as ``key=value`` pairs and appends them to the
message::

    >>> import gocept.logging
    >>> import logging
    >>> import sys

    >>> handler = logging.StreamHandler(sys.stdout)
    >>> handler.setFormatter(gocept.logging.SyslogKeyValueFormatter())
    >>> log = logging.getLogger('example')
    >>> log.addHandler(handler)
    >>> log.warning('Hello, world!', extra={'foo': 'bar'})
    Aug 24 12:10:08 localhost example: Hello, world! foo=bar

This package is tested to be compatible with Python version 2.7 and 3.3.


Advanced usage
==============

If you have ``extra`` values that you always want to pass to your log messages
(e.g things like the current user, session id, ...) you can wrap your logger
with an `LoggerAdapter`_ that prefills these values. gocept.logging provides
one that allows both stacking adapters and overriding the prefilled values::

    >>> from gocept.logging.adapter import StaticDefaults
    >>> import logging

    >>> log = logging.getLogger('advanced')
    >>> log = StaticDefaults(log, {'foo': 'bar', 'qux': 'baz'})
    >>> log = StaticDefaults(log, {'blam': 'splat'})
    >>> log.warning('Hello, world!', extra={'foo': 'override'})
        # yields {'foo': 'override', 'qux': 'baz', 'blam': 'splat'}

.. _`LoggerAdapter`: http://docs.python.org/2/library/logging.html#loggeradapter-objects


Testing support
---------------

To help inspecting the ``extra`` values, gocept.logging comes with a
specialized handler for testing::

    >>> import gocept.logging
    >>> import logging

    >>> log = logging.getLogger('testing')
    >>> handler = gocept.logging.TestingHandler()
    >>> log.addHandler(handler)
    >>> log.warning('Hello, world!', extra={'foo': 'bar'})
    >>> handler.messages[0].extra['foo']
    'bar'

The TestingHandler records each log message as a namedtuple of type
``gocept.logging.testing.LogMessage`` so you an easily access all parts of the
message.


Example configuration
=====================

Creating semi-structured log messages is the first half of the issue, while
analysing them is the second half. We use `logstash`_ for that purpose.

The recommended setup is::

    application -> syslogd on localhost -> logstash on central host (via UDP syslog input)

For development you might want to leave out the middle man and configure the
application to send log messags via syslog protocol directly to logstash.


.. _`logstash`: http://logstash.net/


Setup with ini file
-------------------

If you have a paste.ini for your application, you might use something like
this::

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
------------------

If you have a Zope application, you might use something like this::

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


syslogd configuration
---------------------

rsyslog::

    $EscapeControlCharactersOnReceive off
    $MaxMessageSize 64k
    user.* @localhost:5140

The first two lines are to support tracebacks, which are multiline and might
take up some space. The last line tells rsyslogd to forward all messages of the
``user`` facility (which is what stdlib ``logging`` uses by default) via syslog
UDP protocol to localhost port 5140 (where logstash might be listening).


logstash configuration
----------------------

::

    input {
            tcp {
                    host => "localhost"
                    port => 5140
                    type => syslog
            }
            udp {
                    host => "localhost"
                    port => 5140
                    type => syslog
            }
    }

    filter {
            grok {
                    type => "syslog"
                    pattern => [ "(?m)<%{POSINT:syslog_pri}>%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" ]
            }
            syslog_pri {
                    type => "syslog"
            }
            date {
                    type => "syslog"
                    match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
            }
            mutate {
                    type => "syslog"
                    exclude_tags => "_grokparsefailure"
                    replace => [ "@source_host", "%{syslog_hostname}" ]
                    replace => [ "@message", "%{syslog_program}: %{syslog_message}" ]
            }
            mutate {
                    type => "syslog"
                    remove => [ "syslog_hostname", "syslog_timestamp" ]
            }
            kv {
                    exclude_tags => "_grokparsefailure"
                    type => "syslog"
            }
    }

    output {
            elasticsearch { embedded => true }
    }


Additional features
===================

ArgumentParser
--------------

The provided ``gocept.logging.ArgumentParser`` provides you with the ability to
set a ``logging`` level in you runscripts.::

    from gocept.logging import ArgumentParser
    parser = ArgumentParser()
    # add your arguments with parser.add_argument() here
    options = parser.parse_args()

Use ``your_run_script --help`` to see a help message about the arguments you
can pass to set logging level.


Known bugs
==========

If you log messages as unicode, e.g. ``log.info(u'foo')``, the SyslogHandler
will (incorrectly) prepend a byte-order mark, which confuses the logstash
parser, resulting in "_grokparsefailure". This is a `known bug`_ in the Python
standard library that has been fixed in Python-2.7.4.

.. _`known bug`: http://bugs.python.org/issue14452
