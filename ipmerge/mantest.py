import sys
from ipaddress import ip_network
import timeit
from ipaddress import collapse_addresses
from merger import merge

import cProfile


def run_tests_v4():
    iterations = 200
    print('collapsing {} IPv4 networks {} times'.format(
        len(testdata), iterations))
    print('new: ', timeit.timeit('merge(testdata)',
                                 setup=('from merger import merge; '
                                        'from testdata import testdata'),
                                 number=iterations) / iterations)
    print('old: ', timeit.timeit(
        'collapse_addresses(testdata)',
        setup=('from ipaddress import collapse_addresses; '
               'from testdata import testdata'),
        number=iterations) / iterations)


def gendata():
    print('generating test-data with {} networks'.format(sys.argv[2]))
    from genpool import gen
    testdata = gen(int(sys.argv[2]))
    with open("testdata.txt", "w") as fp:
        fp.writelines(['{}\n'.format(_) for _ in testdata])


def run_new():
    testdata = [ip_network(_) for _ in open('testdata.txt').readlines()]
    result = merge(testdata)


def run_old():
    testdata = [ip_network(_) for _ in open('testdata.txt').readlines()]
    prof = cProfile.Profile()
    prof.enable()
    result = collapse_addresses(testdata)
    prof.disable()
    prof.dump_stats('old-algo.stats')
    resultlist = [str(_) for _ in result]
    with open("old_result.txt", "w") as fp:
        fp.write('\n'.join(resultlist))


if __name__ == '__main__':
    if sys.argv[1] == 'new':
        run_new()
    elif sys.argv[1] == 'old':
        run_old()
    elif sys.argv[1] == 'gendata':
        gendata()
