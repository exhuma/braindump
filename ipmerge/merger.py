def merge(networks):

    if isinstance(networks, list):
        networks = iter(networks)

    output = [next(networks)]

    for net in networks:

        bucket = output.pop()
        if (bucket.network_address <= net.network_address and
                bucket.broadcast_address >= net.broadcast_address):
            output.append(bucket)

        elif net.prefixlen != bucket.prefixlen:
            output.append(bucket)
            output.append(net)

        elif list(bucket.supernet().subnets())[1] == net:
            output.append(bucket.supernet())

            while (len(output) >= 2 and
                   list(output[-2].supernet().subnets())[1] == output[-1]):
                output.pop()
                output[-1] = output[-1].supernet()
        else:
            output.append(bucket)
            output.append(net)

    return output
