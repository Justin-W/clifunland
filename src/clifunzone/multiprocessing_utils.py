import logging
import random
from multiprocessing import Process
from time import sleep as time_sleep

log = logging.getLogger(__name__)


def sleep(millis):
    # current_process().join(0.001 * millis)
    time_sleep(0.001 * millis)


def run_processes(processes):
    log.info('Processes: Initializing: count=%s' % len(processes))
    # start all processes
    for p in processes:
        log.info('Processes: Starting: %s' % p.name)
        p.start()

    # wait for all processes to finish
    for p in processes:
        log.info('Processes: Waiting for: %s' % p.name)
        # Note: there is no need to join() to non-daemon processes,
        # unless you actually want to run more code from this process afterwards
        p.join()

    log.info('Processes: Done.')


def _simple__process_func(name, max_delay, exception_probability):
    log.debug('Process event: status={}; process={}'.format('start', name))

    max_delay = float(max_delay)
    exception_probability = float(exception_probability)

    try:
        log.debug('Process event: status={}; process={}'.format('try', name))
        # actual_delay = random.randrange(0, max_delay)
        actual_delay = max_delay * random.random()
        raise_exception = bool(random.random() <= exception_probability)
        sleep(1000 * actual_delay)
        if raise_exception:
            raise RuntimeError('This simulates a semi-Random exception occurring.')
    except Exception as ex:
        log.info('Process event: status={}; process={}'.format('try-except', name), exc_info=ex)
        raise
    else:
        log.info('Process event: status={}; process={}'.format('try-else', name))
    finally:
        log.debug('Process event: status={}; process={}'.format('try-finally', name))

    log.debug('Process event: status={}; process={}'.format('end', name))


def main():
    import json
    from clifunzone import configparser_utils

    cp = configparser_utils.get_configparser(extended_interpolation=False)
    cp.read(configparser_utils.get_default_ini(__file__))
    config = configparser_utils.load_sections(cp, ordered=True)
    log.debug('ini: {}'.format(json.dumps(config, indent=2)))

    # concurrently process each input file using a separate Process
    main_options = config['main']
    count = int(main_options['count'])
    delay = float(main_options['delay'])
    exception_probability = float(main_options['exception_probability'])

    processes = []
    for i in range(0, count):
        process_name = 'Process #{}'.format(i)
        p = Process(name=process_name, target=_simple__process_func,
                    args=(process_name, delay, exception_probability))
        processes.append(p)

    run_processes(processes)


if __name__ == "__main__":
    import sys

    logging.root.setLevel(logging.INFO)
    logging.basicConfig()
    sys.exit(main())
