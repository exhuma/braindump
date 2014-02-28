from ipaddress import ip_network
from random import randint


def generate(base, **kwargs):
    for sub in base.subnets(**kwargs):
        if randint(0, 100) > 50:
            continue

        if sub.prefixlen < 80 and randint(0, 100) < 30:
            j = 0
            for x in generate(sub, prefixlen_diff=randint(2, 48)):
                yield x
                j += 1
                if j >= randint(0, 20):
                    break

        yield(sub)


def gen(num):
    base = ip_network('1234:1234::/30')
    gen = generate(base, new_prefix=48)

    i = 0
    out = []
    for val in gen:
        out.append(val)
        i += 1
        if i >= num:
            break
    return out


if __name__ == '__main__':
    import sys
    for value in gen(int(sys.argv[1])):
        print(value)
