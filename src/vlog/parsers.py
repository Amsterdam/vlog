import logging

import pytz
from dateutil.parser import parse

logger = logging.getLogger(__name__)


def parse_vlog_line(data: str):
    """
    Parse a single line of V-Log data
    Expected format is:
       date, vri_id, message_type, message

    Example:
        2020-01-23 00:00:02.220,102,10,0A0171010063
    """
    date, vri_id, message_type, message = data.split(',')
    date = parse(date.strip())
    if not date.tzinfo:
        date.replace(tzinfo=pytz.timezone('CET'))
    date = date.astimezone(pytz.utc)
    return dict(
        time=date,
        vri_id=int(vri_id),
        message_type=int(message_type),
        message=message.strip()
    )


def parse_vlog_lines(data: str, strict=False):
    """
    Parse a multiline string of V-Log lines.
    Logs must be split by newlines

    Note:
    Lines will be stripped of leading and trailing spaces
    and empty lines discarded.
    """
    chunks = data.splitlines()
    lines = list(filter(None, [x.strip() for x in chunks]))
    data = []
    for line in lines:
        try:
            data.append(parse_vlog_line(line))
        except ValueError as e:
            logger.exception(e)
            if strict:
                raise
            continue
    return data
