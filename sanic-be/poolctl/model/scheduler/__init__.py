"""
Couple common things for the package

"""


def both_or_none(start_job, end_job):
    return bool(start_job) == bool(end_job)


def raw_record(job):
    return job.args[0].raw_data
