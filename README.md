# PBGui - GUI for Passivbot

> This repository is a **fork** of the original [msei99/pbgui](https://github.com/msei99/pbgui) project, optimized for running **PBGui Master on Windows 11 desktop PC** as the masternode that manages remote Linux VPS instances running Passivbot.

**Current Version:** v1.37

## Overview

Passivbot GUI (pbgui) is a web interface for Passivbot programmed in Python with Streamlit.

### Features

- Run, backtest, and optimize Passivbot v7 and v6 (single and multi-symbol modes)
- Install Passivbot configurations on your VPS
- Start and stop Passivbot instances on your VPS
- Move instances between your VPS servers
- Monitor your instances and automatically restart them if they crash
- Dashboard for viewing real-time trading performance
- CoinMarketCap integration for intelligent coin selection and filtering
- Install and update your VPS with just a few clicks
- And much more to easily manage Passivbot

### Requirements

- Python 3.10
- Streamlit 1.50.0
- Linux (Ubuntu 24.04 recommended) or Windows 11

### Recommended Hardware

- **Master Server:** Windows 11 desktop PC (this fork's primary target) or Linux server with sufficient resources (e.g., 32GB RAM, 8 CPUs)
- **VPS for Running Passivbot:** Minimum specifications of 1 CPU, 1GB Memory, and 10GB SSD

## Code Architecture

PBGui is organized into a modular Python package structure for better maintainability and testing:

```
pbgui/
├── pbgui.py                    # Entry point (Streamlit app launcher)
├── Config.py                   # Compatibility alias for legacy imports
├── Exchange.py                 # Compatibility alias for legacy imports
├── pbgui/                      # Main package
│   ├── configs/                # Configuration hierarchy
│   │   ├── v6/                 # Passivbot v6 config classes
│   │   └── v7/                 # Passivbot v7 config classes
│   │       ├── config.py       # Main v7 config
│   │       ├── bot.py          # Bot settings
│   │       ├── long.py         # Long position settings
│   │       ├── short.py        # Short position settings
│   │       ├── backtest.py     # Backtest settings
│   │       ├── optimize.py     # Optimization settings
│   │       └── ...
│   ├── ui/                     # UI components
│   ├── balance_calculator.py   # Balance calculation utilities
│   ├── compat_patches.py       # Backward compatibility helpers
│   └── utils.py                # Shared utilities
├── exchanges/                  # Exchange-specific implementations
│   ├── base.py                 # Base exchange class
│   ├── binance.py              # Binance integration
│   ├── bybit.py                # Bybit integration
│   ├── okx.py                  # OKX integration
│   └── ...
├── pb_configs/                 # Configuration templates and models
└── navi/                       # Streamlit page modules
```

**Key Design Principles:**

- **Modular Structure**: Code organized by functionality (configs, exchanges, UI)
- **Backward Compatibility**: Legacy imports still work via compatibility aliases
- **Separation of Concerns**: Exchange logic separated from config management
- **Type Safety**: Structured configuration classes with validation
- **Maintainability**: Smaller, focused modules instead of monolithic files

For detailed architecture information, see [CLAUDE.md](CLAUDE.md).

## Contact & Support

- **Telegram Support:** https://t.me/+kwyeyrmjQ-lkYTJk
- **Copytrading Platform:** https://manicpt.streamlit.app/
- **API Service:** I offer API-Service where I run Passivbot for you as a managed service. Contact me on Telegram for more information.

### Support the Project

If you'd like to support PBGui, please consider:
- Join one of my copytrading services at https://manicpt.streamlit.app/
- If you don't have a Bybit account, use my referral code: **XZAJLZ** at https://www.bybit.com/invite?ref=XZAJLZ
- Donate via Ko-fi (link above)

### Get Your VPS for Running Passivbot

I recommend the following VPS providers:

- **IONOS** - Smallest VPS plan available for only 1 Euro. I've been using their services for over a year without any outages. Use my [referral link](https://aklam.io/esMFvG)
- **RackNerd** - Nice small VPS for $11/year. Use my [referral link](https://my.racknerd.com/aff.php?aff=15714)
- **Contabo** - Good alternative VPS provider. Use my [referral link](https://www.tkqlhce.com/click-101296145-12454592)

---

## Installation

### Option 1: Manual Installation for All Linux Distributions

Clone PBGui and Passivbot v6 and v7:

```bash
git clone https://github.com/djienne/pbgui.git
git clone https://github.com/enarjord/passivbot.git pb6
git clone https://github.com/djienne/passivbot.git
```

Install Python 3.10

```bash
# Check if Python 3.10 is installed
python3.10 --version

If not installed, install it first:
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv
```

Create virtual environments:


```bash
python3.10 -m venv venv_pbgui
python3.10 -m venv venv_pb6
python3.10 -m venv venv_pb7
```

Install requirements for pb6, pb7, and pbgui:

```bash
# Install pbgui
source venv_pbgui/bin/activate
cd pbgui
pip install --upgrade pip
pip install -r requirements.txt

# Install pb6 (optional)
source venv_pb6/bin/activate
cd pb6
git checkout v6.1.4b
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

# Install pb7
source venv_pb7/bin/activate
cd pb7
pip install --upgrade pip
pip install -r requirements.txt
cd passivbot-rust/
sudo apt-get install rustc cargo
maturin develop --release
deactivate
cd ../..
```

Start PBGui with:

```bash
streamlit run pbgui.py
```

---

### Option 2: Windows 11 Installation (No WSL)

These steps describe how to run PBGui directly on Windows 11 using Python 3.10 from Chocolatey.

#### 1. Install Prerequisites (PowerShell as Administrator)

```powershell
choco install python --version=3.10.11 -y   # if Python 3.10 is not installed
choco install git -y                        # to clone the repo
choco install rclone -y                     # optional, needed for PBRemote/VPS buckets
```

#### 2. Clone the Repository

```powershell
git clone https://github.com/djienne/pbgui.git
cd pbgui
```

#### 3. Create and Activate a Virtual Environment

```powershell
py -3.10 -m venv venv_pbgui
.\venv_pbgui\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** Some VPS-manager features use Ansible to manage Linux VPSs. Ansible itself only targets Linux hosts; on Windows, use these features only to manage remote Linux servers, not the local machine.

#### 4. Run PBGui on Windows

```powershell
streamlit run pbgui.py
```

Then open `http://localhost:8501` in your browser.

On first run, configure your `pb6/pb7` and virtualenv paths in the GUI. For most Windows users, it is recommended to let PBGui manage **remote Linux** VPSs (as described in the Linux sections above) instead of running Passivbot locally.

---

### Option 5: Docker (Any OS)

Want to use **Docker** instead? Follow this [Quickstart guide](https://github.com/LeonSpors/passivbot-docker).

---

## Running PBGui

Start PBGui with:

```bash
streamlit run pbgui.py
```

Open `http://localhost:8501` in your browser.

**Default credentials:**
- Password: `a`
- Change password in file: `.streamlit/secrets.toml`

**First run configuration:**
1. Select your Passivbot and venv directories
2. For the venv, enter the full path to Python
   - Example path for venv_pb7: `/home/mani/software/venv_pb7/bin/python`
3. Select "Master" on Welcome Screen if this system is used to send configs to VPS

### Configuration File Safety

PBGui stores your local settings in `pbgui.ini`. This file is automatically created from `pbgui.ini.example` on first run.

**Important notes:**
- ✅ `pbgui.ini` is **excluded from git** (in `.gitignore`) and will not be affected by `git pull` operations
- ✅ **Automatic backup**: Every time settings are saved, a backup is created at `pbgui.ini.backup`
- ✅ **Auto-recovery**: If `pbgui.ini` is corrupted or missing, it will be automatically restored from backup or recreated from the example file
- ✅ Your local configuration (paths, API keys, bot names) will **never be reset** by git operations or restarts

If you need to reset your configuration to defaults, simply delete `pbgui.ini` and restart PBGui.

---

## Services Configuration

### PBRun - Instance Manager

To enable the PBGui instance manager:

1. Open the PBGui interface
2. Go to **Services** and enable **PBRun**

To ensure that the Instance Manager starts after rebooting your server, you can use the following method:

1. Create a script file `start.sh` in your pbgui directory (e.g., `~/software/pbgui`):

```bash
#!/usr/bin/bash
venv=~/software/pb_env # Path to your Python virtual environment
pbgui=~/software/pbgui # Path to your PBGui installation

source ${venv}/bin/activate
cd ${pbgui}
python PBRun.py &
```

2. Save the script file and make it executable:

```bash
chmod 755 start.sh
```

3. Open your crontab file:

```bash
crontab -e
```

4. Add the following line to execute the script at reboot:

```bash
@reboot ~/software/pbgui/start.sh
```

5. Save the crontab file

**Note:** Adjust the paths according to your specific setup.

### PBStat - Statistics

This is only needed if you trade spot and want statistics. The best way to enable PBStat is by adding the following line to your `start.sh` script:

```bash
python PBStat.py &
```

### PBData - Database for Dashboard

To enable PBData for the dashboard, add the following line to your `start.sh` script:

```bash
python PBData.py &
```

This command will run PBData in the background, filling the database for the dashboard.

### PBRemote - Server Manager

You can install rclone and configure bucket using PBGui. Go to **Services → PBRemote → Show Details**.

With PBRemote, you can efficiently manage Passivbot instances on multiple servers directly from your PC. This includes starting, stopping, removing, and syncing instances from and to your servers.

PBRemote utilizes rclone to establish communication via cloud storage with your servers. The advantage is that you do not need to open any incoming firewall ports on your PC or servers. Additionally, all your Passivbot config data is securely transferred and stored on your preferred cloud storage provider.

rclone supports over 70 cloud storage providers. More information at https://rclone.org/.

#### Manual rclone Installation

```bash
sudo -v ; curl https://rclone.org/install.sh | sudo bash
```

#### Recommended Cloud Storage

As a recommendation, Synology C2 Object Storage offers a reliable option. They provide 15GB of free storage. Sign up at https://c2.synology.com/en-uk/object-storage/overview.

After registration, create your bucket using your own unique name (note: "pbgui" is already taken).

#### Manual Rclone Configuration (Synology)

```bash
rclone config create <bucket_name> s3 provider=Synology region=eu-002 endpoint=eu-002.s3.synologyc2.net no_check_bucket=true access_key_id=<key> secret_access_key=<secret>
```

#### Configure pbgui.ini on VPS

You need to configure `pbgui.ini` with a minimum of these settings on your VPS:

```ini
[main]
pbdir = /home/mani/software/pb6
pbvenv = /home/mani/software/venv_pb6/bin/python
pb7dir = /home/mani/software/pb7
pb7venv = /home/mani/software/venv_pb7/bin/python
pbname = manibot50

[pbremote]
bucket = pbgui:
```

**Note:** There is no need to install or run Streamlit on your Remote Server. Start PBRun.py and PBRemote using the start.sh script.

### PBCoinData - CoinMarketCap Filters

With PBCoinData, you can download CoinMarketCap data for symbols and use this data to maintain your ignored_symbols and ignored_coins. You can filter out low market cap symbols or use vol/mcap to detect possible rug pulls early.

You need to configure the `pbgui.ini` file with a minimum of the following settings on your VPS:

```ini
[coinmarketcap]
api_key = <your_api_key>
fetch_limit = 1000
fetch_interval = 4
```

With these settings, PBCoinData will fetch the top 1000 symbols every 4 hours. You will need around 930 credits per month with this configuration.

A Basic Free Plan from CoinMarketCap provides 10,000 credits per month, allowing you to run 1 master and 9 VPS instances with the same API key.

Start PBCoinData.py using the start.sh script.

### Running on Windows

**Note:** Not tested with Passivbot 7.

Copy `start.bat.example` to `start.bat`. Edit `pbguipath` in the `start.bat` to your pbgui installation path. Add `start.bat` to Windows Task Scheduler and use Trigger "At system startup".

---

## Changelog

### v1.37 (2025-10-19)

- Compatible with Passivbot 7.4.1
- Resize swap size on VPS
- PBRemote optimized for more than 10 VPS
- Update to Streamlit 1.50
- Save default sort options
- Display CMC credits left for VPS
- Dashboard new income as list
- Setup VPS with private key or user/password
- Bug fixes

### v1.36 (2025-08-07)

- Added coin_overrides and removed old coin_flags
- Converted coin_flags to coin_overrides
- New ADG Dashboard
- Drawdown view for backtests
- Moved navigation to the top for more space on the left
- VPS cleanup to free up storage
- Option to skip installation or remove v6 bot from VPS
- Balance calculator
- Many bug fixes

### v1.35 (2025-06-01)

- Added new options from Passivbot v7.3.13:
  - close_grid_markup_start, close_grid_markup_end
  - mimic_backtest_1m_delay
  - trailing_double_down_factor
- Config Archive
- Many small improvements
- Bug fixes
- Update ccxt for work with OKX

### v1.34 (2025-04-21)

- Compatible with Passivbot v7.3.4
- Using fragments for speedup GUI
- Support for GateIO
- Send Telegram messages on bot errors
- Logarithmic view of backtests
- TWE and WE view on backtests v7
- Update to Streamlit v1.44
- Hundreds of bug fixes

### v1.33 (2024-12-30)

- Filter for coins with warnings on CoinMarketCap
- Multi: Added only_cpt and apply_filter function
- Improved GridVis by Sephral
- Fetch notice from CoinMarketCap metadata for display warning messages
- Added preset manager for optimizer v7 by Sephral
- Small bug fixes

### v1.32 (2024-12-26)

- Converter for pb6 to pb7 configurations
- View Monitor for all VPS on one page
- Small bug fixes

### v1.31 (2024-12-16)

- Added coin_flags to pb7 run
- Reworked GridVisualizer
- Updated SYMBOLMAP for CoinData
- Change balance on Bybit to totalWalletBalance
- Add install.sh for easy install PBGui, pb6, and pb7 on Ubuntu
- Filters for all_results
- Added PBGui Logo
- Bug fix: update VPS will no longer install all requirements.txt
- PBGui can now run without password
- Change password dialog
- pb7.2.10 multi-exchange optimizer/backtester compatibility
- Many more bug fixes

### v1.30 (2024-12-03)

- Added apply_filters for static symbol selection
- ignored_symbols will now always be added to the dynamic_ignore
- Preview of dynamic_ignore when enabling it
- Added copytrading only to dynamic_ignore filter
- Tags can be used as dynamic_ignore filter for running bots
- Add Tags filter from CoinMarketCap (example: memes, gaming, defi, layer-2, etc.)
- Compare Backtests from All Results
- Show All Results on Backtest V7
- Update to Streamlit 1.40
- Add Position Value to Dashboard Positions
- Small bug fixes
- Small cosmetic changes

### v1.29 (2024-11-29)

- Make PBGui Passivbot v7.2.9 compatible
- Backtest V7 Compare results added
- Install requirements when updating VPS or master
- Small bug fixes
- Added ko-fi for donations

### v1.28 (2024-11-24)

- VPS-Manager: Check for working rclone on Master before Setup a VPS
- Added GUI Setup for rclone buckets (Services PBRemote)
- Added Test Connection for rclone buckets
- VPS-Manager: Install and Update rclone on Master
- Bug fix: Optimize V7 corrupted results
- Higher verbosity level when setup VPS and select debug
- Disable IPv6 on VPS using grub
- Coindata fix for NEIROETHUSDT on Binance and correct market cap
- Bug fix: Hyperliquid import
- Expanded settings when setup a new VPS

### v1.27 (2024-11-19)

- Bug fix: Results Backtest Single
- PBRemote: Added delete function for offline Remote Servers with cleanup remote storage
- VPS-Manager: Find new added VPS after a refresh of the page
- VPS-Manager: View logfiles from VPS
- VPS-Manager: Don't allow adding VPS with same names
- New P+L Dashboard (Sephral)
- New Navigation (Sephral)
- Added V7 Grid Visualizer (Sephral)
- Added optional notes to instances (Sephral)
- Improved Title & Page Headers (Sephral)
- VPS-Manager: Added update function for localhost (Master) for pbgui, pb6, and pb7
- Many small bug fixes
- More small improvements

### v1.26 (2024-11-13)

- VPS-Manager: Always build rust when update v7 Passivbot
- VPS-Manager: Show status of PBGui Master
- VPS-Manager: Selectbox for easy switch between VPS
- VPS-Manager: Add option to delete a VPS
- VPS-Manager: Bug fix for unknown VPS hosts
- Bug fixes: vol_mcap
- Select logfile size and view reverse for speed up big logfiles
- Bug fix: API-Editor don't let you delete users that are used by pb7
- Bug fix: Load v7 users without need to have pb6 installed
- Show an OK when paths for pb6, pb7, and venvs are correct
- Remove /../.. from paths
- No longer need to restart Passivbot 7 instances when dynamic_ignore selects new coins
- More small bug fixes

### v1.25 (2024-11-10)

- Rewrite Config Module
- Bug fix for not saving selected coins
- Disable IPv6 on VPS setup
- Bug fix: import config v7 on backtest and run

### v1.24 (2024-11-09)

- Added approved_coins_long and _short
- Added ignored_coins_long and short
- Added empty_means_all_approved option from v7.2.2
- Added compress_cache option on backtest_v7
- Bug fix for new Passivbot v7.2.2
- Copy optimize_result before running analysis to avoid locking errors
- Bug fix for PBRun create_parameters on pb6 single instances
- Bug fix for update pb6 and pb7 ignore error when no instance is running
- More small bug fixes

### v1.23 (2024-11-07)

- PBRun/PBRemote: Check if updates for Linux and reboot needed
- VPS-Manager: Overview of all VPS running versions and update/reboot status
- PBRemote: Compression for alive files, 75% less data usage
- VPS-Manager: Update only PBGui without pb6 and pb7
- PBRun/PBRemote: Gather pbgui/pb6/pb7 versions and send them to master

### v1.22 (2024-11-05)

- VPS-Manager: UFW Firewall configuration
- VPS-Manager: Update pbgui, pb6, and pb7 and restart Passivbot after update
- VPS-Manager: Update Linux
- VPS-Manager: Reboot VPS
- VPS-Manager: View Status and running Passivbots
- Bug fix: Don't allow passwords with {{ or }}
- Add Master/Slave role for using less traffic on PBRemote

### v1.21 (2024-10-29)

- VPS-Manager: Fully automate setup your VPS with PBGui, PB6, and PB7
- starter.py for start, stop, restart PBRun, PBRemote, and PBCoinData
- PBRemote: Finds new VPS without restart
- Some small bug fixes for new v7 functions

### v1.20 (2024-10-22)

- V7: Added all latest config options to live and optimizer
- V7 Run: Added Dynamic filter for mcap and vol/mcap
- Multi: Filters for marketcap and vol/mcap added
- Multi: Dynamic filter for mcap and vol/mcap added
- PBRun: Dynamic filter update ignored_symbols
- PBCoinData: Update on start and every 24h symbols from all exchanges

### v1.19 (2024-10-20)

- CoinMarketCap integration
- V7 Run and Optimize filters for marketcap and vol/mcap added
- New Service PBCoinData fetch data from CoinMarketCap

### v1.18 (2024-10-13)

- Services: Show PNL Today, Yesterday from LogMonitor
- Services: Show Logmonitor Information Memory, CPU, Infos, Errors, Tracebacks
- PBRun/PBRemote: Monitor Passivbot logs and send infos to master
- PBData: Reload User on every run for new added Users
- PBRun: Recompile rust if new pb7 version is installed
- PBData: Bug fix when removing User from API
- V7: Add Exchange and Time information
- Bug fix: Update Symbols from Binance

### v1.17 (2024-10-02)

- V7: Run optimizer from a backtest result with -t starting_config
- Run V7 and Multi: Add All and Add CPT Symbols to approved_symbols
- Multi: lap, ucp, and st in the Overview of Multi Run
- V7: Compile rust if needed
- V7: Show final_balance in backtests for easy sort them
- V7: Refresh logfile fragment for speedup

### v1.16 (2024-09-28)

- Run V7: First version that can run Passivbot v7
- PBRun: Can now start Passivbot v7 instances
- PBRemote: Sync v7 added

### v1.15 (2024-09-24)

- Backtest V7: Added backtester for Passivbot v7
- Bug fix: Optimizer autostart
- Optimizer V7: Added Name to results
- Bug fix: venv for old Passivbot

### v1.14 (2024-09-19)

- Optimize V7: Added optimizer for Passivbot v7
- Add api-keys for Passivbot version 7
- Check for installed Passivbot versions
- Split venv pbgui and venv Passivbot / Config Option for venv Passivbot v6 and v7
- Dashboard: Added Timeframe to Order View and move the time left/right

### v1.13 (2024-09-11)

- Bug fix: Multi Backtest Results, corrected time in View Results
- Removed PBShare, Live View, Grid Share for futures and removed old code from PBRun and PBRemote
- Speed up when starting PBGui
- Bug fix: Bitget Single

### v1.12 (2024-08-31)

- Dashboard: Bug fix Hyperliquid Price and Candlesticks timeframe
- Dashboard: Added Hyperliquid to PBData and Dashboard
- Multi and API-Editor: Added Hyperliquid
- Multi: Added Button for Update Symbols from Exchange
- Bug fix for configparser - under certain circumstances, configuration from other sections was being lost

### v1.11 (2024-08-27)

- Dashboard: Change Bybit Income from positions_history to transactions for more accurate income history
- Dashboard: Kucoin added
- Dashboard: Move panels added
- Dashboard: Added 'ALL' to user selections

### v1.1 (2024-08-20)

- Dashboard: Added Dashboards for replacing the Live View in future versions of PBGui
- Dashboard: Added a SQLite database for fast view of the dashboards
- PBData: New scraper for fetch balance, positions, orders, prices, and income from exchanges

### v1.01 (2024-07-23)

- Optimize_Multi: Bug fix for object has no attribute 'hjson'
- Multi: Bug fix price_distance_threshold

### v1.0 (2024-07-23)

- Optimize_Multi: Generate Analysis from all_results added
- Optimize_Multi: Create Backtest from Analysis (Result)
- Optimize_Multi: Remove Results added
- Optimize_Multi: First running version with multi optimizer

---

## Links

- **Telegram:** https://t.me/+kwyeyrmjQ-lkYTJk
- **Passivbot:** https://www.passivbot.com/en/latest/
- **Streamlit:** https://streamlit.io/

---

## Screenshots

![Dashboard](docs/images/dashboard.png)
![Run](docs/images/run.png)
![Backtest](docs/images/backtest.png)
![Optimize](docs/images/optimize.png)
