from __future__ import absolute_import
from celery import Celery

app = Celery('kkfw',
             broker='amqp://',
             backend='rpc://',
             include=['kkfw.tasks', 'kkfw.tweets'])
