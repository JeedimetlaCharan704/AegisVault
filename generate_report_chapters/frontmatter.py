import os
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from common import  add_p, add_h1, add_h2, add_img, apply_ref_table_style, get_base64_img, IMG_DIR

def build_frontmatter_docx(doc):
    # ----------------- COVER PAGE (PERFECTLY SCALED, ZERO OVERFLOW) -----------------
    add_p(doc, "A", font_name="Cambria", size_pt=14, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "Project report on", font_name="Cambria", size_pt=14, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=6)

    add_p(doc, "AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails",
          font_name="Cambria", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.2, sp_before=4, sp_after=8)

    add_p(doc, "Submitted in partial fulfilment of the award of the", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "Bachelor of Technology", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "in", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "Department of Computer Science and Engineering", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=6)

    add_p(doc, "By", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "JEEDIMETLA CHARAN – 241U1R3026 (LG Group: 09)\nRAKESH JAKKULA – 214U1R3020 (LG Group: 09)",
          font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.2, sp_before=2, sp_after=6)

    add_p(doc, "Under the esteemed guidance of", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "Ms. R. Karunasree", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "Assistant Professor, Dept. of CSE", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=6)

    # University logo
    add_img(doc, "aurora_logo.jpeg", width=Inches(1.1))

    add_p(doc, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (CSE-DS)\nSCHOOL OF ENGINEERING",
          font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=4, sp_after=2)
    add_p(doc, "AURORA HIGHER EDUCATION AND RESEARCH ACADEMY",
          font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "(Deemed to be University)", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
    add_p(doc, "Parvathapur, Uppal, Hyderabad-500 098 (2025-26)", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=6)

    # University seals
    tbl_seals = doc.add_table(rows=1, cols=2)
    tbl_seals.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in tbl_seals.rows[0].cells:
        c.width = Inches(2.5)
    p_s1 = tbl_seals.rows[0].cells[0].paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(os.path.join(IMG_DIR, 'seal_left.jpeg')):
        p_s1.add_run().add_picture(os.path.join(IMG_DIR, 'seal_left.jpeg'), width=Inches(1.0))
    p_s2 = tbl_seals.rows[0].cells[1].paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(os.path.join(IMG_DIR, 'seal_right.jpeg')):
        p_s2.add_run().add_picture(os.path.join(IMG_DIR, 'seal_right.jpeg'), width=Inches(0.72))

    doc.add_page_break()

    # ----------------- DECLARATION -----------------
    add_h1(doc, "DECLARATION", sp_before=14, sp_after=10)
    add_p(doc, "We hereby declare that the comprehensive course project work described in this report, entitled “AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails”, submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering (Data Science) to Aurora Higher Education and Research Academy (Deemed to be University), is a bona fide record of original research, theoretical formulation, and engineering development carried out by us under the esteemed guidance of Ms. R. Karunasree, Assistant Professor, Department of Computer Science and Engineering.")

    add_p(doc, "The course project work presented in this report is original and reflects our independent contributions to sequence learning modeling, convex mathematical optimization, smart contract security engineering, and multi-agent systems. All data sources, mathematical derivations, software libraries, and literature references utilized during this investigation have been appropriately cited and acknowledged in accordance with academic integrity and ethical research standards.")

    add_p(doc, "We further declare that neither this report nor any substantial part of the underlying algorithms, architectures, and empirical findings has been previously submitted to this or any other university, college, or academic institution for the award of any degree, diploma, fellowship, or professional certification.")

    add_p(doc, "Place: Hyderabad\nDate: 27-11-2026", align=WD_ALIGN_PARAGRAPH.LEFT, line_sp=1.5, sp_before=16, sp_after=16)

    add_p(doc, "Signature of the Students:", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, sp_before=8, sp_after=4)
    add_p(doc, "Jeedimetla Charan  –  241U1R3026 (LG Group: 09)\nRakesh Jakkula     –  214U1R3020 (LG Group: 09)",
          font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_sp=1.3, sp_before=2, sp_after=16)

    tbl_dec_seals = doc.add_table(rows=1, cols=2)
    tbl_dec_seals.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in tbl_dec_seals.rows[0].cells:
        c.width = Inches(2.5)
    p_d1 = tbl_dec_seals.rows[0].cells[0].paragraphs[0]
    p_d1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(os.path.join(IMG_DIR, 'seal_left.jpeg')):
        p_d1.add_run().add_picture(os.path.join(IMG_DIR, 'seal_left.jpeg'), width=Inches(1.0))
    p_d2 = tbl_dec_seals.rows[0].cells[1].paragraphs[0]
    p_d2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(os.path.join(IMG_DIR, 'seal_right.jpeg')):
        p_d2.add_run().add_picture(os.path.join(IMG_DIR, 'seal_right.jpeg'), width=Inches(0.72))

    doc.add_page_break()

    # ----------------- CERTIFICATE -----------------
    add_h1(doc, "CERTIFICATE", sp_before=14, sp_after=10)
    add_p(doc, "This is to certify that the course project report entitled “AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails” is a bona fide record of work carried out by Jeedimetla Charan (Roll No: 241U1R3026) and Rakesh Jakkula (Roll No: 214U1R3020), students of III Year – II Term, Bachelor of Technology in Computer Science and Engineering (Data Science), submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering during the academic year 2026–2027.")

    add_p(doc, "The technical investigations, neural network architectures, convex portfolio optimization algorithms, formal smart contract invariant proofs, and empirical stress test evaluations described in this document have been completed under our direct supervision. The results embodied in this report have been verified, systematically tested, and found completely satisfactory for academic evaluation in the course Deep Learning.")

    add_p(doc, "Date: 27-11-2026\nHyderabad", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_sp=1.3, sp_before=14, sp_after=28)

    add_p(doc, "Internal Guide:                                                        Head of Department:", font_name="Cambria", size_pt=12, bold=True, sp_before=8, sp_after=3)
    add_p(doc, "Ms. R. Karunasree                                                      Dr. Mahesh Prabhu", font_name="Cambria", size_pt=12, bold=True, sp_before=2, sp_after=2)
    add_p(doc, "Assistant Professor, Dept. of CSE                                      Professor & Head, Dept. of CSE-DS", font_name="Cambria", size_pt=12, sp_before=2, sp_after=2)
    add_p(doc, "School of Engineering                                                  School of Engineering", font_name="Cambria", size_pt=12, sp_before=2, sp_after=24)

    add_p(doc, "External Examiner: ___________________________", font_name="Cambria", size_pt=12, bold=True, sp_before=12, sp_after=6)

    doc.add_page_break()

    # ----------------- ACKNOWLEDGEMENT -----------------
    add_h1(doc, "ACKNOWLEDGEMENT", sp_before=14, sp_after=10)
    add_p(doc, "First and foremost, we express our profound gratitude to our esteemed guide and course instructor, Ms. R. Karunasree, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, rigorous academic direction, and continuous encouragement throughout the conception, modeling, and completion of this project. Her constructive critiques and deep insights into sequence learning models and machine learning pipelines proved instrumental in successfully architecting the deep learning co-processor framework.")

    add_p(doc, "We extend our sincere thanks to Dr. Mahesh Prabhu, Professor and Head of Department, Department of CSE-DS, and the Dean, School of Engineering, Aurora Higher Education and Research Academy (Deemed to be University), for providing the state-of-the-art computational infrastructure, high-performance GPU workstations, laboratory facilities, and institutional support required to conduct continuous model training, sequence simulation, and decentralized testnet evaluations.")

    add_p(doc, "We are also deeply thankful to all the faculty members of the Department of Computer Science and Engineering and the Department of Data Science for their technical advice, academic discussions, and moral support throughout our undergraduate coursework. We extend our appreciation to the laboratory technical staff who assisted in maintaining reliable network connectivity and computational hardware environments.")

    add_p(doc, "Finally, we express our heartfelt appreciation to our parents, family members, and friends for their unfailing encouragement, constant understanding, patience, and moral support throughout our academic endeavors. Their confidence in our abilities has been our greatest source of inspiration.")

    add_p(doc, "Jeedimetla Charan (241U1R3026)\nRakesh Jakkula (214U1R3020)\nIII Year – II Term, CSE-DS",
          font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, line_sp=1.3, sp_before=20, sp_after=8)

    doc.add_page_break()

    # ----------------- ABSTRACT -----------------
    add_h1(doc, "ABSTRACT", sp_before=14, sp_after=10)
    add_p(doc, "Decentralized Finance (DeFi) protocols have unlocked permissionless lending, borrowing, and automated market making with over $100 billion in Total Value Locked (TVL). However, capital allocators face severe structural risks: highly stochastic liquidity yield fluctuations, impermanent loss, and devastating economic exploits such as flash-loan attacks. Traditional on-chain yield vaults rely on naive, static heuristics or human-governed multisig updates that are too slow to react to real-time market crashes and too computationally constrained to execute non-linear predictive modeling on EVM execution layers.")

    add_p(doc, "This project presents AegisVault, an end-to-end autonomous decentralized vault architecture powered by an off-chain deep learning co-processor paired with on-chain formal Solidity invariant guardrails. The core predictive engine integrates a Bidirectional Long Short-Term Memory and Gated Recurrent Unit (BiLSTM-GRU) neural network with Multi-Head Self-Attention to forecast multi-step non-linear Annual Percentage Yields (APY) across major lending protocols (Aave V3, Morpho Blue, Compound V3, Uniswap V3). Simultaneously, a Graph Convolutional Network (GCN) models liquidity spillover and cross-pool volatility covariance matrices.")

    add_p(doc, "These forecasted vectors are ingested by an off-chain Modern Portfolio Theory (MPT) quadratic programming solver that computes Sharpe-optimal capital allocations while enforcing strict mathematical guardrails: a 40% maximum allocation ceiling per strategy and a 10% minimum liquid cash reserve floor. An autonomous Sentinel Agent continuously monitors real-time pool borrow spikes, utilization anomalies, and APY crashes using z-score thresholding and Isolation Forests. Upon detecting flash-loan surges, Sentinel bypasses standard rebalancing queues and triggers an immediate emergency recall of funds to the cash floor.")

    add_p(doc, "The optimal target weights are co-signed using cryptographic EIP-712 structured data intents by an off-chain Auditor Agent and submitted to AegisVault.sol on Base Sepolia EVM. The contract routes allocations through InvariantGuard.sol, which formally asserts reserve constraints at the EVM opcode level, reverting any transaction that breaches safety invariants. Experimental results demonstrate that the BiLSTM-GRU predictor achieves an MAE of 0.021 (a 49% improvement over traditional ARIMA and XGBoost baselines), and the autonomous Sentinel mechanism completely mitigated simulated 45M USDC flash-loan liquidity drains with 0.00% capital loss. The full-stack platform is live and verified on the Base Sepolia testnet and deployed on Vercel.")

    add_h2(doc, "Keywords", sp_before=8, sp_after=3)
    add_p(doc, "Deep Learning, BiLSTM-GRU, Graph Convolutional Networks, Modern Portfolio Theory, Autonomous Multi-Agent Systems, Decentralized Finance (DeFi), ERC-4626, Solidity Formal Invariants, Flash-Loan Anomaly Detection, EIP-712 Intent Signing.",
          font_name="Times New Roman", size_pt=12, bold=False, italic=True, sp_before=2, sp_after=8)

    doc.add_page_break()

    # ----------------- TABLE OF CONTENTS -----------------
    add_h1(doc, "TABLE OF CONTENTS", sp_before=14, sp_after=10)

    toc_data = [
        ("1.", "DECLARATION", "2"),
        ("2.", "CERTIFICATE", "3"),
        ("3.", "ACKNOWLEDGEMENT", "4"),
        ("4.", "ABSTRACT", "5"),
        ("5.", "Chapter – 1: Precedent Study\n      1.1 Introduction to the Project\n      1.2 Background Study\n      1.3 Motivation to the Project\n      1.4 Software Development Life Cycle (SDLC) Applied", "7–11"),
        ("6.", "Chapter – 2: Literature Survey\n      2.1 Survey of Six Major Research Articles\n      2.2 Comparison Table of Literature Articles vs. AegisVault\n      2.3 Observations from Comparison\n      2.4 Drawbacks of Existing Approaches\n      2.5 Advantages of Proposed Course Project", "12–18"),
        ("7.", "Chapter – 3: Project Design\n      3.1 Architecture Components\n      3.2 High-Level Architecture Diagram\n      3.3 Deep Learning Model Architecture\n      3.4 Algorithms Employed (Algorithms 1 to 8)\n      3.5 Flowchart Incorporated & Explanation\n      3.6 UML Use Case Diagram\n      3.7 UML Class Diagram\n      3.8 UML Sequence Diagrams (Rebalance & Attack Defense)\n      3.9 UML Component Architecture Diagram", "19–29"),
        ("8.", "Chapter – 4: Project Implementation\n      4.1 Introduction to Implementation Phase\n      4.2 Development Environment and Tools\n      4.3 Implementation Strategy\n      4.4 Module-Wise Implementation\n      4.5 Frontend Implementation\n      4.6 Data Storage and Data Handling\n      4.7 Security Measures Implemented\n      4.8 Error Handling and Validation\n      4.9 Execution and Results", "30–36"),
        ("9.", "Chapter – 5: Experimental Results and Discussions\n      5.1 Valid Result Description & Test Cases Table\n      5.2 Screenshots of Valid Operations & Dashboard\n      5.3 Observations on Valid Operations\n      5.4 Invalid Result Description & Attack Test Cases Table\n      5.5 Screenshots of Invalid Operations & Defense Telemetry\n      5.6 Observations on Invalid Operations\n      5.7 Overall Discussion Key Points\n      5.8 Limitations & Future Improvements", "37–44"),
        ("10.", "Chapter – 6: Conclusion and Future Enhancements\n      6.1 Conclusion\n      6.2 Key Achievements\n      6.3 Future Enhancements Description\n      6.4 Proposed Future Enhancements", "45–47"),
        ("11.", "Chapter – 7: Bibliography\n      7.1 Reference Books\n      7.2 Reference Papers\n      7.3 Reference Websites", "48–50")
    ]

    tbl_toc = doc.add_table(rows=len(toc_data)+1, cols=3)
    col_w = [Inches(0.8), Inches(4.5), Inches(0.9)]
    tbl_toc.rows[0].cells[0].paragraphs[0].text = "S. No."
    tbl_toc.rows[0].cells[1].paragraphs[0].text = "Contents"
    tbl_toc.rows[0].cells[2].paragraphs[0].text = "Page No."

    for idx, (sno, cont, pg) in enumerate(toc_data):
        row = tbl_toc.rows[idx+1]
        row.cells[0].paragraphs[0].text = sno
        row.cells[1].paragraphs[0].text = cont
        row.cells[2].paragraphs[0].text = pg
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    apply_ref_table_style(tbl_toc, col_widths=col_w)

    doc.add_page_break()
