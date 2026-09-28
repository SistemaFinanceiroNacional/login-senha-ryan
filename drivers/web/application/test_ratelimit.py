from drivers.web.application.ratelimit import RateLimiter


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_events_beyond_the_limit_are_refused():
    limiter = RateLimiter(3, 60, Clock())

    assert [limiter.allow("1.2.3.4") for _ in range(4)] == \
        [True, True, True, False]


def test_keys_are_limited_independently():
    limiter = RateLimiter(1, 60, Clock())

    assert limiter.allow("1.2.3.4")
    assert limiter.allow("5.6.7.8")
    assert not limiter.allow("1.2.3.4")


def test_the_window_slides():
    clock = Clock()
    limiter = RateLimiter(2, 60, clock)
    limiter.allow("ip")
    clock.now = 30
    limiter.allow("ip")

    clock.now = 59
    assert not limiter.allow("ip")
    clock.now = 60.5
    assert limiter.allow("ip")
