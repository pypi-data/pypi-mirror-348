#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:   digua
Created:  2025-05-15 11:53:04
"""

import collections
import time
from pathlib import Path

from utils import Dict, Logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileMonitor(FileSystemEventHandler):

    def __init__(self, root):
        super().__init__()
        self.root = Path(root).expanduser().resolve()
        self.files = collections.defaultdict(list)
        self.logger = Logger('FileMonitor')

    def scan_dir(self, path, recursive=False):
        if not path.is_dir():
            return []

        path = path.expanduser().resolve()
        if not path.is_relative_to(self.root):
            return []

        files = []
        for item in sorted(path.iterdir()):
            if not item.exists() or item.name.startswith('.'):
                continue
            files.append(Dict({
                'path': item.relative_to(self.root),
                'mtime': item.stat().st_mtime,
                'size': item.stat().st_size,
                'is_dir': item.is_dir(),
            }))

        self.files[path] = files
        for item in files:
            if recursive and item.is_dir:
                self.scan_dir(self.root / item.path, recursive)

        return self.files[path]

    def on_modified(self, event):
        filepath = Path(event.src_path)
        if filepath.is_dir():
            self.scan_dir(filepath)

    def on_created(self, event):
        filepath = Path(event.src_path)
        if filepath.is_dir():
            self.scan_dir(filepath)

    def on_deleted(self, event):
        filepath = Path(event.src_path)
        if filepath.is_dir():
            self.files.pop(filepath, None)

    def on_moved(self, event):
        filepath = Path(event.dest_path)
        if filepath.is_dir():
            self.scan_dir(filepath)

    def start(self):
        self.observer = Observer()
        self.observer.schedule(self, self.root, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()


if __name__ == "__main__":
    path = "."  # 监控当前目录
    event_handler = FileMonitor(path)
    observer = Observer()
    # recursive=True 监控子目录
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
