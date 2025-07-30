import argparse
import logging
import os
import time
from datetime import datetime, timezone

from openfilter.filter_runtime.filter import LOG_UTC
from openfilter.filter_runtime.rolllog import RollLog
from openfilter.filter_runtime.logging import LOG_PATH, Logger
from openfilter.filter_runtime.utils import sanitize_filename, parse_date_and_or_time

from .common import SCRIPT

logger = logging.getLogger(__name__)

logger.setLevel(int(getattr(logging, (os.getenv('LOG_LEVEL') or 'INFO').upper())))


# --- logs OR metrics --------------------------------------------------------------------------------------------------

def _cmd_logs_or_metrics(args, category, default_path, setup_func, entry_func):

    # parse options from command line

    parser = argparse.ArgumentParser(prog=f'{SCRIPT} {category}', formatter_class=argparse.RawTextHelpFormatter,
        description=f'Show Filter {category}.',
        epilog=f"""
notes:
  * Dates are in year/month/day order, separator is '/' or '-', accepted formats are 'yyyy/mm/dd', 'yy/mm/dd', 'mm/dd' or 'dd'.
  * Accepted times are 24 hour clock 'hh:mm:ss.ms', 'hh:mm:ss', 'hh:mm', 'mm:ss.ms' or 'ss.ms'.
  * Date with time is accepted separated by a space or a 'T', e.g. 'yy-mm-dd hh:mm:ss' or 'mm/ddTss.ms'.
  * Datetime can also be ISO format.
        """.strip(),
    )

    parser.add_argument('-f', '--from',
        type = str,
        help = f"date/time to show {category} from, 'start' from very beginning (default: show last file)",
    )
    parser.add_argument('-t', '--to',
        type = str,
        help = f'date/time to show {category} to (default: show last file)',
    )
    parser.add_argument('-p', '--path',
        type    = str,
        default = default_path,
        help    = f'path to {category} (default: %(default)s)',
    )
    parser.add_argument('--utc',
        action  = 'store_true',
        default = None,
        help    = 'all dates/times in UTC regardless of environment setting',
    )
    parser.add_argument('--no-utc',
        action = 'store_false',
        dest   = 'utc',
        help   = 'all dates/times in local time regardless of environment setting',
    )
    parser.add_argument('FILTER',
        nargs='*',
        help='Filters to show, all if nothing specified',
    )

    opts = parser.parse_args(args)

    logger.debug(f'opts: {opts}')

    # do the thing

    setup_func(opts.utc)

    path    = opts.path
    ts_from = None if (f := getattr(opts, 'from')) is None else \
        (dt_from := parse_date_and_or_time(f, opts.utc)).timestamp() if f.lower() != 'start' else 0
    ts_to   = None if (t := opts.to) is None else (dt_to := parse_date_and_or_time(t, opts.utc)).timestamp()
    FILTERS = [sanitize_filename(f) for f in opts.FILTER]
    filters = set()

    if ts_from:  # also checks for 0
        logger.debug(f'from: {dt_from}')

    if ts_to is not None:
        logger.debug(f'to: {dt_to}')

    if not os.path.isdir(path):
        print(f'Path does not exist: {path}')

        return

    if ts_from is not None and ts_to is not None and ts_to <= ts_from:
        raise ValueError("'--to' timestamp can not be before or same as '--from' timestamp")

    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            filters.add(name)

    if not FILTERS:
        if not filters:
            print(f'No {category} directories')

    else:
        for filter in FILTERS:
            if filter not in filters:
                print(f'No {category} directory for: {filter}')

        filters &= set(FILTERS)

    if not filters:
        return

    filters     = sorted(filters)
    filter_logs = {}  # {'filter': RollLog, ...}

    for filter in filters:
        rl = RollLog(mode='json', rdonly=True, **Logger.path_prefix_and_suffix(path, filter, category))

        if rl.logfiles:
            filter_logs[filter] = rl
        else:
            print(f'No {category} for: {filter}')

    for filter, rl in filter_logs.items():
        if len(filter_logs) > 1:
            print(f'\n{filter}\n')

        rl.seek_block(rl.logfiles[-1].timestamp if ts_from is None else ts_from)

        if ts_from is not None:
            while entry := rl.read():
                entry['ts'] = dt = datetime.fromisoformat(entry['ts'])

                if dt.timestamp() >= ts_from:
                    if ts_to is None or dt.timestamp() < ts_to:
                        entry_func(entry)

                    break

            else:
                continue

        while entry := rl.read():
            entry['ts'] = dt = datetime.fromisoformat(entry['ts'])

            if ts_to is None or dt.timestamp() < ts_to:
                entry_func(entry)
            else:
                break


# --- logs -------------------------------------------------------------------------------------------------------------

def cmd_logs(args):
    LogRecord = logging.LogRecord
    levels    = {
        'CRITICAL': 50,
        'FATAL':    50,
        'ERROR':    40,
        'WARN':     30,
        'WARNING':  30,
        'INFO':     20,
        'DEBUG':    10,
        'NOTSET':   0,
    }

    format = None

    def setup_func(utc: bool | None):
        nonlocal format

        root_formatter      = logging.getLogger().handlers[0].formatter  # root formatter
        formatter           = logging.Formatter(  # clone it
            fmt     = root_formatter._fmt,
            datefmt = root_formatter.datefmt,
            style   = root_formatter._style._fmt[0],
        )
        formatter.converter = root_formatter.converter if utc is None else time.gmtime if utc else time.localtime
        format              = formatter.format

    def entry_func(entry: dict):  # format it exactly the same way as the logger
        log_record         = LogRecord(None, levels.get(entry['lvl'], 0), None, None, entry['msg'], None, None)
        log_record.process = entry['pid']
        log_record.thread  = log_record.threadName = entry['thid']
        log_record.created = ct = entry['ts'].timestamp()
        log_record.msecs   = int((ct - int(ct)) * 1000) + 0.0  # see gh-89047
        log_record.lineno  = 0

        # log_record.threadName = ''
        # log_record.filename   = ''
        # log_record.funcName   = ''

        print(format(log_record))

    return _cmd_logs_or_metrics(args, 'logs', LOG_PATH, setup_func, entry_func)


# --- metrics ----------------------------------------------------------------------------------------------------------

def cmd_metrics(args):
    tz = datefmt = None

    def setup_func(utc: bool | None):
        nonlocal tz, datefmt

        tz      = timezone.utc if (LOG_UTC if utc is None else utc) else datetime.now().astimezone().tzinfo
        datefmt = logging.getLogger().handlers[0].formatter.datefmt

    def entry_func(entry: dict):
        entry['ts'] = entry['ts'].astimezone(tz).strftime(datefmt)

        print(', '.join(f'{k}: {v}' for k, v in entry.items()))

    return _cmd_logs_or_metrics(args, 'metrics', LOG_PATH, setup_func, entry_func)
