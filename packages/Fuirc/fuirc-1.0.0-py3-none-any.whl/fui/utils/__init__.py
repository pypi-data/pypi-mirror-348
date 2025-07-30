from fui.utils.browser import open_in_browser
from fui.utils.classproperty import classproperty
from fui.utils.deprecated import deprecated
from fui.utils.files import (
    copy_tree,
    get_current_script_dir,
    is_within_directory,
    safe_tar_extractall,
    which,
)
from fui.utils.hashing import calculate_file_hash, sha1
from fui.utils.network import get_free_tcp_port, get_local_ip
from fui.utils.once import Once
from fui.utils.platform_utils import (
    get_arch,
    get_bool_env_var,
    get_platform,
    is_android,
    is_asyncio,
    is_embedded,
    is_ios,
    is_linux,
    is_linux_server,
    is_macos,
    is_mobile,
    is_pyodide,
    is_windows,
)
from fui.utils.slugify import slugify
from fui.utils.strings import random_string
from fui.utils.vector import Vector
