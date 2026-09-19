def add_entity(entities, entity_type, value, source, timestamp=None):
    if value is None:
        return

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none"}:
        return

    entities.append({
        "type": entity_type,
        "value": value,
        "source": source,
        "timestamp": timestamp
    })


def extract_entities(records):
    entities = []

    for record in records:

        source = record.get("source")
        timestamp = record.get("timestamp")

        # CDR
        if record.get("event_type") == "CALL":
            add_entity(entities, "PHONE", record.get("caller"), source, timestamp)
            add_entity(entities, "PHONE", record.get("callee"), source, timestamp)
            add_entity(entities, "IMEI", record.get("imei"), source, timestamp)
            add_entity(entities, "IMSI", record.get("imsi"), source, timestamp)

        # Bank transactions
        elif record.get("event_type") == "TRANSACTION":
            add_entity(
                entities,
                "ACCOUNT",
                record.get("sender_account"),
                source,
                timestamp
            )

            add_entity(
                entities,
                "ACCOUNT",
                record.get("receiver_account"),
                source,
                timestamp
            )

            add_entity(
                entities,
                "UPI",
                record.get("sender_upi"),
                source,
                timestamp
            )

            add_entity(
                entities,
                "UPI",
                record.get("receiver_upi"),
                source,
                timestamp
            )

        # IPDR
        elif record.get("event_type") == "NETWORK":
            add_entity(entities, "PHONE", record.get("phone"), source, timestamp)
            add_entity(entities, "IP", record.get("ip"), source, timestamp)
            add_entity(entities, "IMEI", record.get("imei"), source, timestamp)

        # Android
        elif record.get("event_type") == "DEVICE":
            add_entity(entities, "IMEI", record.get("imei"), source)
            add_entity(entities, "IMSI", record.get("imsi"), source)
            add_entity(entities, "MAC", record.get("mac"), source)
            add_entity(entities, "IP", record.get("ip"), source)

        # Email
        elif record.get("event_type") == "EMAIL":
            add_entity(entities, "EMAIL", record.get("from"), source, timestamp)
            add_entity(entities, "EMAIL", record.get("to"), source, timestamp)

            received = record.get("received", "")

            if "(" in received and ")" in received:
                ip = received.split("(")[-1].split(")")[0]
                add_entity(entities, "IP", ip, source, timestamp)

    return entities