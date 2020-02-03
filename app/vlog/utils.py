from dateutil.parser import parse


def parse_vlog_line(data, vri_id):
    datetime, message_type, message = data.split(',')
    datetime = parse(datetime)
    return dict(
        time=datetime,
        vri_id=vri_id,
        message_type=message_type,
        message=message
    )


def parse_vlog_lines(data, vri_id):
    chunks = data.split('\n')
    lines = list(filter(None, [x.strip() for x in chunks]))
    return [parse_vlog_line(line, vri_id) for line in lines]
