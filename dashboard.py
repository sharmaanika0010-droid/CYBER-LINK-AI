import json
import re
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd

from pyvis.network import Network

from app import run_intelligence


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = BASE_DIR / "reports"

DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CYBER-LINK AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #666;
        margin-bottom: 20px;
    }

    .section-note {
        color: #666;
        font-size: 14px;
    }

    .lead-box {
        padding: 14px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }

    .small-note {
        font-size: 12px;
        color: #666;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ CYBER-LINK AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Evidence-to-Network Intelligence | '
    'AI-assisted Cyber Fraud Triage & Digital Artifact Correlation'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🔎 Investigation Console")

    st.write(
        "Upload, correlate and triage "
        "digital forensic evidence."
    )

    st.divider()

    st.subheader("Investigation Pipeline")

    st.write("📥 Evidence Ingestion")
    st.write("🧪 Evidence Validation")
    st.write("🔐 SHA-256 Integrity")
    st.write("🔄 Data Normalization")
    st.write("🧩 Entity Extraction")
    st.write("🔗 Cross-Source Correlation")
    st.write("⚡ Golden-Hour Triage")
    st.write("🚨 Risk Intelligence")
    st.write("🕸️ Network Analysis")
    st.write("🕒 Attack Timeline")
    st.write("🕵️ Investigation Leads")
    st.write("📄 Case Reporting")

    st.divider()

    st.caption(
        "Synthetic data is used for demonstration. "
        "All detected relationships are investigative "
        "leads requiring verification."
    )


# ============================================================
# CASE CREATION
# ============================================================

st.header("🗂️ Investigation Case")

st.caption(
    "Create a case and upload multiple digital evidence artifacts."
)


case_id = st.text_input(
    "Case ID",
    value="CASE-2026-001",
    help="Unique identifier for the investigation."
)


# ============================================================
# EVIDENCE UPLOAD
# ============================================================

st.subheader("📤 Upload Evidence")

st.write(
    "Supported formats: CSV, XLSX, JSON, EML, TXT and LOG"
)

uploaded_files = st.file_uploader(
    "Select one or more evidence files",
    type=[
        "csv",
        "xlsx",
        "json",
        "eml",
        "txt",
        "log"
    ],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(
        f"✅ {len(uploaded_files)} evidence file(s) selected."
    )

    upload_preview = pd.DataFrame(
        [
            {
                "File": file.name,
                "Size": f"{file.size / 1024:.1f} KB",
                "Type": file.type or "Unknown"
            }
            for file in uploaded_files
        ]
    )

    st.dataframe(
        upload_preview,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DEMO MODE
# ============================================================

use_demo = st.checkbox(
    "Use synthetic demo dataset instead",
    value=not bool(uploaded_files)
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_clicked = st.button(
    "🚀 Analyze Evidence",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_clicked:

    # --------------------------------------------------------
    # UPLOAD MODE
    # --------------------------------------------------------

    if uploaded_files and not use_demo:

        if not case_id.strip():

            st.error(
                "Please enter a Case ID."
            )

            st.stop()


        safe_case_id = re.sub(
            r"[^A-Za-z0-9_-]",
            "_",
            case_id.strip()
        )


        if not safe_case_id:

            st.error(
                "Invalid Case ID."
            )

            st.stop()


        case_dir = (
            UPLOADS_DIR
            / safe_case_id
        )

        case_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        saved_files = []


        with st.status(
            "🔄 Processing investigation evidence...",
            expanded=True
        ) as status:

            st.write(
                f"🗂️ Case: {safe_case_id}"
            )

            for uploaded_file in uploaded_files:

                clean_name = Path(
                    uploaded_file.name
                ).name

                file_path = (
                    case_dir
                    / clean_name
                )

                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                saved_files.append(
                    clean_name
                )

                st.write(
                    f"📥 Stored: {clean_name}"
                )


            st.write(
                "🧪 Validating evidence formats..."
            )

            st.write(
                "🔐 Calculating SHA-256 fingerprints..."
            )

            st.write(
                "🔄 Normalizing evidence..."
            )

            st.write(
                "🧩 Extracting entities..."
            )

            st.write(
                "🔗 Correlating artifacts..."
            )

            st.write(
                "🚨 Calculating risk indicators..."
            )

            st.write(
                "🕸️ Building investigation network..."
            )


            try:

                result = run_intelligence(
                    case_dir
                )

                status.update(
                    label="✅ Evidence analysis completed",
                    state="complete"
                )

                st.session_state[
                    "analysis_result"
                ] = result

                st.session_state[
                    "analysis_source"
                ] = safe_case_id

                st.session_state[
                    "analysis_mode"
                ] = "UPLOADED"

            except Exception as error:

                status.update(
                    label="❌ Analysis failed",
                    state="error"
                )

                st.error(
                    "Pipeline execution failed."
                )

                st.exception(
                    error
                )

                st.stop()


    # --------------------------------------------------------
    # DEMO MODE
    # --------------------------------------------------------

    else:

        with st.status(
            "🔄 Running synthetic demonstration...",
            expanded=True
        ) as status:

            st.write(
                "📂 Loading synthetic evidence..."
            )

            st.write(
                "🧪 Validating evidence..."
            )

            st.write(
                "🔐 Calculating SHA-256 fingerprints..."
            )

            st.write(
                "🔄 Normalizing evidence..."
            )

            st.write(
                "🧩 Extracting entities..."
            )

            st.write(
                "🔗 Correlating artifacts..."
            )

            st.write(
                "🚨 Calculating risk indicators..."
            )

            st.write(
                "🕸️ Building investigation network..."
            )

            try:

                result = run_intelligence()

                status.update(
                    label="✅ Demo analysis completed",
                    state="complete"
                )

                st.session_state[
                    "analysis_result"
                ] = result

                st.session_state[
                    "analysis_source"
                ] = "DEMO-DATASET"

                st.session_state[
                    "analysis_mode"
                ] = "DEMO"

            except Exception as error:

                status.update(
                    label="❌ Demo analysis failed",
                    state="error"
                )

                st.error(
                    "Pipeline execution failed."
                )

                st.exception(
                    error
                )

                st.stop()


# ============================================================
# WAIT FOR ANALYSIS
# ============================================================

if "analysis_result" not in st.session_state:

    st.info(
        "👆 Select evidence or use the synthetic demo dataset, "
        "then click **Analyze Evidence**."
    )

    st.stop()


# ============================================================
# LOAD RESULTS
# ============================================================

result = st.session_state[
    "analysis_result"
]

analysis_source = st.session_state.get(
    "analysis_source",
    "DEMO-DATASET"
)

analysis_mode = st.session_state.get(
    "analysis_mode",
    "DEMO"
)


evidence = result.get(
    "evidence",
    []
)

records = result.get(
    "records",
    []
)

entities = result.get(
    "entities",
    []
)

links = result.get(
    "links",
    []
)

risk_results = result.get(
    "risk_results",
    []
)

fraud_graph = result.get(
    "graph"
)

graph_info = result.get(
    "graph_info",
    {}
)

evidence_hashes = result.get(
    "evidence_hashes",
    []
)


# ============================================================
# ACTIVE CASE
# ============================================================

st.divider()

st.header("📌 Active Investigation")

case_col1, case_col2, case_col3, case_col4 = st.columns(4)

with case_col1:

    st.metric(
        "Case ID",
        analysis_source
    )

with case_col2:

    st.metric(
        "Evidence Files",
        len(evidence)
    )

with case_col3:

    st.metric(
        "Evidence Records",
        len(records)
    )

with case_col4:

    st.metric(
        "Analysis Mode",
        "LIVE EVIDENCE"
        if analysis_mode == "UPLOADED"
        else "DEMO"
    )


# ============================================================
# INVESTIGATION OVERVIEW
# ============================================================

st.header("📊 Investigation Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:

    st.metric(
        "Records",
        len(records)
    )

with col2:

    st.metric(
        "Entities",
        len(entities)
    )

with col3:

    st.metric(
        "Correlations",
        len(links)
    )

with col4:

    st.metric(
        "Risk Signals",
        len(risk_results)
    )

with col5:

    st.metric(
        "Graph Nodes",
        graph_info.get(
            "nodes",
            0
        )
    )

with col6:

    st.metric(
        "Graph Links",
        graph_info.get(
            "links",
            0
        )
    )


st.divider()


# ============================================================
# EVIDENCE INGESTION
# ============================================================

st.header("📥 Evidence Ingestion")

st.caption(
    "Artifacts detected and processed by the forensic pipeline."
)


evidence_rows = []

for item in evidence:

    evidence_rows.append(
        {
            "Evidence File": item.get(
                "file",
                "Unknown"
            ),

            "Format": item.get(
                "format",
                "Unknown"
            ),

            "Status": item.get(
                "status",
                "UNKNOWN"
            )
        }
    )


if evidence_rows:

    evidence_df = pd.DataFrame(
        evidence_rows
    )

    st.dataframe(
        evidence_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No evidence files detected."
    )


st.divider()


# ============================================================
# EVIDENCE VALIDATION
# ============================================================

st.header("🧪 Evidence Validation")

validation_rows = []

for item in evidence:

    status = item.get(
        "status",
        "UNKNOWN"
    )

    validation_rows.append(
        {
            "File": item.get(
                "file",
                "Unknown"
            ),

            "Format": item.get(
                "format",
                "Unknown"
            ),

            "Validation": (
                "PASS"
                if status == "SUCCESS"
                else "REVIEW"
            )
        }
    )


if validation_rows:

    validation_df = pd.DataFrame(
        validation_rows
    )

    st.dataframe(
        validation_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# GOLDEN HOUR TRIAGE
# ============================================================

st.header("⚡ Golden-Hour Triage")

st.caption(
    "Rapid indicators intended to help investigators "
    "prioritize evidence for verification."
)


high_count = sum(
    1
    for item in risk_results
    if item.get("level") in {
        "HIGH",
        "CRITICAL"
    }
)

medium_count = sum(
    1
    for item in risk_results
    if item.get("level") == "MEDIUM"
)

low_count = sum(
    1
    for item in risk_results
    if item.get("level") == "LOW"
)


triage_col1, triage_col2, triage_col3 = st.columns(3)


with triage_col1:

    st.metric(
        "🔴 High / Critical",
        high_count
    )


with triage_col2:

    st.metric(
        "🟠 Medium",
        medium_count
    )


with triage_col3:

    st.metric(
        "🟢 Low",
        low_count
    )


st.info(
    "Triage signals are investigative leads and "
    "require independent verification."
)


st.divider()


# ============================================================
# RISK INTELLIGENCE
# ============================================================

st.header("🚨 Risk Intelligence")

st.caption(
    "Explainable risk indicators generated from "
    "cross-source and transaction patterns."
)


risk_rows = []


for item in risk_results:

    risk_rows.append(
        {
            "Entity": item.get(
                "entity",
                ""
            ),

            "Risk Score": item.get(
                "score",
                0
            ),

            "Risk Level": item.get(
                "level",
                "UNKNOWN"
            ),

            "Why Flagged": " | ".join(
                item.get(
                    "reasons",
                    []
                )
            )
        }
    )


if risk_rows:

    risk_df = pd.DataFrame(
        risk_rows
    )

    st.dataframe(
        risk_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No risk indicators detected."
    )


# ============================================================
# EXPLAINABLE INVESTIGATION PANEL
# ============================================================

st.subheader("🧠 Why is this suspicious?")

if risk_results:

    selected_entities = [
        item.get(
            "entity",
            ""
        )
        for item in risk_results
    ]

    selected_entity = st.selectbox(
        "Select an indicator",
        selected_entities
    )

    selected_item = next(
        (
            item
            for item in risk_results
            if item.get("entity")
            == selected_entity
        ),
        None
    )

    if selected_item:

        explain_col1, explain_col2 = st.columns(2)

        with explain_col1:

            st.metric(
                "Risk Score",
                selected_item.get(
                    "score",
                    0
                )
            )

        with explain_col2:

            st.metric(
                "Risk Level",
                selected_item.get(
                    "level",
                    "UNKNOWN"
                )
            )

        st.write(
            "**Observed indicators:**"
        )

        for reason in selected_item.get(
            "reasons",
            []
        ):

            st.write(
                f"• {reason}"
            )

        st.caption(
            "These indicators describe observed patterns "
            "in the supplied evidence. They are not conclusions "
            "of wrongdoing."
        )

else:

    st.info(
        "No explainable risk signals available."
    )


st.divider()


# ============================================================
# TRANSACTION NETWORK
# ============================================================

st.header("💰 Transaction Network")

st.caption(
    "Chronological movement of funds across investigation accounts."
)


transaction_rows = []


if fraud_graph is not None:

    for source, target, data in fraud_graph.edges(
        data=True
    ):

        if data.get(
            "relationship"
        ) != "TRANSACTION":

            continue

        transaction_rows.append(
            {
                "From": source,

                "To": target,

                "Amount": (
                    f"₹{data.get('amount', 0):,.0f}"
                ),

                "Transaction ID": data.get(
                    "transaction_id",
                    "N/A"
                ),

                "Timestamp": str(
                    data.get(
                        "timestamp",
                        ""
                    )
                )
            }
        )


if transaction_rows:

    transaction_df = pd.DataFrame(
        transaction_rows
    )

    transaction_df["Timestamp"] = pd.to_datetime(
        transaction_df["Timestamp"],
        errors="coerce"
    )

    transaction_df = transaction_df.sort_values(
        "Timestamp"
    )

    transaction_df["Timestamp"] = (
        transaction_df["Timestamp"]
        .dt.strftime(
            "%d-%b-%Y %H:%M:%S"
        )
    )

    st.dataframe(
        transaction_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No transaction relationships detected."
    )


# ============================================================
# TRANSACTION FLOW SUMMARY
# ============================================================

if transaction_rows:

    amounts = []

    for source, target, data in fraud_graph.edges(
        data=True
    ):

        if data.get(
            "relationship"
        ) == "TRANSACTION":

            amounts.append(
                float(
                    data.get(
                        "amount",
                        0
                    )
                )
            )

    total_value = sum(
        amounts
    )

    max_value = max(
        amounts
    ) if amounts else 0

    flow_col1, flow_col2, flow_col3 = st.columns(3)

    with flow_col1:

        st.metric(
            "Transactions",
            len(transaction_rows)
        )

    with flow_col2:

        st.metric(
            "Total Value",
            f"₹{total_value:,.0f}"
        )

    with flow_col3:

        st.metric(
            "Largest Transfer",
            f"₹{max_value:,.0f}"
        )


st.divider()


# ============================================================
# INTERACTIVE GRAPH
# ============================================================

st.header("🕸️ Investigator Relationship Graph")

st.caption(
    "Interactive network connecting financial, telecom, "
    "device, network and evidence-source artifacts."
)


if fraud_graph is not None and fraud_graph.number_of_nodes() > 0:

    net = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#222222"
    )

    net.barnes_hut(
        gravity=-2500,
        central_gravity=0.2,
        spring_length=180,
        spring_strength=0.04,
        damping=0.09
    )


    # --------------------------------------------------------
    # GRAPH NODES
    # --------------------------------------------------------

    for node, data in fraud_graph.nodes(
        data=True
    ):

        node_type = data.get(
            "node_type",
            "UNKNOWN"
        )

        value = str(
            data.get(
                "value",
                node
            )
        )

        label = value

        if len(label) > 25:

            label = (
                label[:22]
                + "..."
            )

        title = (
            f"<b>Type:</b> {node_type}<br>"
            f"<b>Value:</b> {value}"
        )

        node_size = 20

        if node_type == "ACCOUNT":

            node_size = 26

        elif node_type == "SOURCE":

            node_size = 14

        elif node_type == "IMEI":

            node_size = 22

        elif node_type == "IP":

            node_size = 22

        net.add_node(
            node,
            label=label,
            title=title,
            group=node_type,
            size=node_size
        )


    # --------------------------------------------------------
    # GRAPH EDGES
    # --------------------------------------------------------

    for source, target, data in fraud_graph.edges(
        data=True
    ):

        relationship = data.get(
            "relationship",
            "LINK"
        )


        if relationship == "TRANSACTION":

            amount = data.get(
                "amount",
                0
            )

            edge_label = (
                f"₹{amount:,.0f}"
            )

            edge_title = (
                f"<b>Transaction</b><br>"
                f"Amount: ₹{amount:,.0f}<br>"
                f"Transaction ID: "
                f"{data.get('transaction_id', 'N/A')}<br>"
                f"Time: "
                f"{data.get('timestamp', 'N/A')}"
            )

        else:

            edge_label = relationship

            confidence = data.get(
                "confidence"
            )

            if confidence is not None:

                edge_title = (
                    f"<b>Relationship:</b> "
                    f"{relationship}<br>"
                    f"<b>Confidence:</b> "
                    f"{confidence:.2f}"
                )

            else:

                edge_title = (
                    f"<b>Relationship:</b> "
                    f"{relationship}"
                )


        net.add_edge(
            source,
            target,
            label=edge_label,
            title=edge_title,
            arrows="to"
        )


    # --------------------------------------------------------
    # GRAPH OPTIONS
    # --------------------------------------------------------

    net.set_options(
        """
        {
          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true,
            "zoomView": true,
            "dragNodes": true,
            "dragView": true
          },

          "physics": {
            "enabled": true,
            "stabilization": {
              "enabled": true,
              "iterations": 150
            }
          },

          "nodes": {
            "shape": "dot",
            "font": {
              "size": 14,
              "face": "Arial"
            },
            "borderWidth": 1
          },

          "edges": {
            "smooth": true,
            "font": {
              "size": 10,
              "face": "Arial"
            },
            "arrows": {
              "to": {
                "enabled": true
              }
            },
            "width": 1
          }
        }
        """
    )


    graph_file = (
        OUTPUT_DIR
        / f"{analysis_source}_graph.html"
    )


    net.write_html(
        str(graph_file),
        open_browser=False
    )


    try:

        with open(
            graph_file,
            "r",
            encoding="utf-8"
        ) as file:

            graph_html = file.read()


        st.components.v1.html(
            graph_html,
            height=730,
            scrolling=True
        )

    except Exception as error:

        st.error(
            "Unable to display interactive graph."
        )

        st.exception(
            error
        )

else:

    st.info(
        "No graph relationships available."
    )


st.divider()


# ============================================================
# CROSS-SOURCE CORRELATION MATRIX
# ============================================================

st.header("🔗 Cross-Source Correlations")

st.caption(
    "Identifiers observed across independent evidence sources."
)


correlation_rows = []


for link in links:

    correlation_rows.append(
        {
            "Entity": (
                f"{link.get('entity_type', '')}:"
                f"{link.get('value', '')}"
            ),

            "Source A": link.get(
                "source_a",
                ""
            ),

            "Source B": link.get(
                "source_b",
                ""
            ),

            "Confidence": (
                f"{link.get('confidence', 0):.2f}"
            ),

            "Reason": link.get(
                "reason",
                ""
            )
        }
    )


if correlation_rows:

    correlation_df = pd.DataFrame(
        correlation_rows
    )

    st.dataframe(
        correlation_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No cross-source correlations detected."
    )


st.divider()


# ============================================================
# ENTITY TYPE SUMMARY
# ============================================================

st.header("🧩 Entity Intelligence")

entity_counts = {}

for entity in entities:

    entity_type = entity.get(
        "type",
        "UNKNOWN"
    )

    entity_counts[entity_type] = (
        entity_counts.get(
            entity_type,
            0
        ) + 1
    )


if entity_counts:

    entity_df = pd.DataFrame(
        [
            {
                "Entity Type": key,
                "Occurrences": value
            }

            for key, value
            in sorted(
                entity_counts.items()
            )
        ]
    )

    st.dataframe(
        entity_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# INVESTIGATION TIMELINE
# ============================================================

st.header("🕒 Investigation Timeline")

st.caption(
    "Chronological view of normalized evidence events."
)


timeline_rows = []


for record in records:

    timestamp = record.get(
        "timestamp"
    )

    if not timestamp:

        continue

    timeline_rows.append(
        {
            "Timestamp": str(
                timestamp
            ),

            "Event": record.get(
                "event_type",
                "UNKNOWN"
            ),

            "Source": record.get(
                "source",
                "UNKNOWN"
            )
        }
    )


if timeline_rows:

    timeline_df = pd.DataFrame(
        timeline_rows
    )

    timeline_df["Timestamp"] = pd.to_datetime(
        timeline_df["Timestamp"],
        errors="coerce"
    )

    timeline_df = timeline_df.dropna(
        subset=[
            "Timestamp"
        ]
    )

    timeline_df = timeline_df.sort_values(
        "Timestamp"
    )

    timeline_df["Timestamp"] = (
        timeline_df["Timestamp"]
        .dt.strftime(
            "%d-%b-%Y %H:%M:%S"
        )
    )

    timeline_df = timeline_df.reset_index(
        drop=True
    )

    st.dataframe(
        timeline_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No timestamped events available."
    )


st.divider()


# ============================================================
# INVESTIGATION LEAD GENERATOR
# ============================================================

st.header("🕵️ Investigation Leads")

st.caption(
    "Automatically generated next-step leads based on "
    "observed correlations and transaction patterns."
)


leads = []


# High-risk entities

for item in risk_results:

    if item.get(
        "level"
    ) in {
        "HIGH",
        "CRITICAL"
    }:

        leads.append(
            {
                "Priority": "HIGH",
                "Lead": (
                    f"Review evidence supporting "
                    f"{item.get('entity', '')}"
                ),
                "Basis": " | ".join(
                    item.get(
                        "reasons",
                        []
                    )
                )
            }
        )


# Cross-source links

for link in links:

    if link.get(
        "confidence",
        0
    ) >= 0.90:

        leads.append(
            {
                "Priority": "VERIFY",
                "Lead": (
                    f"Verify shared "
                    f"{link.get('entity_type', '')} "
                    f"{link.get('value', '')}"
                ),
                "Basis": (
                    f"{link.get('source_a', '')} ↔ "
                    f"{link.get('source_b', '')}"
                )
            }
        )


# Transaction hops

for record in records:

    if record.get(
        "event_type"
    ) != "TRANSACTION":

        continue

    receiver = record.get(
        "receiver_account"
    )

    if receiver:

        leads.append(
            {
                "Priority": "TRACE",
                "Lead": (
                    f"Trace downstream movement "
                    f"from account {receiver}"
                ),
                "Basis": (
                    f"Transaction "
                    f"{record.get('transaction_id', 'N/A')}"
                )
            }
        )


# Remove duplicates

unique_leads = []

seen_leads = set()


for lead in leads:

    key = (
        lead["Priority"],
        lead["Lead"]
    )

    if key in seen_leads:

        continue

    seen_leads.add(
        key
    )

    unique_leads.append(
        lead
    )


if unique_leads:

    leads_df = pd.DataFrame(
        unique_leads
    )

    st.dataframe(
        leads_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No automated investigation leads generated."
    )


st.divider()


# ============================================================
# EVIDENCE INTEGRITY
# ============================================================

st.header("🔐 Evidence Integrity")

st.caption(
    "SHA-256 fingerprints provide a verifiable "
    "digital integrity record for processed evidence."
)


integrity_rows = []


for item in evidence_hashes:

    integrity_rows.append(
        {
            "Evidence File": item.get(
                "file",
                "Unknown"
            ),

            "Size": (
                f"{item.get('size_bytes', 0):,} bytes"
            ),

            "SHA-256": item.get(
                "sha256",
                "ERROR"
            )
        }
    )


if integrity_rows:

    integrity_df = pd.DataFrame(
        integrity_rows
    )

    st.dataframe(
        integrity_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No evidence integrity records available."
    )


st.divider()


# ============================================================
# NETWORK STATISTICS
# ============================================================

st.header("📡 Network Statistics")


stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)


with stat_col1:

    st.metric(
        "Transaction Links",
        graph_info.get(
            "transaction_links",
            0
        )
    )


with stat_col2:

    st.metric(
        "Evidence Links",
        graph_info.get(
            "evidence_links",
            0
        )
    )


with stat_col3:

    st.metric(
        "Device / Network Links",
        graph_info.get(
            "device_links",
            0
        )
    )


with stat_col4:

    st.metric(
        "Total Graph Links",
        graph_info.get(
            "links",
            0
        )
    )


st.divider()


# ============================================================
# CASE ANALYSIS SUMMARY
# ============================================================

st.header("📋 Case Analysis Summary")


summary_col1, summary_col2 = st.columns(2)


with summary_col1:

    st.write(
        "**Evidence Pipeline**"
    )

    st.write(
        "📥 Evidence ingestion → "
        "🧪 Validation → "
        "🔐 Hashing → "
        "🔄 Normalization → "
        "🧩 Entity extraction"
    )


with summary_col2:

    st.write(
        "**Intelligence Pipeline**"
    )

    st.write(
        "🔗 Correlation → "
        "⚡ Triage → "
        "🚨 Risk analysis → "
        "🕸️ Network → "
        "🕵️ Investigation leads"
    )


st.divider()


# ============================================================
# INVESTIGATION EXPORT
# ============================================================

st.header("📦 Investigation Export")


json_col, pdf_col = st.columns(2)


# ============================================================
# JSON EXPORT
# ============================================================

with json_col:

    st.subheader(
        "📄 JSON Intelligence Report"
    )


    export_data = {

        "application":
            "CYBER-LINK AI",

        "title":
            "Evidence-to-Network Intelligence",

        "case_id":
            analysis_source,

        "generated_at":
            datetime.now().isoformat(),

        "analysis_mode":
            analysis_mode,

        "summary": {

            "evidence_files":
                len(evidence),

            "normalized_records":
                len(records),

            "entities":
                len(entities),

            "correlations":
                len(links),

            "risk_signals":
                len(risk_results),

            "network_nodes":
                graph_info.get(
                    "nodes",
                    0
                ),

            "network_links":
                graph_info.get(
                    "links",
                    0
                )
        },

        "risk_intelligence":
            risk_results,

        "correlations":
            links,

        "investigation_leads":
            unique_leads,

        "timeline":
            [
                {
                    "timestamp":
                        r.get(
                            "timestamp"
                        ),

                    "event_type":
                        r.get(
                            "event_type"
                        ),

                    "source":
                        r.get(
                            "source"
                        )
                }

                for r in records

                if r.get(
                    "timestamp"
                )
            ],

        "evidence_integrity":
            evidence_hashes,

        "investigator_note":
            (
                "Detected correlations and risk indicators "
                "are intelligence leads requiring independent "
                "verification. They are not conclusions of guilt."
            )
    }


    json_bytes = json.dumps(
        export_data,
        indent=4,
        default=str
    ).encode(
        "utf-8"
    )


    st.download_button(
        label="⬇️ Download JSON Report",
        data=json_bytes,
        file_name=(
            f"{analysis_source}_"
            "cyber_link_investigation.json"
        ),
        mime="application/json",
        use_container_width=True
    )


# ============================================================
# PDF EXPORT
# ============================================================

with pdf_col:

    st.subheader(
        "📑 PDF Investigation Report"
    )


    try:

        from reportlab.lib import colors

        from reportlab.lib.pagesizes import A4

        from reportlab.lib.styles import (
            getSampleStyleSheet
        )

        from reportlab.lib.units import mm

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )


        pdf_path = (
            REPORTS_DIR
            / f"{analysis_source}_report.pdf"
        )


        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm
        )


        styles = getSampleStyleSheet()

        story = []


        # ----------------------------------------------------
        # PDF HEADER
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "CYBER-LINK AI",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "Evidence-to-Network Intelligence",
                styles["Heading2"]
            )
        )

        story.append(
            Spacer(
                1,
                8
            )
        )

        story.append(
            Paragraph(
                f"Case ID: {analysis_source}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Generated: "
                f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}",
                styles["Normal"]
            )
        )

        story.append(
            Spacer(
                1,
                12
            )
        )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Investigation Summary",
                styles["Heading2"]
            )
        )


        summary_data = [
            ["Metric", "Value"],
            [
                "Evidence Files",
                str(len(evidence))
            ],
            [
                "Evidence Records",
                str(len(records))
            ],
            [
                "Extracted Entities",
                str(len(entities))
            ],
            [
                "Correlations",
                str(len(links))
            ],
            [
                "Risk Signals",
                str(len(risk_results))
            ],
            [
                "Network Nodes",
                str(
                    graph_info.get(
                        "nodes",
                        0
                    )
                )
            ],
            [
                "Network Links",
                str(
                    graph_info.get(
                        "links",
                        0
                    )
                )
            ]
        ]


        summary_table = Table(
            summary_data,
            colWidths=[
                80 * mm,
                70 * mm
            ]
        )


        summary_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    )
                ]
            )
        )


        story.append(
            summary_table
        )

        story.append(
            Spacer(
                1,
                15
            )
        )


        # ----------------------------------------------------
        # RISK
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Risk Intelligence",
                styles["Heading2"]
            )
        )


        risk_pdf_data = [
            [
                "Entity",
                "Score",
                "Level"
            ]
        ]


        for item in risk_results:

            risk_pdf_data.append(
                [
                    item.get(
                        "entity",
                        ""
                    ),

                    str(
                        item.get(
                            "score",
                            0
                        )
                    ),

                    item.get(
                        "level",
                        ""
                    )
                ]
            )


        if len(
            risk_pdf_data
        ) > 1:

            risk_table = Table(
                risk_pdf_data,
                colWidths=[
                    85 * mm,
                    25 * mm,
                    35 * mm
                ]
            )


            risk_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.lightgrey
                        ),

                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.grey
                        ),

                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold"
                        ),

                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP"
                        )
                    ]
                )
            )


            story.append(
                risk_table
            )


        story.append(
            Spacer(
                1,
                15
            )
        )


        # ----------------------------------------------------
        # CORRELATIONS
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Cross-Source Correlations",
                styles["Heading2"]
            )
        )


        correlation_pdf_data = [
            [
                "Entity",
                "Source A",
                "Source B",
                "Confidence"
            ]
        ]


        for link in links:

            correlation_pdf_data.append(
                [
                    (
                        f"{link.get('entity_type', '')}:"
                        f"{link.get('value', '')}"
                    ),

                    link.get(
                        "source_a",
                        ""
                    ),

                    link.get(
                        "source_b",
                        ""
                    ),

                    (
                        f"{link.get('confidence', 0):.2f}"
                    )
                ]
            )


        if len(
            correlation_pdf_data
        ) > 1:

            correlation_table = Table(
                correlation_pdf_data,
                colWidths=[
                    65 * mm,
                    35 * mm,
                    35 * mm,
                    25 * mm
                ]
            )


            correlation_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.lightgrey
                        ),

                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.grey
                        ),

                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, 0),
                            "Helvetica-Bold"
                        ),

                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            7
                        ),

                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP"
                        )
                    ]
                )
            )


            story.append(
                correlation_table
            )


        story.append(
            Spacer(
                1,
                15
            )
        )


        # ----------------------------------------------------
        # INTEGRITY
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Evidence Integrity",
                styles["Heading2"]
            )
        )


        integrity_pdf_data = [
            [
                "File",
                "Size",
                "SHA-256"
            ]
        ]


        for item in evidence_hashes:

            integrity_pdf_data.append(
                [
                    item.get(
                        "file",
                        ""
                    ),

                    f"{item.get('size_bytes', 0):,}",

                    item.get(
                        "sha256",
                        ""
                    )
                ]
            )


        integrity_table = Table(
            integrity_pdf_data,
            colWidths=[
                45 * mm,
                25 * mm,
                90 * mm
            ]
        )


        integrity_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        6
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    )
                ]
            )
        )


        story.append(
            integrity_table
        )

        story.append(
            Spacer(
                1,
                15
            )
        )


        # ----------------------------------------------------
        # INVESTIGATOR NOTE
        # ----------------------------------------------------

        story.append(
            Paragraph(
                "Investigator Note",
                styles["Heading2"]
            )
        )


        story.append(
            Paragraph(
                "Detected correlations and risk indicators "
                "are intelligence leads requiring independent "
                "verification. They are not conclusions of guilt.",
                styles["Normal"]
            )
        )


        # ----------------------------------------------------
        # BUILD PDF
        # ----------------------------------------------------

        doc.build(
            story
        )


        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            pdf_bytes = pdf_file.read()


        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name=(
                f"{analysis_source}_report.pdf"
            ),
            mime="application/pdf",
            use_container_width=True
        )


    except ImportError:

        st.error(
            "ReportLab is not installed. "
            "Run: pip install reportlab"
        )


    except Exception as error:

        st.error(
            "PDF generation failed."
        )

        st.exception(
            error
        )


st.divider()


# ============================================================
# FINAL INVESTIGATOR NOTE
# ============================================================

st.header("⚠️ Investigator Note")

st.warning(
    "Detected correlations, risk scores and network "
    "relationships are intelligence leads. They require "
    "independent investigator verification and are not "
    "conclusions of guilt."
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "CYBER-LINK AI | Evidence-to-Network Intelligence | "
    "Synthetic demonstration / investigator-uploaded evidence"
)