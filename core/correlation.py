from collections import defaultdict


def group_entities(entities):
    groups = defaultdict(list)

    for entity in entities:
        key = (entity["type"], entity["value"])
        groups[key].append(entity)

    return groups


def create_links(entities):
    links = []
    seen = set()

    groups = group_entities(entities)

    for (entity_type, value), occurrences in groups.items():

        # Which independent sources contain this entity?
        source_map = defaultdict(list)

        for occurrence in occurrences:
            source_map[occurrence["source"]].append(occurrence)

        sources = sorted(source_map.keys())

        if len(sources) < 2:
            continue

        # Create only ONE link between each pair of sources
        for i in range(len(sources)):
            for j in range(i + 1, len(sources)):

                source_a = sources[i]
                source_b = sources[j]

                unique_key = (
                    entity_type,
                    value,
                    source_a,
                    source_b
                )

                if unique_key in seen:
                    continue

                seen.add(unique_key)

                if entity_type == "IMEI":
                    confidence = 1.00
                    reason = "Same IMEI across independent evidence sources"

                elif entity_type == "IMSI":
                    confidence = 0.95
                    reason = "Same IMSI across independent evidence sources"

                elif entity_type == "IP":
                    confidence = 0.80
                    reason = "Same IP observed across independent evidence sources"

                elif entity_type == "UPI":
                    confidence = 0.90
                    reason = "Same UPI identifier observed across evidence"

                elif entity_type == "PHONE":
                    confidence = 0.90
                    reason = "Same phone number observed across evidence"

                else:
                    confidence = 0.75
                    reason = f"Same {entity_type} observed across evidence"

                links.append({
                    "entity_type": entity_type,
                    "value": value,
                    "source_a": source_a,
                    "source_b": source_b,
                    "confidence": confidence,
                    "reason": reason
                })

    return links