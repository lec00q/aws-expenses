import math
import click


INF = float('inf')


class Float(float):

    def __div__(self, other):
        if other:
            return float.__div__(self, other)
        elif self == 0.0 or math.isnan(self):
            return float('nan')
        return float('inf') if self > 0.0 else float('-inf')


class InputError(Exception):
    pass


class MMcQueue(object):
    """
    In the mathematical theory of random processes, the M/M/c queue is
    a multi-server queue model. It is a generalization of the M/M/1 queue.

        Arrivals are a Poisson process
        Service time is exponentially distributed
        There are c servers
        The length of queue in which arriving users wait before being served is
            infinite
        The population of users (i.e. the pool of users), or requests, available
            to join the system is infinite

    This type of system arises in many situations, including lines at a bank,
        phone queuing systems, the application of computer resources, etc...

    http://en.wikipedia.org/wiki/M/M/c_queue
    """

    def __init__(self, arrival_rate, service_time, num_servers=1):
        """
        @param arrival_rate: 0 and over
        @param service_time: 0 and over
        @param num_servers: int between 1 and 150, inclusive
        """
        self.c = num_servers  # Number of servers.
        if not (isinstance(num_servers, int) and 1 <= num_servers <= 150):
            raise InputError('num_servers must be int between 1 and 150, inclusive.')
        if arrival_rate < 0 or service_time < 0:
            raise InputError('arrival_time and service_time must be 0 and over.')

        self.arrival_rate = Float(arrival_rate)
        service_time = Float(service_time)
        self.service_rate = Float(1.0) / service_time
        self.util = self.arrival_rate / self.service_rate / self.c

        if self.util == 0.0:
            self.tw = self.lq = self.lw = 0.0
            self.tq = service_time
            return
        if self.util >= 1.0:
            self.tw = self.tq = self.lq = self.lw = INF
            return

        try:
            crc = pow(self.c * self.util, self.c)
        except OverflowError:
            self.tw = self.tq = self.lq = self.lw = INF
            return

        factc = math.factorial(self.c)
        x = 0.0
        for i in range(self.c):
            x += pow(self.c * self.util, i) / math.factorial(i)
        x += crc / (factc * (1.0 - self.util))
        x = crc / x / (factc * (1.0 - self.util))

        # Expected number of customers waiting in queue not in service
        self.lw = x * self.util / (1.0 - self.util)
        # Average waiting time in queue
        self.tw = Float(self.lw) / self.arrival_rate
        # Average time in system (queued + serviced)
        self.tq = self.tw + service_time
        # Expected number of customers in system
        self.lq = self.arrival_rate * self.tq
        return

    def __str__(self):
        return ('arr=%.3f, dep=%.3f, c=%d, util=%.3f, ' +
                'TmQue=%.3f, TmSys=%.3f, NmQue=%.3f, NmSys=%.3f') \
            % (self.arrival_rate, self.service_rate, self.c, self.util,
               self.tw, self.tq, self.lw, self.lq)


@click.command()
@click.option('--arrival-rate', '-l', 'arrival_rate', default=10.0,
              help='Average number of jobs per hour (default 10).')
@click.option('--service-time', '-s', 'service_time', default=7.0,
              help='Number of minutes for serving a single job (default 7).')
@click.option('--max-wait-time', '-t', 'maximum_wait_time', default=10.0,
              help='Maximum expected time in the system in minutes (default 10).')
@click.option('--fixed-cost', '-f', 'fixed_cost', default=70,
              help='Approximate monthly fixed cost for the architecture in dollars (default 70).')
@click.option('--var-cost', '-v', 'server_cost', default=41,
              help='Variable monthly cost for each back-end server in dollars (default 41).')
def get_number_of_servers(arrival_rate, service_time, maximum_wait_time, fixed_cost, server_cost):
    if (maximum_wait_time < service_time):
        print ("The expected waiting time cannot be less that the service time!")
        return False

    for n in range(1, 151):
        mmc = MMcQueue(Float(arrival_rate) / 60, service_time, n)
        if (mmc.tq < maximum_wait_time):
            break

    if n < 150:
        print ("Number of servers: %d" % mmc.c)
        print ("Average serving time: %.3f minutes" % mmc.tq)
        total_cost = fixed_cost + n * server_cost
        print ("Total cost: %d$ per month" % total_cost)
        return True
    else:
        print ("Reached max number of servers (%d)." % n)
        print ("Please reduce the arrival rate or the service time.")
        return False


if __name__ == '__main__':
    get_number_of_servers()
