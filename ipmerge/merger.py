def merge(networks):

    output = []

    for net in networks:

        # Initialise the output
        if not output:
            output.append(net)
            continue

        # Keep a ref to output[-1] (just to keep the code more readable)
        head = output[-1]

        # If the current net is completely contained inside the last item on
        # the stack we can simply ignore it.
        if (head.network_address <= net.network_address and
                head.broadcast_address >= net.broadcast_address):
            continue

        # If the current net does not have the same prefix length, we cannot
        # merge them. Shift it onto the stack.
        elif net.prefixlen != head.prefixlen:
            output.append(net)

        # If the network which immediately follows last item on the stack is
        # the same as the current net, we can merge (i.e. add the head's
        # supernet)
        elif list(head.supernet().subnets())[1] == net:
            output[-1] = head.supernet()

            # Now, the last item on the stack changed, and possibly this can
            # have an effect on previous items on the stack. Reduce the stack
            # as much as possible.
            while (len(output) >= 2 and
                   list(output[-2].supernet().subnets())[1] == output[-1]):
                output.pop()
                output[-1] = output[-1].supernet()

        # Nothing can be done. Shift the current net on the stack.
        else:
            output.append(net)

    return output



from ipaddress import _BaseNetwork, _BaseAddress

def collapse_addresses(addresses):
    """Collapse a list of IP objects.

    Example:
        collapse_addresses([IPv4Network('192.0.2.0/25'),
                            IPv4Network('192.0.2.128/25')]) ->
                           [IPv4Network('192.0.2.0/24')]

    Args:
        addresses: An iterator of IPv4Network or IPv6Network objects.

    Returns:
        An iterator of the collapsed IPv(4|6)Network objects.

    Raises:
        TypeError: If passed a list of mixed version objects.

    """
    i = 0
    addrs = []
    ips = []
    nets = []

    # split IP addresses and networks
    for ip in addresses:
        if isinstance(ip, _BaseAddress):
            if ips and ips[-1]._version != ip._version:
                raise TypeError("%s and %s are not of the same version" % (
                                 ip, ips[-1]))
            ips.append(ip)
        elif ip._prefixlen == ip._max_prefixlen:
            if ips and ips[-1]._version != ip._version:
                raise TypeError("%s and %s are not of the same version" % (
                                 ip, ips[-1]))
            try:
                ips.append(ip.ip)
            except AttributeError:
                ips.append(ip.network_address)
        else:
            if nets and nets[-1]._version != ip._version:
                raise TypeError("%s and %s are not of the same version" % (
                                 ip, nets[-1]))
            nets.append(ip)

    # sort and dedup
    ips = sorted(set(ips))
    nets = sorted(set(nets))

    while i < len(ips):
        (first, last) = _find_address_range(ips[i:])
        i = ips.index(last) + 1
        addrs.extend(summarize_address_range(first, last))

    return iter(merge(sorted(
        addrs + nets, key=_BaseNetwork._get_networks_key)))

