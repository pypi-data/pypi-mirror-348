# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

__all__ = [
    "configuration",
    "eventhub",
    "taskflow",
    "taskpool",
    "tasksequence"
]

__name__ = "ezudesign"
__author__ = "numlinka"
__license__ = "LGPLv3"
__copyright__ = "Copyright (C) 2023 numlinka"

__version_info__ = (0, 3, 1)
__version__ = ".".join(map(str, __version_info__))

# internal
from . import configuration
from . import eventhub
from . import taskflow
from . import taskpool
from . import tasksequence
from . import utils
