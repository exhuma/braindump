import sys
import timeit
from ipaddress import collapse_addresses
from merger import merge
from testdata import testdata


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
    from genpool import gen
    from datetime import datetime
    testdata = gen(int(sys.argv[1]))
    with open("testdata.txt", "w") as fp:
        fp.writelines([str(_) for _ in testdata])
    print('collapsing {} IPv6 networks'.format(sys.argv[1]))

    before = datetime.now()
    result = merge(testdata)
    done = datetime.now()
    with open("new_result.txt", "w") as fp:
        fp.writelines([str(_) for _ in result])
    print('new collapsed to {} networks in {}'.format(
        len(result), done - before))

    before = datetime.now()
    result = collapse_addresses(testdata)
    done = datetime.now()
    resultlist = [str(_) for _ in result]
    with open("old_result.txt", "w") as fp:
        fp.writelines(resultlist)
    print('old collapsed to {} networks in {}'.format(
        len(resultlist), done - before))

run_tests_v6()
