# aws-expenses

A simple but useful tool for calculating the cost of an AWS infrastructure as a function of real usage needs.

## Problem statement

Let's consider a typical AWS infrastructure composed of a "fixed" part, a set of EC2 machines that are always on (such as RDS or Cloudfront), and a "variable" part, a set of EC2 units that act as backend servers. The backend is defined as a server that executes a single job, or task, that lasts a finite amount of time.

If you know:

- the average number of hourly requests to the backend
- the average number of minutes for serving a single job
- the maximum expected time (in minutes) that a client can wait in the system
- the monthly cost for a single backend server (in dollars)
- the cost for the fixed part of the AWS infrastructure

this tool can compute the minimum number of EC2 machines that satisfy the requests and consequently the monthly cost of the AWS infrastructure.

### Mathematical Theory

The system can be modeled as a M/M/c queue, where arrivals are a Poisson process and the service time is exponentially distributed. For more information see [Wikipedia](http://en.wikipedia.org/wiki/M/M/c_queue).

## Usage

First install the requirements:

```
$ pip install -f requirements.txt
```

The command help is self-explanatory:

```
$ python aws_compute.py --help
Usage: aws_compute.py [OPTIONS]

Options:
  -l, --arrival-rate FLOAT   Average number of jobs per hour (default 10).
  -s, --service-time FLOAT   Number of minutes for serving a single job
                             (default 7).
  -t, --max-wait-time FLOAT  Maximum expected time in the system in minutes
                             (default 10).
  -f, --fixed-cost INTEGER   Approximate monthly fixed cost for the
                             architecture in dollars (default 70).
  -v, --var-cost INTEGER     Variable monthly cost for each back-end server in
                             dollars (default 41).
  --help                     Show this message and exit.

```


