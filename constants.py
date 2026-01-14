"""
Constants module for PBGui.
Centralizes magic numbers and configuration values used throughout the codebase.
"""

# File size thresholds (in bytes)
FILE_SIZE_10MB = 10485760  # 10 * 1024 * 1024
FILE_SIZE_1MB = 1048576    # 1024 * 1024

# Time intervals (in seconds)
SECONDS_PER_DAY = 86400
ONLINE_THRESHOLD_SECONDS = 300  # 5 minutes
DEFAULT_SLEEP_INTERVAL = 60

# Memory thresholds (in MB)
DEFAULT_MEM_WARNING_MB = 250
DEFAULT_SWAP_WARNING_MB = 250
DEFAULT_DISK_WARNING_MB = 1000

# CPU thresholds (in percent)
DEFAULT_CPU_WARNING_PERCENT = 90

# CoinMarketCap defaults
DEFAULT_CMC_FETCH_LIMIT = 1000
DEFAULT_CMC_FETCH_INTERVAL = 4  # hours

# Service polling intervals (in seconds)
PBRUN_POLL_INTERVAL = 60
PBREMOTE_POLL_INTERVAL = 60
PBDATA_POLL_INTERVAL = 60
PBCOIN_POLL_INTERVAL = 14400  # 4 hours

# Default configuration values
DEFAULT_BACKTEST_CPU = 1
DEFAULT_OPTIMIZE_CPU = 1

# Log rotation
MAX_LOG_SIZE_BYTES = FILE_SIZE_10MB
