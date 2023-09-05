import os.path

# Variables for paths
BASE = os.path.abspath("./data")
DB_PASSWORD_PATH = f"{BASE}/password/"
DB_MASTER_PATH = f"{BASE}/master/"

# Variables for master password management
USERNAME="user"
VERIFY_TIME = 5
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%M:%S"

# Variables for management master password
OK = 1
NO_OK = 2
NO_PASSWORD = 3
