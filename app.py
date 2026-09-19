from pathlib import Path

from core.ingestion import ingest_evidence_folder
from core.hashing import hash_evidence_folder
from core.normalization import normalize_evidence
from core.entity_extraction import extract_entities
from core.correlation import create_links
from core.risk_engine import calculate_risk
from core.graph_engine import build_fraud_graph, graph_summary


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# ------------------------------------------------------------
# DEMO DATASET
# ------------------------------------------------------------
# Ready-made synthetic evidence for hackathon demonstration.

DATA_DIR = BASE_DIR / "data"


# ------------------------------------------------------------
# UPLOAD DIRECTORY
# ------------------------------------------------------------
# Uploaded investigation evidence will be stored here later.

UPLOADS_DIR = BASE_DIR / "uploads"


# ------------------------------------------------------------
# OUTPUT / REPORT DIRECTORIES
# ------------------------------------------------------------

OUTPUT_DIR = BASE_DIR / "output"

REPORTS_DIR = BASE_DIR / "reports"


# Create folders automatically if they do not exist

DATA_DIR.mkdir(exist_ok=True)

UPLOADS_DIR.mkdir(exist_ok=True)

OUTPUT_DIR.mkdir(exist_ok=True)

REPORTS_DIR.mkdir(exist_ok=True)


# ============================================================
# BUILD EVIDENCE PIPELINE
# ============================================================

def build_pipeline(evidence_dir=None):
    """
    Build the complete evidence processing pipeline.

    If evidence_dir is not provided:
        Use the default synthetic demo dataset.

    If evidence_dir is provided:
        Process the uploaded investigation evidence
        from that directory.

    Pipeline:

        Evidence Ingestion
              ↓
        Data Normalization
              ↓
        Entity Extraction
              ↓
        Cross-Source Correlation
    """

    # --------------------------------------------------------
    # SELECT EVIDENCE SOURCE
    # --------------------------------------------------------

    if evidence_dir is None:

        evidence_dir = DATA_DIR

    else:

        evidence_dir = Path(evidence_dir)

    # --------------------------------------------------------
    # STEP 1: EVIDENCE INGESTION
    # --------------------------------------------------------

    evidence = ingest_evidence_folder(
        evidence_dir
    )

    # --------------------------------------------------------
    # STEP 2: NORMALIZATION
    # --------------------------------------------------------

    all_records = []

    for item in evidence:

        if item["status"] != "SUCCESS":
            continue

        try:

            normalized_records = normalize_evidence(
                item
            )

            all_records.extend(
                normalized_records
            )

        except Exception:

            # Ignore unsupported/unrecognized
            # evidence during normalization.

            continue

    # --------------------------------------------------------
    # STEP 3: ENTITY EXTRACTION
    # --------------------------------------------------------

    entities = extract_entities(
        all_records
    )

    # --------------------------------------------------------
    # STEP 4: CROSS-SOURCE CORRELATION
    # --------------------------------------------------------

    links = create_links(
        entities
    )

    # --------------------------------------------------------
    # RETURN PIPELINE RESULTS
    # --------------------------------------------------------

    return {

        "evidence":
            evidence,

        "records":
            all_records,

        "entities":
            entities,

        "links":
            links
    }


# ============================================================
# RUN COMPLETE INTELLIGENCE ANALYSIS
# ============================================================

def run_intelligence(evidence_dir=None):
    """
    Run the complete CYBER-LINK AI intelligence pipeline.

    Parameters:
        evidence_dir:
            Optional folder containing investigation evidence.

            If None:
                Default synthetic demo dataset is used.

    Returns:
        Complete intelligence analysis result.
    """

    # --------------------------------------------------------
    # BUILD PIPELINE
    # --------------------------------------------------------

    pipeline = build_pipeline(
        evidence_dir
    )

    evidence = pipeline[
        "evidence"
    ]

    records = pipeline[
        "records"
    ]

    entities = pipeline[
        "entities"
    ]

    links = pipeline[
        "links"
    ]

    # --------------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------------

    risk_results = calculate_risk(

        entities,

        links,

        records
    )

    # --------------------------------------------------------
    # GRAPH CONSTRUCTION
    # --------------------------------------------------------

    fraud_graph = build_fraud_graph(

        records,

        entities,

        links
    )

    graph_info = graph_summary(

        fraud_graph
    )

    # --------------------------------------------------------
    # EVIDENCE INTEGRITY
    # --------------------------------------------------------

    evidence_hashes = hash_evidence_folder(
    evidence_dir if evidence_dir is not None else DATA_DIR
)

    # --------------------------------------------------------
    # RETURN EVERYTHING
    # --------------------------------------------------------

    return {

        "evidence":
            evidence,

        "records":
            records,

        "entities":
            entities,

        "links":
            links,

        "risk_results":
            risk_results,

        "graph":
            fraud_graph,

        "graph_info":
            graph_info,

        "evidence_hashes":
            evidence_hashes,

        "evidence_directory":
            str(evidence_dir)
    }


