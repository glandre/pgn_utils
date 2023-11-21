def parse_int(s) -> int | None:
  try:
    return int(s)
  except ValueError:
    return None
