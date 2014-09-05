from argparse import ArgumentParser
from subprocess import call
import functools
import logging
import os.path
import platform
import shlex
import signal
import threading
import time

signal.signal(signal.SIGINT, signal.SIG_DFL)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.INFO)


SYNC_DELAY = 0.1


def _ensure_trailing_slash_present(path_spec):
    path_spec = os.path.normpath(path_spec)

    if path_spec[-1] != os.sep:
        path_spec += os.sep
    return path_spec


class Syncer(threading.Thread):
    """
     Automatically keep two directory structures synchronized. This sync is push
     only, i.e. changes made where the script is run will overwrite the files in
     the destination directory.

     For improved performance, add the following to your ~/.ssh/config file:
     Host <recipient host name>
        ControlPath ~/.ssh/master-%r@%h:%p
        ControlMaster no

     Where <recipient host name> is the DNS name of the computer that receives
     your files. For example, if I'm syncing from localhost to devapp001, the
     recipient host name is devapp001.

    """
    def __init__(self, options):
        super(Syncer, self).__init__()

        self.options = options
        self.source = _ensure_trailing_slash_present(self.options.source)
        self.remote_spec = _ensure_trailing_slash_present(
            self.options.remote_spec)

        self.lock = threading.Lock()
        self.last_event = 0
        self.path = None

    def add_event(self, path):
        with self.lock:
            self.last_event = time.time()
            if self.path is None:
                self.path = path
            else:
                self.path = os.path.commonprefix([self.path, path])

    def set_tab_title(self, title):
        if 'Darwin' in platform.system():
            cmd = 'echo -n "\033]0;%s\007"' % title
            call(shlex.split(cmd))

        logging.info(title)

    def watch_complete(self):
        self.path = None
        self.set_tab_title("Watching...")

    def sync_cb(self):
        with self.lock:
            if not self.path or time.time() - self.last_event < SYNC_DELAY:
                return

            normalized_path = os.path.normpath(self.path)
            if os.path.isdir(normalized_path):
                normalized_path += os.sep

            excludes = ["*.pyc", "*.ldb", ".DS_Store", "pinboard.css", "build", "node_modules"]
            excludes.extend(self.options.extra_excludes)

            if self.options.exclude_git:
                if ".git" in normalized_path:
                    self.watch_complete()
                    return
                excludes.append(".git")

            exclude_cmd = ""

            for exclude in excludes:
                exclude_cmd += " --exclude '%s'" % exclude

            self.set_tab_title('Syncing %s' % self.source)
            cmd = "/usr/bin/rsync -avz --delete {excludes} {source} {remote_spec}".format(
                excludes=exclude_cmd,
                source=self.source,
                remote_spec=self.remote_spec)

            call(shlex.split(cmd))
            self.watch_complete()

    def run(self):
        while True:
            self.sync_cb()
            time.sleep(SYNC_DELAY / 2)


def file_changed(add_event, options, subpath, mask):
    if options.exclude_git and subpath.endswith(".git/"):
        return
    add_event(subpath)


parser = ArgumentParser(description="Push local changes to a remote server")
parser.add_argument("-s", dest="source", help="the directory to monitor",
                    required=True)
parser.add_argument("--exclude-git", dest="exclude_git", action="store_true")
parser.add_argument(
    "--exclude", dest="extra_excludes", action="append", default=[])
parser.add_argument("remote_spec")

if __name__ == '__main__':
    options = parser.parse_args()

    syncer = Syncer(options)
    syncer.start()
    try:
        import fsevents

        observer = fsevents.Observer()
        stream = fsevents.Stream(
            functools.partial(file_changed, syncer.add_event, options), options.source)
        observer.schedule(stream)
        observer.run()
    except ImportError:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class FileChangedHandler(FileSystemEventHandler):
            """Logs all the events captured."""

            def __init__(self, syncer):
                self.syncer = syncer

            def on_any_event(self, event):
                super(FileChangedHandler, self).on_any_event(event)
                self.syncer.add_event(event.src_path)

        observer = Observer()
        observer.schedule(
            FileChangedHandler(syncer),
            path=options.source,
            recursive=True
        )
        observer.start()
    logging.info("Night gathers, and now my watch begins.")
