def envelope(fn):
    def wrapper(*args, **kwargs):
        r = fn(*args, **kwargs)
        return {
            'total': len(r),
            'data': r
        }

    return wrapper