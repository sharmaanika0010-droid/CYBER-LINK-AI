import pandas as pd


def normalize_cdr(data):
    records = []

    for _, row in data.iterrows():
        records.append({
            "event_type": "CALL",
            "timestamp": str(row["timestamp"]),
            "source": "CDR",
            "caller": str(row["caller"]),
            "callee": str(row["callee"]),
            "imei": str(row["imei"]),
            "imsi": str(row["imsi"]),
            "cell_id": str(row["cell_id"]),
            "duration_seconds": int(row["duration_seconds"])
        })

    return records


def normalize_transactions(data):
    records = []

    for _, row in data.iterrows():
        records.append({
            "event_type": "TRANSACTION",
            "timestamp": str(row["timestamp"]),
            "source": "BANK",
            "transaction_id": str(row["transaction_id"]),
            "sender_account": str(row["sender_account"]),
            "receiver_account": str(row["receiver_account"]),
            "sender_upi": str(row["sender_upi"]),
            "receiver_upi": str(row["receiver_upi"]),
            "amount": float(row["amount"])
        })

    return records


def normalize_ipdr(data):
    records = []

    for _, row in data.iterrows():
        records.append({
            "event_type": "NETWORK",
            "timestamp": str(row["timestamp"]),
            "source": "IPDR",
            "phone": str(row["phone"]),
            "ip": str(row["ip"]),
            "port": int(row["port"]),
            "imei": str(row["imei"])
        })

    return records


def normalize_android(data):
    device = data.get("device", {})
    network = data.get("network", {})

    return [{
        "event_type": "DEVICE",
        "timestamp": None,
        "source": "ANDROID",
        "imei": str(device.get("imei", "")),
        "imsi": str(device.get("imsi", "")),
        "mac": str(device.get("mac", "")),
        "ip": str(network.get("last_ip", ""))
    }]


def normalize_email(data):
    return [{
        "event_type": "EMAIL",
        "timestamp": data.get("Date", ""),
        "source": "EMAIL",
        "from": data.get("From", ""),
        "to": data.get("To", ""),
        "subject": data.get("Subject", ""),
        "message_id": data.get("Message-ID", ""),
        "received": data.get("Received", "")
    }]


def normalize_evidence(evidence):
    """
    Convert an ingested evidence file into the common event structure.
    """

    source_file = evidence["file"]
    data = evidence["data"]

    if source_file.lower() == "cdr.csv":
        return normalize_cdr(data)

    if source_file.lower() == "transactions.csv":
        return normalize_transactions(data)

    if source_file.lower() == "ipdr.csv":
        return normalize_ipdr(data)

    if source_file.lower() == "android_log.json":
        return normalize_android(data)

    if source_file.lower() == "suspicious.eml":
        return normalize_email(data)

    return []