
import hashlib
import json


def record_hash(record):
    """Generate a SHA-256 hash from a record's contents."""
    payload = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_record_id(record, id_field):
    """
    Build a unique record identifier.

    A string identifies a single field.
    A tuple/list identifies a composite key.
    """

    if isinstance(id_field, str):
        value = record.get(id_field)

        if value is None or str(value).strip() == "":
            raise ValueError(f"Missing record identifier: {id_field}")

        return str(value)

    if isinstance(id_field, (tuple, list)):
        values = []

        for field in id_field:
            value = record.get(field)

            if value is None or str(value).strip() == "":
                raise ValueError(f"Missing record identifier: {field}")

            values.append(value)

        return json.dumps(values, separators=(",", ":"), default=str)

    raise TypeError("id_field must be a string, tuple, or list")


def detect_changes(conn, entity_type, records, id_field):
    """
    Compare a complete current snapshot with persisted source hashes.

    Returns four groups:
    insert, update, unchanged and delete.

    Delete detection assumes records represent a complete snapshot.
    """

    previous = {
        row["record_id"]: row
        for row in conn.execute(
            """
            SELECT record_id, row_hash, is_deleted
            FROM source_state
            WHERE entity_type = ?
            """,
            (entity_type,),
        ).fetchall()
    }

    current_ids = set()

    changes = {
        "insert": [],
        "update": [],
        "unchanged": [],
        "delete": [],
    }

    for record in records:
        record_id = build_record_id(record, id_field)

        if record_id in current_ids:
            raise ValueError(
                f"Duplicate record identifier in {entity_type}: {record_id}"
            )

        current_ids.add(record_id)

        digest = record_hash(record)
        old = previous.get(record_id)

        if old is None:
            changes["insert"].append((record, digest))

        elif old["row_hash"] != digest or old["is_deleted"]:
            changes["update"].append((record, digest))

        else:
            changes["unchanged"].append((record, digest))

    # Records previously present but missing from the complete snapshot
    # are classified as deleted.
    for record_id, old in previous.items():
        if record_id not in current_ids and not old["is_deleted"]:
            changes["delete"].append(record_id)

    return changes


def save_source_state(
    conn,
    entity_type,
    record_id,
    digest,
    is_deleted,
    timestamp,
):
    """Insert or update the persisted CDC state."""

    conn.execute(
        """
        INSERT INTO source_state (
            entity_type,
            record_id,
            row_hash,
            is_deleted,
            last_seen_at
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(entity_type, record_id)
        DO UPDATE SET
            row_hash = excluded.row_hash,
            is_deleted = excluded.is_deleted,
            last_seen_at = excluded.last_seen_at
        """,
        (
            entity_type,
            str(record_id),
            digest,
            int(is_deleted),
            timestamp,
        ),
    )
