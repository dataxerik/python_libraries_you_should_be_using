from collections import OrderedDict, defaultdict, namedtuple
from string import ascii_lowercase
from time import perf_counter
from array import array
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor as Executor
import logging
import sched
import time
from datetime import datetime, timedelta


def showcase_ordered_dict():
    # Useful for when you need to perverse the insert order like mapping
    print("Notice how the order can differ")
    print(dict(zip(ascii_lowercase, range(4))))
    print(dict(zip(ascii_lowercase, range(5))))
    print(dict(zip(ascii_lowercase, range(6))))
    print(dict(zip(ascii_lowercase, range(7))))

    print("But, using order dict, the insert order is preserved")
    print(OrderedDict(zip(ascii_lowercase, range(4))))
    print(OrderedDict(zip(ascii_lowercase, range(5))))
    print(OrderedDict(zip(ascii_lowercase, range(6))))
    print(OrderedDict(zip(ascii_lowercase, range(7))))

    print("CAUTION - OrderedDict doesn't work for keyword arguments")
    print(OrderedDict(a=1, b=2, c=3))


def showcase_default_dict():
    # Useful for when you need to specific the default values of new keys
    d = defaultdict(list)
    print(d['a'])

    # Using defaultdict avoids uncessary code like below
    # d = {}; for k in keydata: if not k in d: d[k] = []; d[k].append(...)


def showcase_named_tuples():
    tup = (1, True, "red")

    def f_bad():
        return 2, False, "blue"

    def f_good():
        name_tup = namedtuple('A', 'count enabled color')
        return name_tup(2, False, "blue")

    name_tup = namedtuple('A', 'count enabled color')
    tup = name_tup(count=1, enabled=True, color='red')
    print(tup)
    print(tup.color)

    # BAD - if we increase the number of return values this breaks
    count, enabled, color = f_bad()

    # BAD - if we change the order for the tuple then this won't work as expcted
    tup = f_bad()
    enabled = tup[1]

    # Goood
    tup = f_good()
    print(tup.color)


def showcase_context_lib():
    @contextmanager
    def timing(label: str):
        t0 = perf_counter()
        yield lambda: (label, t1 - t0)
        t1 = perf_counter()

    with timing('Array tests') as total:
        with timing('Array creation outermul') as outer:
            x = array('d', [0]) * 1000000

        with timing('Array creation innermul') as inner:
            x = array('d', [0] * 1000000)

    print('Total [%s]: %.6f s' % total())
    print(total)
    print('      Timing [%s]: %.6f s' % inner())
    print('      Timing [%s]: %.6f s' % outer())


def showcase_concurrent_future():
    urls = """google twitter facebook youtube pinterest tumblr
    instagram reddit flickr meetup classmates microsoft apple
    linkedin xing renren disqus snapchat twoo whatsapp""".split()

    def fetch(url):
        from urllib import request, error
        try:
            data = request.urlopen(url).read()
            return '{}: length {}'.format(url, len(data))
        except error.HTTPError as e:
            return '{} : {}'.format(url, e)

    with Executor(max_workers=4) as exe:
        template = 'http://www.{}.com'
        jobs = [exe.submit(
            fetch, template.format(u)) for u in urls]
        results = [job.result() for job in jobs]

    print('\n'.join(results))


def showcase_logging():
    logger = logging.getLogger()

    def blah():
        return 'blah'

    try:
        1 / 0
    except:
        logging.exception("something failed.")


def showcase_sched():
    scheduler = sched.scheduler(timefunc=time.time)

    def saytime():
        print(time.ctime())
        scheduler.enter(10, priority=0, action=saytime)

    saytime()
    try:
        scheduler.run(blocking=True)
    except KeyboardInterrupt:
        print("Stoppped.")

def showcase_sched1():
    scheduler = sched.scheduler(timefunc=time.time)

    def reschedule():
        new_target = datetime.now().replace(
            second=0, microsecond=0)
        new_target += timedelta(minutes=1)
        scheduler.enterabs(
            new_target.timestamp(), priority=0, action=saytime
        )
    def saytime():
        print(time.ctime(), flush=True)
        reschedule()

    reschedule()
    try:
        scheduler.run(blocking=True)
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == '__main__':
    # showcase_ordered_dict()
    # showcase_default_dict()
    # showcase_named_tuples()
    # showcase_context_lib()
    # showcase_concurrent_future()
    # showcase_logging()
    showcase_sched1()