# ============================================================
# COMMAND LINE DEMO
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # DEFAULT DEMO MODE
    # --------------------------------------------------------
    # When app.py is run directly, the synthetic dataset
    # inside data/ is automatically used.

    result = run_intelligence()


    records = result[
        "records"
    ]

    entities = result[
        "entities"
    ]

    links = result[
        "links"
    ]

    risk_results = result[
        "risk_results"
    ]

    graph = result[
        "graph"
    ]

    graph_info = result[
        "graph_info"
    ]

    evidence_hashes = result[
        "evidence_hashes"
    ]


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "                 CYBER-LINK AI"
    )

    print(
        "          Evidence-to-Network Intelligence"
    )

    print(
        "=" * 60
    )


    # --------------------------------------------------------
    # PIPELINE SUMMARY
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "                  PIPELINE SUMMARY"
    )

    print(
        "=" * 60
    )


    print(
        f"Evidence Directory : "
        f"{result['evidence_directory']}"
    )

    print(
        f"Normalized Records : "
        f"{len(records)}"
    )

    print(
        f"Extracted Entities : "
        f"{len(entities)}"
    )

    print(
        f"Correlation Links  : "
        f"{len(links)}"
    )

    print(
        f"Risk Signals       : "
        f"{len(risk_results)}"
    )

    print(
        f"Graph Nodes        : "
        f"{graph_info['nodes']}"
    )

    print(
        f"Graph Links        : "
        f"{graph_info['links']}"
    )

    print(
        f"Evidence Files     : "
        f"{len(evidence_hashes)}"
    )


    # --------------------------------------------------------
    # EVIDENCE INTEGRITY
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "                EVIDENCE INTEGRITY"
    )

    print(
        "=" * 60
    )


    for item in evidence_hashes:

        print()

        print(
            f"File      : "
            f"{item['file']}"
        )

        print(
            f"Size      : "
            f"{item.get('size_bytes', 0)} bytes"
        )

        print(
            f"SHA-256   : "
            f"{item['sha256']}"
        )


    # --------------------------------------------------------
    # CROSS-SOURCE CORRELATIONS
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "             CROSS-SOURCE CORRELATIONS"
    )

    print(
        "=" * 60
    )


    if not links:

        print()

        print(
            "No cross-source correlations detected."
        )

    else:

        for link in links:

            print()

            print(
                f"{link['entity_type']} : "
                f"{link['value']}"
            )

            print(
                f"Sources    : "
                f"{link['source_a']} <-> "
                f"{link['source_b']}"
            )

            print(
                f"Confidence : "
                f"{link['confidence']:.2f}"
            )

            print(
                f"Reason     : "
                f"{link['reason']}"
            )


    # --------------------------------------------------------
    # RISK INTELLIGENCE
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "                 RISK INTELLIGENCE"
    )

    print(
        "=" * 60
    )


    if not risk_results:

        print()

        print(
            "No risk signals detected."
        )

    else:

        for item in risk_results:

            print()

            print(
                item["entity"]
            )

            print(
                f"Risk Score : "
                f"{item['score']}"
            )

            print(
                f"Risk Level : "
                f"{item['level']}"
            )

            print(
                "Indicators:"
            )

            for reason in item["reasons"]:

                print(
                    f"  - {reason}"
                )


    # --------------------------------------------------------
    # TRANSACTION NETWORK
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "                TRANSACTION NETWORK"
    )

    print(
        "=" * 60
    )


    transaction_count = 0


    for source, target, data in graph.edges(
        data=True
    ):

        if data.get(
            "relationship"
        ) != "TRANSACTION":

            continue


        transaction_count += 1


        print()

        print(
            f"{source} -> {target}"
        )

        print(
            f"Amount      : "
            f"₹{data.get('amount', 0):,.2f}"
        )

        print(
            f"Transaction : "
            f"{data.get('transaction_id', 'N/A')}"
        )

        print(
            f"Timestamp   : "
            f"{data.get('timestamp', 'N/A')}"
        )


    if transaction_count == 0:

        print()

        print(
            "No transaction relationships detected."
        )


    # --------------------------------------------------------
    # FINAL NOTE
    # --------------------------------------------------------

    print()

    print(
        "=" * 60
    )

    print(
        "                 ANALYSIS COMPLETE"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Investigator Note:"
    )

    print(
        "Detected correlations and risk indicators "
        "are intelligence leads."
    )

    print(
        "They require independent investigator "
        "verification and are not conclusions of guilt."
    )

    print()