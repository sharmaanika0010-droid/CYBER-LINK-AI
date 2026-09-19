import networkx as nx


def build_fraud_graph(records, entities, links):

    graph = nx.DiGraph()

    # ---------------------------------------------
    # 1. TRANSACTION RELATIONSHIPS
    # ---------------------------------------------

    for record in records:

        if record.get("event_type") != "TRANSACTION":
            continue

        sender = record.get("sender_account")
        receiver = record.get("receiver_account")

        if not sender or not receiver:
            continue

        graph.add_node(
            sender,
            node_type="ACCOUNT"
        )

        graph.add_node(
            receiver,
            node_type="ACCOUNT"
        )

        graph.add_edge(
            sender,
            receiver,
            relationship="TRANSACTION",
            amount=record.get("amount", 0),
            timestamp=record.get("timestamp"),
            transaction_id=record.get("transaction_id")
        )

    # ---------------------------------------------
    # 2. ENTITY NODES
    # ---------------------------------------------

    for entity in entities:

        node_id = f"{entity['type']}:{entity['value']}"

        graph.add_node(
            node_id,
            node_type=entity["type"],
            value=entity["value"]
        )

    # ---------------------------------------------
    # 3. CORRELATION RELATIONSHIPS
    # ---------------------------------------------

    for link in links:

        entity_node = (
            f"{link['entity_type']}:{link['value']}"
        )

        source_a_node = f"SOURCE:{link['source_a']}"
        source_b_node = f"SOURCE:{link['source_b']}"

        graph.add_node(
            source_a_node,
            node_type="SOURCE",
            value=link["source_a"]
        )

        graph.add_node(
            source_b_node,
            node_type="SOURCE",
            value=link["source_b"]
        )

        graph.add_edge(
            entity_node,
            source_a_node,
            relationship="EVIDENCE",
            confidence=link["confidence"]
        )

        graph.add_edge(
            entity_node,
            source_b_node,
            relationship="EVIDENCE",
            confidence=link["confidence"]
        )

    # ---------------------------------------------
    # 4. PHONE → IMEI RELATIONSHIPS
    # ---------------------------------------------

    phone_imei = {}

    for record in records:

        if record.get("event_type") == "CALL":

            phone_imei.setdefault(
                record["caller"],
                set()
            ).add(record["imei"])

            phone_imei.setdefault(
                record["callee"],
                set()
            ).add(record["imei"])

        elif record.get("event_type") == "NETWORK":

            phone_imei.setdefault(
                record["phone"],
                set()
            ).add(record["imei"])

    for phone, imeis in phone_imei.items():

        phone_node = f"PHONE:{phone}"

        graph.add_node(
            phone_node,
            node_type="PHONE",
            value=phone
        )

        for imei in imeis:

            imei_node = f"IMEI:{imei}"

            graph.add_edge(
                phone_node,
                imei_node,
                relationship="USES_DEVICE"
            )

    # ---------------------------------------------
    # 5. IMEI → IP RELATIONSHIPS
    # ---------------------------------------------

    imei_ip = {}

    for record in records:

        if record.get("event_type") == "NETWORK":

            imei_ip.setdefault(
                record["imei"],
                set()
            ).add(record["ip"])

        elif record.get("event_type") == "DEVICE":

            imei_ip.setdefault(
                record["imei"],
                set()
            ).add(record["ip"])

    for imei, ips in imei_ip.items():

        imei_node = f"IMEI:{imei}"

        for ip in ips:

            ip_node = f"IP:{ip}"

            graph.add_edge(
                imei_node,
                ip_node,
                relationship="USES_IP"
            )

    # ---------------------------------------------
    # 6. RETURN GRAPH
    # ---------------------------------------------

    return graph


def graph_summary(graph):

    transaction_edges = 0
    evidence_edges = 0
    device_edges = 0

    for _, _, data in graph.edges(data=True):

        relationship = data.get("relationship")

        if relationship == "TRANSACTION":
            transaction_edges += 1

        elif relationship == "EVIDENCE":
            evidence_edges += 1

        elif relationship in {
            "USES_DEVICE",
            "USES_IP"
        }:
            device_edges += 1

    return {
        "nodes": graph.number_of_nodes(),
        "links": graph.number_of_edges(),
        "transaction_links": transaction_edges,
        "evidence_links": evidence_edges,
        "device_links": device_edges
    }