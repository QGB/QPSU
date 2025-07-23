#!/usr/bin/python
#
# Created by Peter Krumins (peter@catonmat.net, @pkrumins on twitter)
# www.catonmat.net -- good coders code, great coders reuse
#
# Asynchronous DNS Resolution in Python.
#
# Read more about how this code works in my post:
# www.catonmat.net/blog/asynchronous-dns-resolution
#

import adns
from time import time

class AsyncResolver(object):
    def __init__(self, hosts, intensity=100):
        """
        hosts: a list of hosts to resolve
        intensity: how many hosts to resolve at once
        """
        self.hosts = hosts
        self.intensity = intensity
        self.adns = adns.init()

    def resolve(self):
        """ Resolves hosts and returns a dictionary of { 'host': 'ip' }. """
        resolved_hosts = {}
        active_queries = {}
        host_queue = self.hosts[:]

        def collect_results():
            for query in self.adns.completed():
                answer = query.check()
                host = active_queries[query]
                del active_queries[query]
                if answer[0] == 0:
                    ip = answer[3][0]
                    resolved_hosts[host] = ip
                elif answer[0] == 101: # CNAME
                    query = self.adns.submit(answer[1], adns.rr.A)
                    active_queries[query] = host
                else:
                    resolved_hosts[host] = None

        def finished_resolving():
            return len(resolved_hosts) == len(self.hosts)

        while not finished_resolving():
            while host_queue and len(active_queries) < self.intensity:
                host = host_queue.pop()
                query = self.adns.submit(host, adns.rr.A)
                active_queries[query] = host
            collect_results()

        return resolved_hosts


if __name__ == "__main__":
    host_format = "www.host%d.com"
    number_of_hosts = 20000

    hosts = [host_format % i for i in range(number_of_hosts)]

    ar = AsyncResolver(hosts, intensity=500)
    start = time()
    resolved_hosts = ar.resolve()
    end = time()

    print "It took %.2f seconds to resolve %d hosts." % (end-start, number_of_hosts)

