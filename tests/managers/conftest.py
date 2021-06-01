"""This module provides helper fixtures for quickly generating flows and jobs."""

import pytest


@pytest.fixture(scope="session")
def simple_job():
    from jobflow import job

    global func

    @job
    def func(message):
        return message + "_end"

    return func


@pytest.fixture(scope="session")
def simple_flow(simple_job):
    from jobflow import Flow

    def _gen():
        simple = simple_job("12345")
        return Flow([simple], simple.output)

    return _gen


@pytest.fixture(scope="session")
def connected_flow(simple_job):
    from jobflow import Flow

    def _gen():
        simple1 = simple_job("12345")
        simple2 = simple_job(simple1.output)
        return Flow([simple1, simple2], simple2.output)

    return _gen


@pytest.fixture(scope="session")
def nested_flow(connected_flow):
    from jobflow import Flow

    def _gen():
        flow1 = connected_flow()
        flow2 = connected_flow()
        flow2.jobs[0].function_args = (flow1.jobs[1].output,)
        return Flow([flow1, flow2], flow2.output)

    return _gen


@pytest.fixture(scope="session")
def addition_job(simple_job):
    from jobflow import Response, job

    global addition_func

    @job
    def addition_func(a, b):
        return Response(output=a + b, addition=simple_job(str(a + b)))

    return addition_func


@pytest.fixture(scope="session")
def addition_flow(addition_job):
    from jobflow import Flow

    def _gen():
        add = addition_job(5, 6)
        return Flow([add], add.output)

    return _gen


@pytest.fixture(scope="session")
def detour_job(simple_job):
    from jobflow import Response, job

    global detour_func

    @job
    def detour_func(a, b):
        return Response(output=a + b, detour=simple_job(str(a + b)))

    return detour_func


@pytest.fixture(scope="session")
def detour_flow(detour_job, simple_job):
    from jobflow import Flow

    def _gen():
        detour = detour_job(5, 6)
        simple = simple_job("12345")
        return Flow([detour, simple], simple.output)

    return _gen


@pytest.fixture(scope="session")
def replace_job(simple_job):
    from jobflow import Response, job

    global replace_func

    @job
    def replace_func(a, b):
        return Response(output=a + b, replace=simple_job(str(a + b)))

    return replace_func


@pytest.fixture(scope="session")
def replace_flow(replace_job, simple_job):
    from jobflow import Flow

    def _gen():
        replace = replace_job(5, 6)
        simple = simple_job("12345")
        return Flow([replace, simple], simple.output)

    return _gen


@pytest.fixture(scope="session")
def stop_jobflow_job():
    from jobflow import Response, job

    global stop_jobflow_func

    @job
    def stop_jobflow_func():
        return Response(output="1234", stop_jobflow=True)

    return stop_jobflow_func


@pytest.fixture(scope="session")
def stop_jobflow_flow(stop_jobflow_job, simple_job):
    from jobflow import Flow

    def _gen():
        stop = stop_jobflow_job()
        simple = simple_job("12345")
        return Flow([stop, simple], simple.output)

    return _gen


@pytest.fixture(scope="session")
def stop_children_job():
    from jobflow import Response, job

    global stop_children_func

    @job
    def stop_children_func():
        return Response(output="1234", stop_children=True)

    return stop_children_func


@pytest.fixture(scope="session")
def stop_children_flow(stop_children_job, simple_job):
    from jobflow import Flow

    def _gen():
        stop = stop_children_job()
        simple1 = simple_job(stop.output)
        simple2 = simple_job("12345")
        return Flow([stop, simple1, simple2], simple2.output)

    return _gen
