import uuid

import ulid


def ulid_as_uuid() -> uuid.UUID:
    return ulid.new().uuid
