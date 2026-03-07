import psutil
import subprocess
import sys
import os
from pathlib import Path, PurePath
from time import sleep
from io import TextIOWrapper
from datetime import datetime
from Instance import Instances
import platform
import traceback
import logging
from process_utils import ServiceBase, log_ts, rotate_log_if_needed

class PBStat(ServiceBase, Instances):
    SERVICE_NAME = "PBStat"
    SCRIPT_NAME = "PBStat.py"
    PROCESS_SUFFIX = "pbstat.py"
    MAX_START_WAIT = 10

    def __init__(self):
        Instances.__init__(self)
        pbgdir = Path.cwd()
        self._init_service(str(pbgdir), Path(f'{pbgdir}/data/pid'), 'pbstat')

    def fetch_all(self):
        self.fetch_status()
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch trades and funding fees')
        for instance in self.instances:
            if instance.market_type == "spot":
                instance.save_status()
                instance.fetch_trades()
    def fetch_status(self):
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Start Fetch status')
        for instance in self.instances:
            if instance.market_type == "spot":
                print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Start Save Status {instance.user} {instance.symbol}')
                instance.save_status()
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} End Fetch status')

def main():
    logging.getLogger("streamlit.runtime.state.session_state_proxy").disabled=True
    logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").disabled=True
    pbgdir = Path.cwd()
    dest = Path(f'{pbgdir}/data/logs')
    if not dest.exists():
        dest.mkdir(parents=True)
    logfile = Path(f'{str(dest)}/PBStat.log')
    sys.stdout = TextIOWrapper(open(logfile,"ab",0), encoding='utf-8', write_through=True)
    sys.stderr = TextIOWrapper(open(logfile,"ab",0), encoding='utf-8', write_through=True)
    print(f'{log_ts()} Start: PBStat')
    stat = PBStat()
    if stat.is_running():
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print(f'{log_ts()} Error: PBStat already started')
        exit(1)
    stat.save_pid()
    trade_count = 0
    while True:
        try:
            rotate_log_if_needed(logfile)
            if trade_count%5 == 0:
                stat.fetch_all()
            else:
                stat.fetch_status()
            trade_count += 1
            sleep(60)
            # Refresh Instances if there are some new or removed
            stat.instances = []
            stat.load()
        except Exception as e:
            print(f'Something went wrong, but continue {e}')
            traceback.print_exc()

if __name__ == '__main__':
    main()