from datetime import datetime


def parse_timestamp(ts: str) -> datetime:
    """
    Parse benchmark timestamp string
    into timezone-aware datetime.
    """

    return datetime.fromisoformat(
        ts.replace("Z", "+00:00")
    )


def time_difference_seconds(
    ts1: str,
    ts2: str
) -> float:
    """
    Return absolute difference
    between timestamps in seconds.
    """

    dt1 = parse_timestamp(ts1)
    dt2 = parse_timestamp(ts2)

    return abs(
        (dt2 - dt1).total_seconds()
    )


def within_time_window(
    ts1: str,
    ts2: str,
    seconds: int
) -> bool:
    """
    Check if timestamps fall
    within specified window.
    """

    return (
        time_difference_seconds(
            ts1,
            ts2
        ) <= seconds
    )