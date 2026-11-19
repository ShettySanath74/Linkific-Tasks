
import json
from datetime import datetime

from .cdc import detect_changes, save_source_state, record_hash, build_record_id
from .error_handler import retry

ID_FIELDS = ("order_id", "line_number")

def apply_incremental_load(conn, records, snapshot_ids, explicit_deletes=None):
    """
    Apply incremental changes using (order_id, line_number) as the
    composite business key.

    snapshot_ids contains the composite keys present in the current
    complete source snapshot.
    """

    explicit_deletes = set(explicit_deletes or [])

    changes = detect_changes(
        conn,
        "sales",
        records,
        ID_FIELDS,
    )

    now = datetime.now().isoformat(timespec="seconds")

    counts = {
        "inserted": 0,
        "updated": 0,
        "deleted": 0,
        "unchanged": len(changes["unchanged"]),
    }

    def is_explicitly_deleted(record):
        composite_id = (
            record["order_id"],
            record["line_number"],
        )

        return (
            composite_id in explicit_deletes
            or record["order_id"] in explicit_deletes
        )

    with conn:
        # 1. Insert new records.
        for record, digest in changes["insert"]:
            record_id = build_record_id(record, ID_FIELDS)

            if record["is_deleted"] or is_explicitly_deleted(record):
                save_source_state(
                    conn, "sales", record_id, digest, 1, now
                )
                continue

            _upsert(conn, record, now)

            save_source_state(
                conn, "sales", record_id, digest, 0, now
            )

            counts["inserted"] += 1

        # 2. Update existing records or process tombstones.
        for record, digest in changes["update"]:
            record_id = build_record_id(record, ID_FIELDS)

            if record["is_deleted"] or is_explicitly_deleted(record):
                _mark_deleted(conn, record, now)

                save_source_state(
                    conn, "sales", record_id, digest, 1, now
                )

                counts["deleted"] += 1

            else:
                _upsert(conn, record, now)

                save_source_state(
                    conn, "sales", record_id, digest, 0, now
                )

                counts["updated"] += 1

        # 3. Preserve unchanged records.
        for record, digest in changes["unchanged"]:
            record_id = build_record_id(record, ID_FIELDS)

            if record["is_deleted"] or is_explicitly_deleted(record):
                _mark_deleted(conn, record, now)

                save_source_state(
                    conn, "sales", record_id, digest, 1, now
                )

            else:
                save_source_state(
                    conn, "sales", record_id, digest, 0, now
                )

        # 4. Detect records missing from the complete source snapshot.
        # CDC returns their composite identifiers as JSON strings.
        for record_id in changes["delete"]:
            order_id, line_number = json.loads(record_id)

            conn.execute(
                """
                UPDATE transformed_sales
                SET is_deleted=1, loaded_at=?
                WHERE order_id=? AND line_number=?
                """,
                (now, order_id, line_number),
            )

            old = conn.execute(
                """
                SELECT row_hash
                FROM source_state
                WHERE entity_type='sales' AND record_id=?
                """,
                (record_id,),
            ).fetchone()

            if old:
                save_source_state(
                    conn,
                    "sales",
                    record_id,
                    old["row_hash"],
                    1,
                    now,
                )

            counts["deleted"] += 1

        # 5. Process explicit delete instructions.
        for record in records:
            if is_explicitly_deleted(record) and not record["is_deleted"]:
                _mark_deleted(conn, record, now)

                record_id = build_record_id(record, ID_FIELDS)

                save_source_state(
                    conn,
                    "sales",
                    record_id,
                    record_hash(record),
                    1,
                    now,
                )

    return counts

def _mark_deleted(conn, record, now):
    """Soft-delete exactly one sales line."""

    conn.execute(
        """
        UPDATE transformed_sales
        SET is_deleted=1, loaded_at=?
        WHERE order_id=? AND line_number=?
        """,
        (
            now,
            record["order_id"],
            record["line_number"],
        ),
    )

def _upsert(conn, record, now):
    """Insert or update one sales line using its composite primary key."""

    conn.execute(
        """
        INSERT INTO transformed_sales (
            order_id,
            line_number,
            customer_id,
            customer_name,
            city,
            product_id,
            product_name,
            category,
            order_date,
            quantity,
            unit_price,
            revenue,
            source_updated_at,
            is_deleted,
            loaded_at
        )
        VALUES (
            :order_id,
            :line_number,
            :customer_id,
            :customer_name,
            :city,
            :product_id,
            :product_name,
            :category,
            :order_date,
            :quantity,
            :unit_price,
            :revenue,
            :source_updated_at,
            0,
            :loaded_at
        )
        ON CONFLICT(order_id, line_number)
        DO UPDATE SET
            customer_id=excluded.customer_id,
            customer_name=excluded.customer_name,
            city=excluded.city,
            product_id=excluded.product_id,
            product_name=excluded.product_name,
            category=excluded.category,
            order_date=excluded.order_date,
            quantity=excluded.quantity,
            unit_price=excluded.unit_price,
            revenue=excluded.revenue,
            source_updated_at=excluded.source_updated_at,
            is_deleted=0,
            loaded_at=excluded.loaded_at
        """,
        {
            **record,
            "loaded_at": now,
        },
    )