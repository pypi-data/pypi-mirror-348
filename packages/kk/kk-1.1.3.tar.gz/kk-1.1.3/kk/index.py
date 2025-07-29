#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Last modified: 2020-03-27 21:40:13
'''
import os  # NOQA: E402
import sys  # NOQA: E402

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # NOQA: E402

import hashlib
import logging
from datetime import datetime, timedelta
from functools import partial
from pathlib import Path

import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from handler import bp as bp_disk
from monitor import FileMonitor
from tornado.options import define, options
from tornado_utils import Application, bp_user
from utils import AioEmail, AioRedis, Motor, Request, connect

define('root', default='.', type=str)
define('auth', default=False, type=bool)
define('upload', default=True, type=bool)
define('delete', default=True, type=bool)
define('db', default='kk', type=str)
define('name', default='FileServer', type=str)

logging.getLogger('apscheduler').setLevel(logging.ERROR)


class Application(Application):

    def init(self):
        self.root = Path(options.root).expanduser().resolve()
        self.http = Request(lib='aiohttp')
        self.monitor = FileMonitor(self.root)
        self.monitor.start()

        self.opt.update(
            {k.lower(): v for k, v in os.environ.items() if k.lower() in ['site_id']})
        self.sched = BackgroundScheduler()
        self.sched.add_job(partial(self.monitor.scan_dir, self.root, True),
                           'date', run_date=datetime.now() + timedelta(seconds=10))
        self.sched.start()
        if options.auth:
            self.db = Motor(options.db)
            self.email = AioEmail(use_tls=True)
            self.rd = AioRedis()

    async def shutdown(self):
        self.monitor.stop()
        await super().shutdown()

    def get_md5(self, path):
        if path.is_file():
            md5 = hashlib.md5()
            with path.open('rb') as fp:
                while True:
                    data = fp.read(4194304)
                    if not data:
                        break
                    md5.update(data)
            return md5.hexdigest()

    def get_port(self):
        port = 8000
        try:
            connections = psutil.net_connections()
            ports = set([x.laddr.port for x in connections])
            while port in ports:
                port += 1
        except:
            while connect('127.0.0.1', port):
                port += 1
        return port


def main():
    kwargs = dict(
        static_path=Path(__file__).parent.absolute() / 'static',
        template_path=Path(__file__).parent.absolute() / 'templates',
    )
    app = Application(**kwargs)
    app.register(bp_disk, bp_user)
    port = options.port if options.auth else app.get_port()
    max_body_size = 10240 * 1024 * 1024
    app.run(port=port, max_body_size=max_body_size)


if __name__ == '__main__':
    main()
