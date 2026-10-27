def refund_stats(conn):
    count, total = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(amount_cents), 0) FROM refunds"
    ).fetchone()
    return {"refund_count": count, "refunded_cents": total}
