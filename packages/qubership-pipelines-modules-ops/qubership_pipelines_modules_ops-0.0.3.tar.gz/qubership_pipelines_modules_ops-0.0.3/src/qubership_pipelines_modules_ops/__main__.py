from __future__ import annotations # if sys.version_info < (3, 9)

import click    # pip install click
import os
import sys
import time
from functools import wraps

import logging
# in main, configure logging before other imports that may write logs
logging.basicConfig(stream=sys.stdout,
                    format='[%(asctime)s] [%(levelname)-5s] [%(filename)s:%(lineno)-3s] %(message)s',
                    level=os.getenv('QUBERSHIP_PIPELINES_MODULES_OPS_LOG_LEVEL', logging.INFO))

from .prepare_data import prepare_data, store_data

logger = logging.getLogger(__name__)

DEFAULT_JOB_STAGE = 'test'
DEFAULT_JOB_NAME = 'test'

def log_method_params(func):
    @wraps(func)
    def inner(*args, **kwargs):
        t0 = time.time()
        logger.info(f"{func.__name__} started with params {kwargs}")
        func(*args, **kwargs)
        logger.info(f"{func.__name__} finished in {time.time()-t0:.3f} s")
    return inner

@click.group
def cli():
    pass

@cli.command('prepare-data')
@click.option('--root')
@click.option('--stage')
@log_method_params
def _prepare_data(root: str, stage: str):
    prepare_data(root, stage)

@cli.command('store-data')
@click.option('--root')
@click.option('--stage')
@click.option('--job')
@log_method_params
def _store_data(root: str, stage: str, job: str):
    store_data(root, stage, job)
