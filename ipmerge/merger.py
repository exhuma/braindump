def merge(networks):

    output = []

    for net in networks:

        # Initialise the output
        if not output:
            output.append(net)
            continue

        # Keep a ref to output[-1]
        bucket = output.pop()

        # If the current net is completely contained inside the last item on
        # the stack we can simply ignore it.
        if (bucket.network_address <= net.network_address and
                bucket.broadcast_address >= net.broadcast_address):
            output.append(bucket)

        # If the current net does not have the same prefix length, we cannot
        # merge them. Put both back on the stack.
        elif net.prefixlen != bucket.prefixlen:
            output.append(bucket)
            output.append(net)

        # If the network which immediately follows last item on the stack is
        # the same as the current net, we can merge (i.e. add the buckets
        # supernet)
        elif list(bucket.supernet().subnets())[1] == net:
            output.append(bucket.supernet())

            # Now, the last item on the stack changed, and possibly this can
            # have an effect on previous items on the stack. Reduce the stack
            # as much as possible.
            while (len(output) >= 2 and
                   list(output[-2].supernet().subnets())[1] == output[-1]):
                output.pop()
                output[-1] = output[-1].supernet()

        # Nothing can be done. Shift the current net on the stack.
        else:
            output.append(bucket)
            output.append(net)

    return output
