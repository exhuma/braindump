import sys
import timeit
from testdata import testdata, genv6
from merger import merge
from ipaddress import collapse_addresses


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


def run_tests_v6():
    out = genv6(sys.argv[1])
    #iterations = 1
    #print('collapsing {} IPv6 networks {} times'.format(sys.argv[1],
    #                                                    iterations))
    ##print('new: ', timeit.timeit('merge(genv6({}))'.format(sys.argv[1]),
    ##                             setup=('from merger import merge; '
    ##                                    'from testdata import genv6'),
    ##                             number=iterations) / iterations)
    #print('old: ', timeit.timeit(
    #    'collapse_addresses(genv6({}))'.format(sys.argv[1]),
    #    setup=('from ipaddress import collapse_addresses; '
    #           'from testdata import genv6'),
    #    number=iterations) / iterations)

run_tests_v6()
