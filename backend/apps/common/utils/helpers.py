from datetime import datetime

def timestamp_to_datetime(ts):
    """Convertit un timestamp (millisecondes) en datetime"""
    return datetime.fromtimestamp(ts / 1000)

def datetime_to_timestamp(dt):
    """Convertit un datetime en timestamp (millisecondes)"""
    return int(dt.timestamp() * 1000)