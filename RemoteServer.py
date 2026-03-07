"""
RemoteServer class manages a remote server's configuration and synchronization with cloud storage.

RemoteServer() creates a profile for the local server to interact with the remote storage,
it imports the information from remote to local, and will update the status after doing so.
"""
import subprocess
import gzip
import json
import hashlib
import shutil
import platform
from pathlib import Path, PurePath
from datetime import datetime
import glob

from Status import InstancesStatus
from PBRun import PBRun
from process_utils import run_logged_command


class RemoteServer():
    def __init__(self, path: str):
        """
        Initialize a RemoteServer instance to manage PB configurations.

        It exports both multi and single configurations to the remote storage.
        It lists the instances that will be used in PBRun (_instances) and verifies that the API keys in PB directory are up to date.

        Args:
            path (str): Path to the remote server configuration.
        """
        self._name = None
        self._ts = 0
        self._startts = 0
        self._rtd = None
        self._edit = False
        self._path = path
        self._unique = []
        self._api_md5 = None
        self._pbdir = None
        self._pb7dir = None
        self._bucket = None
        # self._instances = []
        self._mem = []
        self._swap = []
        self._disk = []
        self._cpu = 0
        self._boot = 0
        self._monitor = []
        self._upgrades = 0
        self._reboot = False
        self._cmc_credits = 0
        self._role = None
        self._pbgui_version = "N/A"
        self._pbgui_commit = None
        self._pb6_version = "N/A"
        self._pb6_commit = None
        self._pb7_version = "N/A"
        self._pb7_commit = None
        self.pbname = None
        self.instances_status = InstancesStatus(f'{self.path}/status.json')
        self.instances_status.load()
        self.instances_status_single = InstancesStatus(f'{self.path}/status_single.json')
        self.instances_status_single.load()
        self.instances_status_v7 = InstancesStatus(f'{self.path}/status_v7.json')
        self.instances_status_v7.load()

    @property
    def name(self): return self._name
    @property
    def ts(self): return self._ts
    @property
    def startts(self): return self._startts
    @property
    def rtd(self): return self._rtd
    @property
    def edit(self): return self._edit
    @property
    def path(self): return self._path
    @property
    def api_md5(self): return self._api_md5
    @property
    def pbdir(self): return self._pbdir
    @property
    def pb7dir(self): return self._pb7dir
    @property
    def bucket(self): return self._bucket
    @property
    def mem(self): return self._mem
    @property
    def swap(self): return self._swap
    @property
    def disk(self): return self._disk
    @property
    def cpu(self): return self._cpu
    @property
    def boot(self): return self._boot
    @property
    def monitor(self): return self._monitor
    @property
    def upgrades(self): return self._upgrades
    @property
    def reboot(self): return self._reboot
    @property
    def cmc_credits(self): return self._cmc_credits
    @property
    def role(self): return self._role
    @property
    def pbgui_version(self): return self._pbgui_version
    @property
    def pbgui_commit(self): return self._pbgui_commit
    @property
    def pb6_version(self): return self._pb6_version
    @property
    def pb6_commit(self): return self._pb6_commit
    @property
    def pb7_version(self): return self._pb7_version
    @property
    def pb7_commit(self): return self._pb7_commit

    @name.setter
    def name(self, new_name):
        if self._name != new_name:
            self._name = new_name
    @ts.setter
    def ts(self, new_ts):
        if self._ts != new_ts:
            self._ts = new_ts
    @startts.setter
    def startts(self, new_startts):
        if self._startts != new_startts:
            self._startts = new_startts
    @edit.setter
    def edit(self, new_edit):
        if self._edit != new_edit:
            self._edit = new_edit
    @path.setter
    def path(self, new_path):
        if self._path != new_path:
            self._path = new_path
    @pbdir.setter
    def pbdir(self, new_pbdir):
        if self._pbdir != new_pbdir:
            self._pbdir = new_pbdir
    @pb7dir.setter
    def pb7dir(self, new_pb7dir):
        if self._pb7dir != new_pb7dir:
            self._pb7dir = new_pb7dir
    @bucket.setter
    def bucket(self, new_bucket):
        if self._bucket != new_bucket:
            self._bucket = new_bucket

    def is_api_md5_same(self, api_md5: str):
        """
        Check if the API MD5 hash is the same as the stored one.

        Args:
            api_md5 (str): The API MD5 hash to compare.

        Returns:
            bool: True if the API MD5 hash is the same, False otherwise.
        """
        if self.api_md5 == api_md5:
            return True
        return False

    def is_online(self):
        """
        Check if the remote server is online by loading the alive_*.cmd file and checking if the latest is less than 300 seconds ago.

        Returns:
            bool: True if the remote server is online, False otherwise.
        """
        self.load()
        timestamp = round(datetime.now().timestamp())
        self._rtd = timestamp - self.ts
        if self._rtd < 300:
            return True
        return False

    def load(self):
        """
        Load the server's configuration.
        """
        p = str(Path(f'{self._path}/alive_*.cmd*'))
        alive_remote = glob.glob(p)
        alive_remote.sort()
        self._name = PurePath(self._path).name[4:]
        if alive_remote:
            while len(alive_remote) > 0:
                remote = Path(alive_remote.pop())
                try:
                    if str(remote).endswith('.gz'):
                        with gzip.open(remote, "rt", encoding='utf-8') as f:
                            cfg = json.load(f)
                    else:
                        with open(remote, "r", encoding='utf-8') as f:
                            cfg = json.load(f)
                    if "name" in cfg and "timestamp" in cfg:
                        self._ts = cfg["timestamp"]
                    if "startts" in cfg:
                        self._startts = cfg["startts"]
                    if "api_md5" in cfg:
                        self._api_md5 = cfg["api_md5"]
                    if "mem" in cfg:
                        self._mem = cfg["mem"]
                    if "swap" in cfg:
                        self._swap = cfg["swap"]
                    if "disk" in cfg:
                        self._disk = cfg["disk"]
                    if "cpu" in cfg:
                        self._cpu = cfg["cpu"]
                    if "boot" in cfg:
                        self._boot = cfg["boot"]
                    if "monitor" in cfg:
                        self._monitor = cfg["monitor"]
                    if "upgrades" in cfg:
                        self._upgrades = cfg["upgrades"]
                    if "reboot" in cfg:
                        self._reboot = cfg["reboot"]
                    if "cmc" in cfg:
                        self._cmc_credits = cfg["cmc"]
                    if "role" in cfg:
                        self._role = cfg["role"]
                    if "pbgv" in cfg:
                        self._pbgui_version = cfg["pbgv"]
                    if "pbgc" in cfg:
                        self._pbgui_commit = cfg["pbgc"]
                    if "pb6v" in cfg:
                        self._pb6_version = cfg["pb6v"]
                    if "pb6c" in cfg:
                        self._pb6_commit = cfg["pb6c"]
                    if "pb7v" in cfg:
                        self._pb7_version = cfg["pb7v"]
                    if "pb7c" in cfg:
                        self._pb7_commit = cfg["pb7c"]
                    return
                except Exception as e:
                    print(f'{str(remote)} is corrupted {e}')

    def sync_v7_down(self, role: str):
        """Sync the v7 configurations from the remote storage to the local machine."""
        if self.instances_status_v7.has_new_status():
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} New status_v7.json from: {self.name}')
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Sync v7 from: {self.name}')
            pbgdir = Path.cwd()
            if role == "master":
                # cmd = ['rclone', 'sync', '-v', '--include', f'{{cmd_**/alive_*.cmd*,run_v7_{self.name}/**/*.json}}', f'{self.bucket}', PurePath(f'{pbgdir}/data/remote')]
                cmd = ['rclone', 'sync', '-v', '--filter', f'- cmd_{self.pbname}/*', '--filter', '+ cmd_**/alive_*.cmd*', '--filter', f'+ run_v7_{self.name}/**/*.json', '--filter', '- *', f'{self.bucket}', PurePath(f'{pbgdir}/data/remote')]
            else:
                cmd = ['rclone', 'sync', '-v', '--include', f'{{*.json}}', f'{self.bucket}/run_v7_{self.name}', PurePath(f'{pbgdir}/data/remote/run_v7_{self.name}')]
            logfile = Path(f'{pbgdir}/data/logs/sync.log')
            run_logged_command(cmd, pbgdir, logfile)
            PBRun().update_status(self.instances_status_v7.status_file, self.name)
            status_ts = self.instances_status_v7.status_ts
            self.instances_status_v7.update_status()
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Update status_v7 ts: {self.name} old: {status_ts} new: {self.instances_status_v7.status_ts}')

    def sync_multi_down(self):
        """Sync the multi configurations from the remote storage to the local machine."""
        if self.instances_status.has_new_status():
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} New status.json from: {self.name}')
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Sync multi from: {self.name}')
            pbgdir = Path.cwd()
            cmd = ['rclone', 'sync', '-v', '--include', f'{{multi.hjson,*.json}}', f'{self.bucket}/multi_{self.name}', PurePath(f'{pbgdir}/data/remote/multi_{self.name}')]
            logfile = Path(f'{pbgdir}/data/logs/sync.log')
            run_logged_command(cmd, pbgdir, logfile)
            PBRun().update_status(self.instances_status.status_file, self.name)
            status_ts = self.instances_status.status_ts
            self.instances_status.update_status()
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Update status ts: {self.name} old: {status_ts} new: {self.instances_status.status_ts}')

    def sync_single_down(self):
        """Sync the single configurations from the local machine to the remote storage."""
        if self.instances_status_single.has_new_status():
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} New status_single.json from: {self.name}')
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Sync single from: {self.name}')
            pbgdir = Path.cwd()
            cmd = ['rclone', 'sync', '-v', '--include', f'{{instance.cfg,config.json}}', f'{self.bucket}/instances_{self.name}', PurePath(f'{pbgdir}/data/remote/instances_{self.name}')]
            logfile = Path(f'{pbgdir}/data/logs/sync.log')
            run_logged_command(cmd, pbgdir, logfile)
            PBRun().update_status(self.instances_status_single.status_file, self.name)
            status_ts = self.instances_status_single.status_ts
            self.instances_status_single.update_status()
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Update status_single ts: {self.name} old: {status_ts} new: {self.instances_status_single.status_ts}')

    def sync_api(self):
        """
        Sync the API keys from the remote storage to the local machine.
        """
        api_file = Path(f'{self._path}/api-keys.json')
        if api_file.exists():
            if self.pbdir:
                api_keys = Path(f'{self._pbdir}/api-keys.json')
                self.update_api(api_file, api_keys, "v6")
            if self.pb7dir:
                api_keys = Path(f'{self._pb7dir}/api-keys.json')
                self.update_api(api_file, api_keys, "v7")

    def update_api(self, api_file: Path, api_keys: Path, version : str):
        """
        Checks if the api-keys.json from pbgui (self._path) is different from api-keys.json from passivbot.
        If different, It creates a backup of the passivbot api-keys.json to pbgui/data/backup, and then copy the new api-keys.json file to the passivbot directory.
        """
        if self.calculate_hash(api_file) != self.calculate_hash(api_keys):
            print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Install new API Keys from: {self.name} to {api_keys}')
            # Backup api-keys
            date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pbgdir = Path.cwd()
            if version == "v6":
                destination = Path(f'{pbgdir}/data/backup/api-keys/{date}')
            elif version == "v7":
                destination = Path(f'{pbgdir}/data/backup/api-keys_v7/{date}')
            if not destination.exists():
                destination.mkdir(parents=True)
            if api_keys.exists():
                shutil.copy(api_keys, destination)
            # Copy new api-keys
            shutil.copy(api_file, api_keys)

    def calculate_hash(self, file: Path):
        """Checks if the two API files have the same hash using SHA-256."""
        if file.exists():
            with open(file, 'rb') as file_obj:
                file_contents = file_obj.read()
            return hashlib.sha256(file_contents).hexdigest()
        return None

    def delete_server(self):
        """
        Delete the server from the remote storage.
        """
        pbgdir = Path.cwd()
        # rclone delete pbgui:pbgui --include *manibot51*/**
        cmd = ['rclone', 'delete', '-v', f'{self.bucket}', '--include', f'*{self.name}*/**']
        logfile = Path(f'{pbgdir}/data/logs/sync.log')
        run_logged_command(cmd, pbgdir, logfile)
        # delete local files
        shutil.rmtree(f'{pbgdir}/data/remote/cmd_{self.name}', ignore_errors=True)
        shutil.rmtree(f'{pbgdir}/data/remote/instances_{self.name}', ignore_errors=True)
        shutil.rmtree(f'{pbgdir}/data/remote/multi_{self.name}', ignore_errors=True)
        shutil.rmtree(f'{pbgdir}/data/remote/run_v7_{self.name}', ignore_errors=True)
