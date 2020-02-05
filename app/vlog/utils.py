import logging

import pytz
from dateutil.parser import parse

logger = logging.getLogger(__name__)


def parse_vlog_line(data: str, vri_id: int = 101):
    """
    Parse a single line of V-Log data
    Expected format is:
       date, message_type, message

    Example:
        2020-01-23 00:00:02.220,10,0A0171010063
    """
    date, message_type, message = data.split(',')
    date = parse(date)
    if not date.tzinfo:
        date.replace(tzinfo=pytz.timezone('CET'))
    date = date.astimezone(pytz.utc)
    return dict(
        time=date,
        vri_id=vri_id,
        message_type=int(message_type),
        message=message
    )


def parse_vlog_lines(data: str, vri_id: int = 101, strict=False):
    """
    Parse a multiline string of V-Log lines.
    Logs must be split by newlines

    Note:
    Lines will be stripped of leading and trailing spaces
    and empty lines discarded.
    """
    chunks = data.split('\n')
    lines = list(filter(None, [x.strip() for x in chunks]))
    data = []
    for line in lines:
        try:
            data.append(parse_vlog_line(line, vri_id))
        except ValueError as e:
            logger.exception(e)
            if strict:
                raise
            continue
    return data
