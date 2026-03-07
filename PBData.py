import ast
import psutil
import subprocess
import sys
import os
from pathlib import Path, PurePath
from time import sleep
from io import TextIOWrapper
from datetime import datetime
import platform
import traceback
from pbgui_func import PBGDIR
from pbgui_purefunc import save_ini
from process_utils import ServiceBase, log_ts, rotate_log_if_needed
from Database import Database
from User import Users
import configparser
from collections import defaultdict
import asyncio

class PBData(ServiceBase):
    SERVICE_NAME = "PBData"
    SCRIPT_NAME = "PBData.py"
    PROCESS_SUFFIX = "pbdata.py"

    def __init__(self):
        self._init_service(PBGDIR, Path(f'{PBGDIR}/data/pid'), 'pbdata')
        self.db = Database()
        self.users = Users()
        self._fetch_users = []

    # fetch_users
    @property
    def fetch_users(self):
        return self._fetch_users
    @fetch_users.setter
    def fetch_users(self, new_fetch_users):
        self._fetch_users = new_fetch_users
        self.save_fetch_users()
    
    def load_fetch_users(self):
        pb_config = configparser.ConfigParser()
        try:
            pb_config.read('pbgui.ini', encoding='utf-8')
        except Exception as e:
            print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} Warning: failed reading pbgui.ini ({e}); keeping previous fetch_users: {self._fetch_users}")
            return
        if pb_config.has_option("pbdata", "fetch_users"):
            try:
                users = ast.literal_eval(pb_config.get("pbdata", "fetch_users"))
            except (ValueError, SyntaxError):
                print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} Warning: malformed fetch_users in pbgui.ini; keeping previous: {self._fetch_users}")
                return
            for user in users.copy():
                if user not in self.users.list():
                    users.remove(user)
            self.fetch_users = users
        else:
            self.fetch_users = []  # Default to empty list if not set
    
    def save_fetch_users(self):
        # Use safe locked write instead of direct ConfigParser write
        save_ini("pbdata", "fetch_users", f'{self.fetch_users}')

    # def update_db(self):
    #     # Load users first so filtering in load_fetch_users is correct
    #     self.users.load()
    #     self.load_fetch_users()
    #     print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} Users available: {self.users.list()}")
    #     print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} Will process users: {self.fetch_users}")
    #     processed = 0
    #     for user in self.users:
    #         if user.name in self.fetch_users:
    #             processed += 1
    #             print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} Processing user: {user.name} (exchange={user.exchange})")
    #             print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch history for {user.name}')
    #             self.db.update_history(user)
    #             print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch positions for {user.name}')
    #             self.db.update_positions(user)
    #             print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch orders for {user.name}')
    #             self.db.update_orders(user)
    #             print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch prices for {user.name}')
    #             self.db.update_prices(user)
    #             print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch balance for {user.name}')
    #             self.db.update_balances(user)
    #         else:
    #             print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} Skipping user: {user.name} (not in fetch_users)")
    #     if processed == 0:
    #         print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} No users matched fetch_users; nothing to fetch.")

    async def update_db_async(self):
        # Load users first so filtering in load_fetch_users is correct
        self.users.load()
        self.load_fetch_users()
        print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} [async] Will process users: {self.fetch_users}")

        # Group users by exchange
        users_by_exchange = defaultdict(list)
        for user in self.users:
            if user.name in self.fetch_users:
                users_by_exchange[user.exchange].append(user)

        # For each exchange, create a task to process its users serially
        exchange_tasks = []

        for exchange, users in users_by_exchange.items():
            print(f"{datetime.now().isoformat(sep=' ', timespec='seconds')} [async] Queueing {len(users)} user(s) for exchange: {exchange}")
            # Run each exchange's users sequentially
            exchange_tasks.append(self.process_exchange(users))

        # Run all exchanges concurrently
        await asyncio.gather(*exchange_tasks)

    async def process_exchange(self, users):
        # Process users serially within this exchange
        for user in users:
            await self.update_user_series(user)

    async def update_user_series(self, user):
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch history for {user.name}')
        # Wrap blocking sync db operations in threads
        await asyncio.to_thread(self.db.update_history, user)
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch positions for {user.name}')
        await asyncio.to_thread(self.db.update_positions, user)
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Fetch orders for {user.name}')
        await asyncio.to_thread(self.db.update_orders, user)

        # Run prices and balances concurrently
        await asyncio.gather(
            asyncio.to_thread(self.db.update_prices, user),
            asyncio.to_thread(self.db.update_balances, user)
        )
        print(f'{datetime.now().isoformat(sep=" ", timespec="seconds")} Updated prices and balances for {user.name}')

def main():
    """Entry point kept synchronous; spins up an async loop internally."""
    dest = Path(f'{PBGDIR}/data/logs')
    if not dest.exists():
        dest.mkdir(parents=True)
    logfile = Path(f'{str(dest)}/PBData.log')
    _log_out = open(logfile, "ab", 0)
    sys.stdout = TextIOWrapper(_log_out, encoding='utf-8', write_through=True)
    _log_err = open(logfile, "ab", 0)
    sys.stderr = TextIOWrapper(_log_err, encoding='utf-8', write_through=True)
    print(f'{log_ts()} Start: PBData')
    pbdata = PBData()
    if pbdata.is_running():
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print(f'{log_ts()} Error: PBData already started')
        exit(1)
    pbdata.save_pid()

    async def run_loop():
        while True:
            try:
                rotate_log_if_needed(logfile)
                await pbdata.update_db_async()
                await asyncio.sleep(1)
            except Exception as e:
                print(f'Something went wrong, but continue {e}')
                traceback.print_exc()

    asyncio.run(run_loop())

if __name__ == '__main__':
    main()