"""General-purpose utilities."""

import os
import uuid


def get_tmp_path() -> str:
    """Get random path in /tmp."""
    return os.path.join(os.path.sep, "tmp", str(uuid.uuid4()))
