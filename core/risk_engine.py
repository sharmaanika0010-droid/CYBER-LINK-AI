def calculate_risk(entities, links, records):

    scores = {}

    reasons = {}

    def add_score(entity, points, reason):

        if entity not in scores:
            scores[entity] = 0
            reasons[entity] = []

        scores[entity] += points

        if reason not in reasons[entity]:
            reasons[entity].append(reason)

    # Correlation-based signals
    for link in links:

        entity = f"{link['entity_type']}:{link['value']}"

        if link["entity_type"] == "IMEI":
            add_score(
                entity,
                20,
                "Device identifier appears across multiple evidence sources"
            )

        elif link["entity_type"] == "IMSI":
            add_score(
                entity,
                15,
                "Subscriber identifier appears across evidence sources"
            )

        elif link["entity_type"] == "IP":
            add_score(
                entity,
                15,
                "IP address is correlated across independent evidence sources"
            )

        elif link["entity_type"] == "UPI":
            add_score(
                entity,
                10,
                "UPI identifier appears in multiple financial records"
            )

    # Rapid fund movement
    transactions = [
        r for r in records
        if r.get("event_type") == "TRANSACTION"
    ]

    transactions.sort(key=lambda x: str(x.get("timestamp")))

    for i in range(len(transactions) - 1):

        current = transactions[i]
        next_tx = transactions[i + 1]

        if current["receiver_account"] == next_tx["sender_account"]:

            entity = f"ACCOUNT:{current['receiver_account']}"

            add_score(
                entity,
                25,
                "Rapid multi-hop fund movement detected"
            )

    # Multiple incoming victims
    incoming = {}

    for tx in transactions:
        account = tx["receiver_account"]

        if account not in incoming:
            incoming[account] = set()

        incoming[account].add(tx["sender_account"])

    for account, senders in incoming.items():

        if len(senders) >= 2:

            entity = f"ACCOUNT:{account}"

            add_score(
                entity,
                20,
                "Multiple sender accounts transfer funds to the same account"
            )

    # Cap score at 100
    for entity in scores:
        scores[entity] = min(scores[entity], 100)

    results = []

    for entity, score in sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        if score >= 80:
            level = "CRITICAL"
        elif score >= 60:
            level = "HIGH"
        elif score >= 30:
            level = "MEDIUM"
        else:
            level = "LOW"

        results.append({
            "entity": entity,
            "score": score,
            "level": level,
            "reasons": reasons[entity]
        })

    return results