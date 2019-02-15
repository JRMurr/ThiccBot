def get_error_str(r, prefix=""):
    return f"{prefix}, HTTPCODE: {r.status}, ERROR MESSAGE: {r.reason}"
