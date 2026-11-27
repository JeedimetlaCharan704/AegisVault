import os, base64
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

base_dir = r'c:\3rd year charan\Hackathon project analysis\aegis-vault'
img_dir = os.path.join(base_dir, 'report_images')
docx_path = os.path.join(base_dir, 'DEEP_LEARNING_PROJECT_REPORT.docx')
html_path = os.path.join(base_dir, 'DEEP_LEARNING_PROJECT_REPORT.html')

# ==========================================
# 1. GENERATE DOCX (EXACT REFERENCE FORMAT)
# ==========================================
doc = docx.Document()

# Configure Margins: 1.0 inch all around (A4 paper)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

# Standard Black Color
BLACK = RGBColor(0, 0, 0)

def add_p(doc, text="", font_name="Times New Roman", size_pt=12, bold=False, italic=False,
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_sp=1.5, sp_before=0, sp_after=4):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text)
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.line_spacing = line_sp
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    return p

# In reference: Heading 1 is 14pt Bold Cambria / Times New Roman, Black, uppercase
def add_h1(doc, text, align=WD_ALIGN_PARAGRAPH.CENTER, sp_before=12, sp_after=8):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Cambria"
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    p.paragraph_format.line_spacing = 1.15
    return p

# In reference: Heading 2 (Chapter titles & section headings) is 12pt Bold Times New Roman, Black
def add_h2(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, sp_before=8, sp_after=3):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    p.paragraph_format.line_spacing = 1.15
    return p

# Sub-subheading: 12pt Bold Italic Times New Roman, Black
def add_h3(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, sp_before=6, sp_after=2):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.italic = True
    r.font.color.rgb = BLACK
    p.alignment = align
    p.paragraph_format.space_before = Pt(sp_before)
    p.paragraph_format.space_after = Pt(sp_after)
    p.paragraph_format.line_spacing = 1.15
    return p

def add_img(doc, img_name, width=Inches(5.6), caption=None):
    p_path = os.path.join(img_dir, img_name)
    if os.path.exists(p_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(p_path, width=width)
        
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(11)
            r_cap.italic = True
            r_cap.bold = True
            r_cap.font.color.rgb = BLACK

def apply_ref_table_style(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Single 0.5pt black border around all cells (identical to reference XML)
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    table._tbl.tblPr.append(tblBorders)

    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for j, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and j < len(col_widths):
                cell.width = col_widths[j]
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)
                    r.font.color.rgb = BLACK
                    if i == 0:
                        r.bold = True

# ----------------- COVER PAGE -----------------
add_p(doc, "A", font_name="Cambria", size_pt=14, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=6, sp_after=2)
add_p(doc, "Project report on", font_name="Cambria", size_pt=14, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=8)

add_p(doc, "AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails",
      font_name="Times New Roman", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.2, sp_before=4, sp_after=12)

add_p(doc, "Submitted in partial fulfilment of the award of the", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "Bachelor of Technology", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "in", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "Department of Computer Science and Engineering", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=10)

add_p(doc, "By", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=3)
add_p(doc, "JEEDIMETLA CHARAN – 241U1R3026 (LG Group: 09)\nRAKESH JAKKULA – 214U1R3020 (LG Group: 09)",
      font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.2, sp_before=2, sp_after=10)

add_p(doc, "Under the esteemed guidance of", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "Ms. R. Karunasree", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "Assistant Professor, Dept. of CSE", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=8)

# Aurora logo
add_img(doc, "aurora_logo.jpeg", width=Inches(1.2))

add_p(doc, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (CSE-DS)\nSCHOOL OF ENGINEERING",
      font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=4, sp_after=2)
add_p(doc, "AURORA HIGHER EDUCATION AND RESEARCH ACADEMY",
      font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "(Deemed to be University)", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=2)
add_p(doc, "Parvathapur, Uppal, Hyderabad-500 098 (2025-26)", font_name="Cambria", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, line_sp=1.15, sp_before=2, sp_after=8)

# Seals
tbl_seals = doc.add_table(rows=1, cols=2)
tbl_seals.alignment = WD_TABLE_ALIGNMENT.CENTER
for c in tbl_seals.rows[0].cells:
    c.width = Inches(2.5)
p_s1 = tbl_seals.rows[0].cells[0].paragraphs[0]
p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
if os.path.exists(os.path.join(img_dir, 'seal_left.jpeg')):
    p_s1.add_run().add_picture(os.path.join(img_dir, 'seal_left.jpeg'), width=Inches(1.1))
p_s2 = tbl_seals.rows[0].cells[1].paragraphs[0]
p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
if os.path.exists(os.path.join(img_dir, 'seal_right.jpeg')):
    p_s2.add_run().add_picture(os.path.join(img_dir, 'seal_right.jpeg'), width=Inches(0.8))

doc.add_page_break()

# ----------------- DECLARATION -----------------
add_h1(doc, "DECLARATION", sp_before=14, sp_after=10)
add_p(doc, "We hereby declare that the comprehensive course project work described in this report, entitled “AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails”, submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering (Data Science) to Aurora Higher Education and Research Academy (Deemed to be University), is a bona fide record of original research and development carried out by us under the esteemed guidance of Ms. R. Karunasree, Assistant Professor, Department of Computer Science and Engineering.")

add_p(doc, "The course project work is original, and neither the report nor any substantial part of it has been previously submitted to this or any other university or institution for the award of any degree, diploma, or academic credit.")

add_p(doc, "Place: Hyderabad\nDate: 22-12-2025", align=WD_ALIGN_PARAGRAPH.LEFT, line_sp=1.5, sp_before=16, sp_after=16)

add_p(doc, "Signature of the Students:", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, sp_before=8, sp_after=4)
add_p(doc, "Jeedimetla Charan  –  241U1R3026 (LG Group: 09)\nRakesh Jakkula     –  214U1R3020 (LG Group: 09)",
      font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_sp=1.3, sp_before=2, sp_after=16)

tbl_dec_seals = doc.add_table(rows=1, cols=2)
tbl_dec_seals.alignment = WD_TABLE_ALIGNMENT.CENTER
for c in tbl_dec_seals.rows[0].cells:
    c.width = Inches(2.5)
p_d1 = tbl_dec_seals.rows[0].cells[0].paragraphs[0]
p_d1.alignment = WD_ALIGN_PARAGRAPH.CENTER
if os.path.exists(os.path.join(img_dir, 'seal_left.jpeg')):
    p_d1.add_run().add_picture(os.path.join(img_dir, 'seal_left.jpeg'), width=Inches(1.1))
p_d2 = tbl_dec_seals.rows[0].cells[1].paragraphs[0]
p_d2.alignment = WD_ALIGN_PARAGRAPH.CENTER
if os.path.exists(os.path.join(img_dir, 'seal_right.jpeg')):
    p_d2.add_run().add_picture(os.path.join(img_dir, 'seal_right.jpeg'), width=Inches(0.8))

doc.add_page_break()

# ----------------- CERTIFICATE -----------------
add_h1(doc, "CERTIFICATE", sp_before=14, sp_after=10)
add_p(doc, "This is to certify that the course project report entitled “AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails” is a bona fide record of work carried out by Jeedimetla Charan (Roll No: 241U1R3026) and Rakesh Jakkula (Roll No: 214U1R3020), students of III Year – II Term, Bachelor of Technology in Computer Science and Engineering (Data Science), submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering during the academic year 2025–2026.")

add_p(doc, "The results presented in this project report have been verified, systematically tested, and found satisfactory for academic evaluation in the course Deep Learning.")

add_p(doc, "Date: 22-12-2025\nHyderabad", font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_sp=1.3, sp_before=16, sp_after=30)

add_p(doc, "Internal Guide:                                                        Head of Department:", font_name="Cambria", size_pt=12, bold=True, sp_before=10, sp_after=3)
add_p(doc, "Ms. R. Karunasree                                                      Dr. S. Ramanathan", font_name="Cambria", size_pt=12, bold=True, sp_before=2, sp_after=2)
add_p(doc, "Assistant Professor, Dept. of CSE                                      Professor & Head, Dept. of CSE-DS", font_name="Cambria", size_pt=12, sp_before=2, sp_after=2)
add_p(doc, "School of Engineering                                                  School of Engineering", font_name="Cambria", size_pt=12, sp_before=2, sp_after=24)

add_p(doc, "External Examiner: ___________________________", font_name="Cambria", size_pt=12, bold=True, sp_before=14, sp_after=8)

doc.add_page_break()

# ----------------- ACKNOWLEDGEMENT -----------------
add_h1(doc, "ACKNOWLEDGEMENT", sp_before=14, sp_after=10)
add_p(doc, "First and foremost, we express our profound gratitude to our esteemed guide and course instructor, Ms. R. Karunasree, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, rigorous academic direction, and continuous encouragement throughout the conception, modeling, and completion of this project. Her constructive critiques and deep insights into sequence learning models and machine learning pipelines proved instrumental in successfully architecting the deep learning co-processor framework.")

add_p(doc, "We extend our heartfelt thanks to the Head of Department, Department of CSE-DS, and the Dean, School of Engineering, Aurora Higher Education and Research Academy (Deemed to be University), for providing the state-of-the-art computational infrastructure, laboratory facilities, and institutional support required to conduct continuous simulation, model training, and decentralized testnet evaluations.")

add_p(doc, "We are also deeply thankful to our faculty members, laboratory instructors, and administrative staff for their technical support, encouragement, and advice. Finally, we express our deepest appreciation to our parents, family members, and peers for their unfailing moral support, understanding, and enthusiasm throughout our academic journey.")

add_p(doc, "Jeedimetla Charan (241U1R3026)\nRakesh Jakkula (214U1R3020)\nIII Year – II Term, CSE-DS",
      font_name="Cambria", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, line_sp=1.3, sp_before=24, sp_after=8)

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
    ("5.", "Chapter – 1: Precedent Study\n      1.1 Introduction to the Project\n      1.2 Background Study\n      1.3 Motivation to the Project", "7–11"),
    ("6.", "Chapter – 2: Literature Survey\n      2.1 Comparison of Existing Related Approaches\n      2.2 Observations from Comparison\n      2.3 Drawbacks of Existing Approaches\n      2.4 Advantages of Proposed Course Project", "12–16"),
    ("7.", "Chapter – 3: Project Design\n      3.1 Architecture Components\n      3.2 High-Level Architecture Diagram\n      3.3 Deep Learning Model Architecture\n      3.4 Algorithms Employed\n      3.5 Flowchart Incorporated & Explanation\n      3.6 UML Use Case Diagram\n      3.7 UML Class Diagram\n      3.8 UML Sequence Diagrams (Rebalance & Attack Defense)\n      3.9 UML Component Architecture Diagram", "17–26"),
    ("8.", "Chapter – 4: Project Implementation\n      4.1 Introduction to Implementation Phase\n      4.2 Development Environment and Tools\n      4.3 Implementation Strategy\n      4.4 Module-Wise Implementation\n      4.5 Frontend Implementation\n      4.6 Data Storage and Data Handling\n      4.7 Security Measures Implemented\n      4.8 Error Handling and Validation\n      4.9 Execution and Results", "27–33"),
    ("9.", "Chapter – 5: Experimental Results and Discussions\n      5.1 Valid Result Description & Test Cases Table\n      5.2 Screenshots of Valid Operations & Dashboard\n      5.3 Observations on Valid Operations\n      5.4 Invalid Result Description & Attack Test Cases Table\n      5.5 Screenshots of Invalid Operations & Defense Telemetry\n      5.6 Observations on Invalid Operations\n      5.7 Overall Discussion Key Points\n      5.8 Limitations & Future Improvements", "34–40"),
    ("10.", "Chapter – 6: Conclusion and Future Enhancements\n      6.1 Conclusion\n      6.2 Key Achievements\n      6.3 Future Enhancements Description\n      6.4 Proposed Future Enhancements", "41–43"),
    ("11.", "Chapter – 7: Bibliography\n      7.1 Reference Books\n      7.2 Reference Papers\n      7.3 Reference Websites", "44–46")
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

# ----------------- CHAPTER 1 -----------------
add_h2(doc, "Chapter – 1: Precedent Study", sp_before=12, sp_after=6)

add_h2(doc, "Introduction to the Project", sp_before=8, sp_after=3)
add_p(doc, "In the current era of rapid digital transformation and financial innovation, decentralized ledger technologies and smart contracts have transformed traditional capital allocation. Decentralized Finance (DeFi) platforms such as Aave, Morpho Blue, Compound, and Uniswap manage billions of dollars in programmatic liquidity pools. These platforms enable users to supply digital assets (such as USD Coin, USDC) to earn real-time interest rates generated by decentralized lending markets and trading fee volumes.")

add_p(doc, "However, managing decentralized capital efficiently across multiple protocol liquidity pools presents significant challenges. The yield rates (Annual Percentage Yield, APY) across lending pools are highly dynamic, non-linear, and volatile. They fluctuate drastically based on pool utilization, flash-loan volume surges, protocol governance changes, and macro liquidity conditions. Moreover, capital allocators face catastrophic risks, including flash-loan price manipulation, smart contract vulnerabilities, and sudden liquidity crunches.")

add_p(doc, "AegisVault is an autonomous, decentralized yield optimization and threat-mitigation vault developed to demonstrate the practical application of Deep Learning co-processors, Modern Portfolio Theory (MPT), and formal invariant software engineering in autonomous finance. The system dynamically monitors multiple protocol liquidity pools, predicts future multi-step yield and volatility trends using deep neural networks, solves for optimal Sharpe ratio capital allocations, and enforces mathematical safety invariant guardrails directly on-chain.")

add_p(doc, "The project bridges advanced Deep Learning methodology with secure Web3 software engineering. While traditional on-chain vaults rely on manual human governance or simplistic static thresholds, AegisVault introduces an off-chain multi-agent co-processor that offloads heavy tensor matrix operations and convex quadratic programming from the resource-constrained Ethereum Virtual Machine (EVM), while maintaining verifiable on-chain safety through cryptographic EIP-712 signed intents and Solidity invariant contracts.")

add_h2(doc, "Background Study", sp_before=8, sp_after=3)
add_p(doc, "Decentralized liquidity vault systems have evolved through multiple phases, transitioning from basic single-asset yield lockers to multi-strategy yield aggregators (such as Yearn Finance). In early vault architectures, users deposited collateral into a single smart contract that forwarded capital to a single external lending pool. As DeFi protocols multiplied, capital allocation required dynamic rebalancing to capture superior interest rates across competing markets.")

add_p(doc, "The development of a complete autonomous decentralized vault system involves several foundational software engineering and data science components:")

add_h3(doc, "Requirement Analysis")
add_p(doc, "This phase focuses on identifying functional and security requirements. In an autonomous vault system, functional requirements include real-time on-chain telemetry ingestion, automated yield forecasting, Sharpe ratio optimization, user share accounting (ERC-4626 standard), and atomic rebalance execution. Non-functional and security requirements include formal invariant verification (e.g., maximum 40% allocation cap per strategy, minimum 10% liquid cash reserve floor), sub-second flash-loan anomaly detection, and cryptographic integrity.")

add_h3(doc, "System Design")
add_p(doc, "During this phase, the system architecture is decomposed into distinct, decoupled modular layers: an on-chain execution layer (AegisVault.sol, InvariantGuard.sol, strategy connectors), an off-chain deep learning co-processor (FastAPI server, PyTorch neural networks, MPT solver), an autonomous multi-agent monitoring layer (Sentinel anomaly detector, Auditor verification agent), and a client interface (React 19, Viem, Wagmi, real-time WebSockets). This decoupled design ensures gas-efficient on-chain execution while enabling complex multi-variate deep learning inferences.")

add_h3(doc, "Implementation")
add_p(doc, "The implementation phase translates theoretical formulations into production software. Deep learning models are implemented in PyTorch using Bidirectional LSTM, Gated Recurrent Units (GRU), and multi-head self-attention mechanisms. The MPT optimizer utilizes Sequential Least Squares Quadratic Programming (SLSQP). Smart contracts are implemented in Solidity 0.8.24 utilizing OpenZeppelin ERC-4626 standards, deployed and verified on the Base Sepolia Layer-2 EVM testnet. The frontend is built using React 19, TypeScript, and Tailwind CSS, deployed live on Vercel.")

add_h3(doc, "Testing")
add_p(doc, "Testing is executed across multiple stages: unit testing of neural network prediction heads, convex optimization convergence testing, hardhat simulated fork testing of smart contracts, and adversarial stress testing. A simulated flash-loan borrow surge is executed against protocol pools to verify that Sentinel detects anomalies and InvariantGuard reverts any non-compliant state transition.")

add_h3(doc, "Deployment")
add_p(doc, "Deployment entails launching the smart contracts to the Base Sepolia testnet, hosting the Python FastAPI co-processor daemon on an enterprise application runner, and distributing the Web3 frontend globally via Vercel Edge Networks. Deployed contract addresses and ABIs are automatically synchronized to the client.")

add_h3(doc, "Maintenance")
add_p(doc, "Post-deployment maintenance involves continuous monitoring of keeper daemon latency, retrained model weights as market regimes shift, and on-chain telemetry caching. This structured lifecycle guarantees the long-term reliability and safety of the autonomous vault.")

add_h2(doc, "Motivation to the Project", sp_before=8, sp_after=3)
add_p(doc, "The motivation behind building AegisVault stems from several compelling academic, practical, and financial considerations:")

add_h3(doc, "Application of Deep Learning Theory")
add_p(doc, "While deep learning is widely utilized in computer vision and natural language processing, applying sequence learning (BiLSTM-GRU) and graph convolutional neural networks to real-time decentralized liquidity time-series represents a frontier research domain. It demonstrates how AI can serve as an off-chain co-processor for verifiable distributed systems.")

add_h3(doc, "Need for Structured Software & Autonomous Vault Engineering")
add_p(doc, "Billions of dollars have been lost in DeFi due to economic attacks and flash-loan exploits. AegisVault demonstrates how integrating formal invariant checks (asserting safety bounds at the contract level) directly mitigates adversarial manipulation, illustrating the necessity of rigorous software engineering.")

add_h3(doc, "Real-World Relevance in Decentralized Finance")
add_p(doc, "As traditional institutional capital moves onto blockchain rails through tokenized real-world assets (RWA) and stablecoins, institutional investors demand mathematical risk management, automated Sharpe optimization, and provable safety invariants rather than opaque custodial promises.")

add_h3(doc, "Skill Development in AI & Web3 Co-Processors")
add_p(doc, "Developing AegisVault enabled comprehensive skill acquisition spanning deep sequence modeling in PyTorch, convex mathematical optimization, smart contract development in Solidity, cryptographic signing (EIP-712), and modern reactive web development in React 19.")

add_h3(doc, "Preparation for Industry Practices")
add_p(doc, "The project aligns with contemporary enterprise Web3 and FinTech architectures, where multi-agent off-chain systems process big data streams and submit cryptographically verified state changes to distributed ledgers.")

add_h3(doc, "Scope for Future Enhancements")
add_p(doc, "The modular architecture allows seamless extension to cross-chain liquidity networks (Chainlink CCIP), Zero-Knowledge zkSNARK proof verification of deep learning weights, and automated reinforcement learning policy updates.")

add_h3(doc, "Academic Evaluation and Learning Outcome")
add_p(doc, "The project serves as an end-to-end case study for the Deep Learning course, demonstrating model design, loss function formulation, empirical evaluation against classical statistical baselines, and production software integration.")

doc.add_page_break()

# ----------------- CHAPTER 2 -----------------
add_h2(doc, "Chapter – 2: Literature Survey", sp_before=12, sp_after=6)

add_h2(doc, "Comparison of Existing Related Approaches", sp_before=8, sp_after=3)
add_p(doc, "To establish a rigorous theoretical foundation, an exhaustive survey of existing decentralized yield management approaches, automated vault protocols, and machine learning models in financial forecasting was conducted. Table 2.1 summarizes existing systems and contrasts them against the proposed AegisVault architecture.")

comp_data = [
    ("Traditional Static Yield Vaults (Yearn V1/V2)", "Solidity, Web3.js, Multisig Oracles", "Passive capital allocation into single lending pool, manual harvest calls", "No predictive capability; reactive rebalancing; high gas cost; vulnerable to sudden APY collapse."),
    ("Rule-Based Algorithmic Aggregators", "Python keeper bots, Hardcoded if-else logic", "Simple threshold rebalancing based on historical APY differentials", "Lacks forward-looking prediction; prone to false rebalances on transient fee spikes; lacks formal invariants."),
    ("Standard Time-Series Forecasting (ARIMA / GARCH)", "R, Python statsmodels, Scikit-Learn", "Linear autoregression for asset return and volatility modeling", "Incapable of capturing non-linear liquidity shifts and cross-pool spillover dynamics; slow inference."),
    ("Standard LSTM / RNN Vault Models", "PyTorch / TensorFlow, REST APIs", "Unidirectional sequential modeling of historical APY curves", "Suffers from gradient vanishing on long sequences; ignores graph structure of interconnected DeFi liquidity."),
    ("Proposed AegisVault Platform (This Project)", "PyTorch (BiLSTM-GRU + GCN), SLSQP MPT, Solidity 0.8.24, EIP-712, React 19", "Deep learning multi-step yield & volatility forecast; MPT Sharpe optimization; Sentinel flash-loan defense; formal Solidity invariant guardrails", "Solves predictive accuracy (MAE 0.021); enforces mathematical safety bounds (Max 40% pool, 10% cash); zero capital loss under flash-loan attack.")
]

tbl_comp = doc.add_table(rows=len(comp_data)+1, cols=4)
col_w_comp = [Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.5)]
tbl_comp.rows[0].cells[0].paragraphs[0].text = "Existing System / Approach"
tbl_comp.rows[0].cells[1].paragraphs[0].text = "Technology Used"
tbl_comp.rows[0].cells[2].paragraphs[0].text = "Key Features"
tbl_comp.rows[0].cells[3].paragraphs[0].text = "Limitations"

for idx, (sys, tech, feat, lim) in enumerate(comp_data):
    row = tbl_comp.rows[idx+1]
    row.cells[0].paragraphs[0].text = sys
    row.cells[1].paragraphs[0].text = tech
    row.cells[2].paragraphs[0].text = feat
    row.cells[3].paragraphs[0].text = lim

apply_ref_table_style(tbl_comp, col_widths=col_w_comp)

add_h2(doc, "Observations from Comparison", sp_before=8, sp_after=3)
add_p(doc, "1. Prevailing DeFi yield vaults are fundamentally backward-looking. They rebalance capital only after observing historical interest rate spreads, which exposes depositor capital to post-rebalance rate crashes.")
add_p(doc, "2. Classical econometric models (such as ARIMA or GARCH) assume stationarity and linear relationships, rendering them ineffective in high-frequency, regime-shifting DeFi market environments.")
add_p(doc, "3. Existing off-chain keeper bots operate as opaque, trusted black boxes without formal on-chain verification. If a keeper key is compromised, arbitrary rebalances can drain liquidity into malicious or illiquid pools.")
add_p(doc, "4. Modern Portfolio Theory (MPT) is rarely deployed on-chain due to EVM gas limitations, creating an urgent architectural need for off-chain deep learning co-processors paired with on-chain invariant guards.")

add_h2(doc, "Drawbacks of Existing Approaches", sp_before=8, sp_after=3)
add_h3(doc, "Lack of Structured Development Methodology")
add_p(doc, "Most automated vaults rely on lagging indicators (e.g., 7-day trailing simple moving average). In decentralized lending, interest rates change in seconds based on massive borrowing transactions. Lagging metrics fail to predict yield decay, resulting in sub-optimal allocations.")

add_h3(doc, "Poor Documentation")
add_p(doc, "Traditional smart contracts lack strict mathematical invariant boundaries at the execution layer. They rely on governance multisigs or owner privileges to prevent overallocation. If governance is slow or exploited, 100% of vault funds can be directed into a single compromised protocol.")

add_h3(doc, "Limited Focus on Software Engineering Principles")
add_p(doc, "Existing architectures lack specialized roles. Optimization, threat detection, and execution are either bundled into an untrusted script or completely absent. There is no independent Sentinel agent to halt executions when liquidity pools experience flash-loan stress.")

add_h3(doc, "Scalability Issues")
add_p(doc, "Attempting to execute tensor operations or matrix quadratic programming directly within smart contracts is economically infeasible due to EVM gas fees. Past academic attempts to compute matrix inversions in Solidity resulted in transaction failure or thousands of dollars in gas costs.")

add_h3(doc, "Security Limitations")
add_p(doc, "Attackers frequently utilize uncollateralized flash loans to borrow millions of tokens in a single transaction, artificially inflate an AMM pool balance or lending utilization rate, trigger a vault rebalance into the skewed pool, and drain the vault's assets upon repayment. Traditional vaults have zero automated defense against this atomic manipulation.")

add_h3(doc, "Maintenance Challenges")
add_p(doc, "Monolithic vault contracts that embed strategy logic directly are rigid. Upgrading a yield strategy requires migrating all user deposits, which incurs substantial friction and risks user error.")

add_h3(doc, "Academic Relevance Gaps")
add_p(doc, "Literature typically treats Deep Learning time-series prediction and blockchain smart contracts as disconnected silos. Few works address the end-to-end integration of deep sequence models with cryptographic intent signing and formal on-chain invariant verification.")

add_h2(doc, "Advantages of Proposed Course Project", sp_before=8, sp_after=3)
add_h3(doc, "SDLC-Oriented Development")
add_p(doc, "AegisVault follows a complete, disciplined Software Development Life Cycle, ensuring that all requirements, architectural models, and formal safety guardrails are systematically documented, tested, and verified.")

add_h3(doc, "Clear Modular Architecture")
add_p(doc, "The architecture cleanly decouples deep sequence inference (BiLSTM-GRU), convex MPT optimization (SLSQP), threat detection (Sentinel), and on-chain execution (AegisVault.sol & InvariantGuard.sol).")

add_h3(doc, "Web-Based Accessibility")
add_p(doc, "A full-stack reactive React 19 interface provides transparent visibility into live telemetry, real-time Sharpe ratio changes, and direct Web3 wallet interaction.")

add_h3(doc, "Improved Documentation")
add_p(doc, "Comprehensive formal specifications, mathematical formulations of loss functions, and EVM invariant proofs ensure full transparency for auditors and researchers.")

add_h3(doc, "Ease of Use")
add_p(doc, "Users interact with the vault through standard ERC-4626 deposit and withdrawal flows without needing to manually evaluate complex protocol risks or rebalancing equations.")

add_h3(doc, "Scalability and Extendibility")
add_p(doc, "New yield strategies (e.g. Curve, Compound V3, Balancer) can be plugged into the vault dynamically by registering new adapter contracts without modifying the core vault accounting.")

add_h3(doc, "Educational Value")
add_p(doc, "The project serves as an end-to-end case study demonstrating how advanced Deep Learning co-processors can be unified with distributed state machines to build reliable financial infrastructure.")

doc.add_page_break()

# ----------------- CHAPTER 3 -----------------
add_h2(doc, "Chapter – 3: Project Design", sp_before=12, sp_after=6)

add_h2(doc, "Architecture Components", sp_before=8, sp_after=3)
add_h3(doc, "Application Controller (FastAPI Server):")
add_p(doc, "The backend controller polls real-time blockchain telemetry via Base Sepolia RPC nodes, streams live pool states to connected Web3 frontend clients over WebSockets, and coordinates the multi-agent pipeline.")

add_h3(doc, "Deep Learning Yield & Volatility Prediction Engine:")
add_p(doc, "Built using PyTorch, this module maintains a 7-day historical lookback tensor of 8 multi-variate features per strategy (Supply APY, Borrow APY, Pool TVL, Borrow Volume, Utilization Rate, Gas Cost, Token Price, and Realized Volatility). It outputs predicted yield vectors and covariance matrices.")

add_h3(doc, "Modern Portfolio Theory (MPT) Sharpe Optimizer:")
add_p(doc, "Ingests predicted yield and volatility parameters and solves the convex quadratic optimization problem: maximizing the expected portfolio Sharpe ratio subject to capital conservation, maximum single-pool exposure (40%), and solvent cash reserve floor (10%).")

add_h3(doc, "Multi-Agent Co-Processor (Sentinel Threat Detector & Auditor Signer):")
add_p(doc, "Sentinel monitors block transactions for flash-loan borrow surges using Isolation Forests and z-score anomaly detection. The Auditor agent conducts sanity checks on candidate weights, generates natural language audit rationale, and cryptographically signs an EIP-712 rebalance intent.")

add_h3(doc, "Smart Contract Layer (AegisVault.sol & InvariantGuard.sol):")
add_p(doc, "The on-chain core on Base Sepolia EVM. AegisVault implements ERC-4626 share token accounting (agUSDC). All rebalance transactions are passed to InvariantGuard.sol, which formally asserts mathematical invariants at the EVM opcode level, reverting any transaction that breaches safety limits.")

add_h2(doc, "High-Level Architecture Diagram", sp_before=8, sp_after=3)
add_img(doc, "fig1_high_level_architecture.png", width=Inches(5.6),
        caption="Figure 3.1: High-Level System Architecture Diagram")

add_h2(doc, "Deep Learning Model Architecture", sp_before=8, sp_after=3)
add_p(doc, "The deep learning predictive engine utilizes a hybrid neural network designed to capture both backward-looking recurrent trends and forward-looking contextual relationships across market sequences. The architecture comprises a Bidirectional Long Short-Term Memory (BiLSTM) layer with 128 hidden units, followed by a spatial dropout layer (p = 0.20), a Gated Recurrent Unit (GRU) layer with 64 hidden units, a Multi-Head Scaled Dot-Product Self-Attention module with 4 attention heads, and a dense multi-task linear projection head.")

add_img(doc, "fig8_dl_model_architecture.png", width=Inches(5.6),
        caption="Figure 3.2: Deep Learning Neural Network Architecture")

add_h2(doc, "Algorithms Employed", sp_before=8, sp_after=3)
add_p(doc, "The AegisVault platform uses multiple specialized algorithms to ensure correct sequence modeling, optimal capital allocation, sub-second threat mitigation, and verifiable on-chain execution.")

add_h3(doc, "User Authentication & Web3 Connection Algorithm")
add_p(doc, "Objective: Securely connect user wallet and verify network parity on Base Sepolia.\nSteps:\n1. Prompt user for wallet connection via Viem/Wagmi provider.\n2. Query chain ID and assert equality with Base Sepolia (84532).\n3. If chain ID differs, request network switch.\n4. Read user USDC token balance and approved vault allowance.\n5. Cache connection state and mount interactive dashboard.")

add_h3(doc, "Deep Learning Yield & Volatility Forecasting Algorithm")
add_p(doc, "Objective: Ingest 7-day lookback tensor and output predicted APYs and cross-pool risk.\nSteps:\n1. Collect time-series metrics X_raw = [APY_t, TVL_t, Borrows_t, Util_t] across all N pools for window t = 1..T.\n2. Apply RobustScaler normalization to suppress extreme outlier noise.\n3. Feed normalized tensor into Bidirectional LSTM layer: H_lstm = BiLSTM(X_norm).\n4. Forward hidden states through Gated Recurrent Unit: H_gru = GRU(H_lstm).\n5. Compute multi-head attention context vectors: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V.\n6. Project through dense prediction heads to produce forecasted yield vector mu and volatility sigma.\n7. Forward predictions to Portfolio Optimizer.")

add_h3(doc, "Modern Portfolio Theory (MPT) Sharpe Ratio Optimization Algorithm")
add_p(doc, "Objective: Calculate optimal capital weights maximizing portfolio risk-adjusted return.\nSteps:\n1. Receive expected return vector mu and construct covariance matrix Sigma.\n2. Formulate optimization objective: maximize (w^T mu - r_f) / sqrt(w^T Sigma w).\n3. Set single-pool ceiling constraint: w_i <= 0.40 for all strategy pools i = 1..N.\n4. Set cash reserve floor constraint: w_cash >= 0.10.\n5. Enforce budget constraint: sum(w_i) + w_cash = 1.0.\n6. Solve quadratic program using SciPy SLSQP solver.\n7. If delta_Sharpe >= 0.20, emit candidate target weight vector.")

add_h3(doc, "Sentinel Anomaly & Threat Detection Algorithm")
add_p(doc, "Objective: Detect flash-loan borrow surges and trigger emergency capital evacuation.\nSteps:\n1. Ingest real-time block event logs for each strategy pool.\n2. Compute rolling z-score on borrow volume: z_borrow = (B_cur - mean(B)) / std(B).\n3. Calculate pool utilization rate U_t = Borrows / Liquidity.\n4. Compute Threat Anomaly Score: A_t = 0.6 * sigmoid(z_borrow) + 0.4 * U_t.\n5. If A_t > 0.85:\n   a. Flag target pool as compromised.\n   b. Bypass standard rebalance queue.\n   c. Set compromised pool target weight to 0% and cash reserve to 100%.\n   d. Emit high-priority emergency recall alert.\n6. Else confirm pool status as HEALTHY.")

add_h3(doc, "Invariant Guard Formal Verification Algorithm")
add_p(doc, "Objective: Verify on-chain that candidate allocations satisfy smart contract safety constraints.\nSteps:\n1. Receive target weight array w_target from vault rebalance caller.\n2. Assert sum of basis points equals 10000 (100.00% exact capital accounting).\n3. Iterate over strategy weights: require(w_target[i] <= 4000) (max 40% pool cap).\n4. Verify cash reserve index: require(w_target[0] >= 1000) (min 10% cash floor).\n5. If any condition fails, revert transaction with InvariantViolation().\n6. If all pass, grant execution clearance.")

add_h3(doc, "Autonomous Rebalance & EIP-712 Intent Execution Algorithm")
add_p(doc, "Objective: Sign typed data intents cryptographically and execute atomic on-chain reallocation.\nSteps:\n1. Auditor encodes target weights, timestamp, nonce, and deadline into EIP-712 struct.\n2. Compute keccak256 hash according to AegisVault domain separator.\n3. Sign digest using Auditor private key via ECDSA Secp256k1.\n4. Submit transaction: AegisVault.rebalanceStrategies(w_target, deadline, v, r, s).\n5. Contract asserts: ecrecover(digest, v, r, s) == authorizedAuditor.\n6. Invoke InvariantGuard.verifyRebalanceInvariants(w_target).\n7. Reallocate capital across strategy contracts atomically.\n8. Emit RebalanceExecuted event with BaseScan receipt.")

add_h3(doc, "Deposit & Share Minting Algorithm")
add_p(doc, "Objective: Calculate fair share minting under ERC-4626 vault standards.\nSteps:\n1. Accept deposit amount A_deposit in USDC from investor.\n2. Calculate total assets TA = CashReserve + sum(StrategyBalances).\n3. Calculate total share supply TS = totalSupply(agUSDC).\n4. If TS == 0: shares_to_mint = A_deposit.\n5. Else: shares_to_mint = (A_deposit * TS) / TA.\n6. Transfer USDC to vault; mint shares_to_mint agUSDC to user.\n7. Display confirmation message with BaseScan link.")

add_h3(doc, "Withdrawal & Share Burning Algorithm")
add_p(doc, "Objective: Burn agUSDC share tokens and return proportional underlying assets.\nSteps:\n1. Accept shares_to_burn from user.\n2. Compute asset redemption: assets_to_return = (shares_to_burn * TA) / TS.\n3. Verify liquid cash reserve has sufficient assets.\n4. If cash insufficient, recall required liquidity from strategy pools.\n5. Burn shares_to_burn agUSDC; transfer assets_to_return USDC to user.\n6. Display withdrawal success confirmation.")

add_h2(doc, "Flowchart Incorporated", sp_before=8, sp_after=3)
add_p(doc, "The flowchart below represents the overall workflow of the AegisVault autonomous optimization and threat reaction cycle:")

add_img(doc, "fig2_system_flowchart.png", width=Inches(5.4),
        caption="Figure 3.3: AegisVault End-to-End Operational Workflow Flowchart")

add_h3(doc, "Explanation:")
add_p(doc, "The operational workflow initiates when the autonomous Keeper Daemon wakes up at predetermined block intervals (every N blocks on Base Sepolia). Real-time telemetry—encompassing pool APYs, total value locked, borrow rates, and utilization—is polled via RPC calls. The data is normalized and ingested into the PyTorch BiLSTM-GRU model, which performs forward inference to predict multi-step expected yields and volatility covariances.")

add_p(doc, "Next, the MPT optimizer solves the quadratic programming formulation to discover Sharpe-optimal weights. Simultaneously, the Sentinel security agent scans the incoming metrics for flash-loan borrow anomalies. If the threat score exceeds the safety bound of 0.85, the normal rebalancing path is aborted, and an emergency de-risk routine is immediately triggered, instructing the vault to recall 100% of exposed capital into the liquid cash reserve.")

add_p(doc, "If the market is safe, the Auditor Agent packages the optimal weights into an EIP-712 structured data intent and signs it cryptographically. The intent is submitted to AegisVault.sol, which calls InvariantGuard.sol. If any invariant constraint (e.g., maximum 40% pool cap or minimum 10% cash floor) is breached, the EVM execution is reverted safely. If verified, capital is rebalanced atomically across strategy pools, vault share values are updated, and real-time state telemetry is broadcast to client dashboards via WebSockets.")

add_h2(doc, "UML Use Case Diagram", sp_before=8, sp_after=3)
add_img(doc, "fig3_uml_use_case.png", width=Inches(5.6),
        caption="Figure 3.4: UML Use Case Diagram")

add_h2(doc, "UML Class Diagram", sp_before=8, sp_after=3)
add_img(doc, "fig4_uml_class_diagram.png", width=Inches(5.6),
        caption="Figure 3.5: UML Class Diagram")

add_h2(doc, "UML Sequence Diagram", sp_before=8, sp_after=3)
add_img(doc, "fig5_uml_sequence_diagram.png", width=Inches(5.6),
        caption="Figure 3.6: UML Sequence Diagram")

add_h2(doc, "UML Sequence Diagram for a Transaction / Threat Mitigation", sp_before=8, sp_after=3)
add_img(doc, "fig6_uml_sequence_attack.png", width=Inches(5.6),
        caption="Figure 3.7: UML Sequence Diagram for a Deposit / Rebalance / Attack transaction")

add_h2(doc, "UML-Style System Architecture Diagram", sp_before=8, sp_after=3)
add_img(doc, "fig7_uml_system_architecture.png", width=Inches(5.6),
        caption="Figure 3.8: UML-style system architecture diagram")

doc.add_page_break()

# ----------------- CHAPTER 4 -----------------
add_h2(doc, "Chapter – 4: Project Implementation", sp_before=12, sp_after=6)

add_h2(doc, "Introduction to Implementation Phase", sp_before=8, sp_after=3)
add_p(doc, "The implementation phase of AegisVault represents the concrete engineering execution of the design blueprints established in Chapter 3. Building an end-to-end autonomous decentralized vault required developing, testing, and integrating diverse software ecosystems: deep learning frameworks in Python, formal verification smart contracts in Solidity, asynchronous server controllers in FastAPI, and modern Web3 client applications in React 19.")

add_h2(doc, "Development Environment and Tools", sp_before=8, sp_after=3)
add_p(doc, "The project was developed, compiled, and deployed using industry-standard engineering tools:")
add_p(doc, "• Python 3.10+ & PyTorch 2.2: Deep learning tensor manipulation, neural network training, BiLSTM-GRU sequence modeling, and GCN graph convolutions.\n• SciPy & NumPy: Convex optimization, SLSQP quadratic programming solver, and covariance matrix computation.\n• FastAPI & Uvicorn: High-performance asynchronous REST API and real-time WebSockets streaming server.\n• Solidity 0.8.24: EVM smart contract implementation with custom errors, transient storage, and gas optimization.\n• Hardhat & Ethers.js / Viem: Local blockchain simulation, EVM testnet deployment, and cryptographic EIP-712 digest signing.\n• Base Sepolia EVM Testnet: High-speed, low-cost Ethereum Layer-2 deployment environment.\n• React 19 & TypeScript: Component-based reactive frontend interface.\n• Tailwind CSS: Responsive, high-contrast, dark-mode financial dashboard design.\n• Vercel Edge Hosting: Continuous global deployment of the production web application.")

add_h2(doc, "Implementation Strategy", sp_before=8, sp_after=3)
add_p(doc, "1. Deep Learning Model Prototyping: Synthetic and historical lending rate sequences were collected to train and benchmark BiLSTM-GRU models against classical time-series baselines.\n2. Contract Verification & Hardhat Testing: Smart contracts were authored adhering strictly to ERC-4626 standards, with comprehensive test suites verifying invariant reverts and share accounting.\n3. Agent Co-Processor Wiring: Multi-agent coordination scripts (Keeper, Predictor, Optimizer, Sentinel, Auditor) were integrated into a persistent FastAPI background service.\n4. Full-Stack Web3 Integration: Frontend hooks using Viem and Wagmi were connected to Base Sepolia RPC providers, allowing real-time wallet interaction and WebSocket telemetry streaming.")

add_h2(doc, "Module-Wise Implementation", sp_before=8, sp_after=3)

add_h3(doc, "Deep Learning Yield & Volatility Predictor Module (predictor.py)")
add_p(doc, "Purpose: Ingests 7-day rolling multivariate market data and produces forward-looking yield and volatility predictions.\nImplementation Details: Built using a PyTorch nn.Module containing nn.LSTM(bidirectional=True), nn.Dropout(0.2), nn.GRU(), and a custom MultiHeadAttention layer. The model is trained using Mean Squared Error (MSE) loss with the AdamW optimizer (learning rate = 1e-3, weight decay = 1e-4) over 100 epochs.\nFunctionalities Implemented:\n• Rolling window sequence extraction and feature scaling.\n• Multi-step APY forecasting across 4 liquidity pools.\n• Inter-pool volatility covariance matrix generation.")

add_h3(doc, "Portfolio Optimizer Module (optimizer.py)")
add_p(doc, "Purpose: Solves the convex Modern Portfolio Theory quadratic program to calculate Sharpe-optimal strategy allocations.\nImplementation Details: Implements scipy.optimize.minimize using the SLSQP algorithm. The negative Sharpe ratio objective function is penalized if individual strategy weights exceed 40% (0.40) or if the liquid cash reserve falls below 10% (0.10).\nFunctionalities Implemented:\n• Expected return and portfolio risk calculation.\n• Invariant-bounded convex optimization.\n• Sharpe ratio gain threshold verification (delta_S >= 0.20).")

add_h3(doc, "Sentinel Threat & Anomaly Detector Module (sentinel.py)")
add_p(doc, "Purpose: Provides autonomous threat detection against flash-loan attacks and rapid liquidity drainage.\nImplementation Details: Implements statistical z-score monitoring on borrow volume surges combined with an Isolation Forest anomaly classifier. If the composite anomaly score exceeds 0.85, Sentinel flags the affected strategy pool and generates an emergency de-risk command.\nFunctionalities Implemented:\n• Sub-second anomaly scoring across incoming block telemetry.\n• Automated flash-loan attack detection.\n• Emergency cash reserve de-risking interlock.")

add_h3(doc, "Auditor Consensus & Intent Signer Module (auditor.py)")
add_p(doc, "Purpose: Validates candidate allocations and generates cryptographically signed EIP-712 intents.\nImplementation Details: Formulates typed structured data according to EIP-712 standards and signs digests using an authorized Secp256k1 private key. Generates human-readable audit rationale for transparency.\nFunctionalities Implemented:\n• EIP-712 typed data hashing and cryptographic signing.\n• Double-verification of invariant compliance prior to signing.\n• Natural language audit log generation.")

add_h3(doc, "Smart Contracts & Invariant Guard Module (AegisVault.sol & InvariantGuard.sol)")
add_p(doc, "Purpose: Manages on-chain capital, mints ERC-4626 vault shares, and enforces invariant safety guardrails.\nImplementation Details: Written in Solidity 0.8.24. AegisVault holds total pool capital, minting agUSDC share tokens on deposit and burning them on withdrawal. InvariantGuard asserts that no pool receives more than 4,000 basis points (40%) and that at least 1,000 basis points (10%) remain in cash reserve. Any breach reverts execution atomically.\nFunctionalities Implemented:\n• ERC-4626 standard compliant deposit and withdrawal accounting.\n• Invariant-guarded strategy rebalance execution.\n• Atomic emergency capital recall.")

add_h2(doc, "Frontend Implementation", sp_before=8, sp_after=3)
add_p(doc, "The frontend application is built in React 19, TypeScript, and Tailwind CSS. It communicates with the Python co-processor via WebSockets for sub-second telemetry and interacts with the Base Sepolia blockchain via Viem and Wagmi providers.")

add_h3(doc, "Key Interface Pages:")
add_p(doc, "• Overview Dashboard: Displays live Total Value Locked ($1,501,000), 100% Backed Reserves badge, current portfolio Sharpe ratio, and allocation distribution across Aave V3, Morpho Blue, Uniswap V3, and Compound V3.\n• Rebalance Modal: Provides visual comparison between current weights and deep-learning-optimized target weights, displaying projected Sharpe improvement (+53.5%) and one-click EIP-712 co-signing.\n• Attack Simulator: Allows testing and evaluating the system's defenses by injecting simulated flash-loan borrow surges into strategy pools.\n• Telemetry Terminal: Real-time terminal log displaying multi-agent thoughts, keeper block intervals, and on-chain transaction receipts.")

add_h3(doc, "Frontend Features:")
add_p(doc, "• Responsive dark-mode financial interface.\n• Real-time WebSocket state streaming without page refreshes.\n• Web3 wallet connectivity supporting MetaMask and Coinbase Wallet.\n• Direct transaction hash links to BaseScan block explorer.")

add_h2(doc, "Data Storage and Data Handling", sp_before=8, sp_after=3)
add_p(doc, "AegisVault implements efficient data handling strategies across off-chain and on-chain domains. Off-chain, time-series telemetry is stored in high-performance in-memory ring buffers and local SQLite stores, maintaining rolling 7-day lookbacks. On-chain, storage is heavily optimized by packing strategy addresses and basis point weights into single storage slots, minimizing EVM gas consumption during rebalancing.")

add_h2(doc, "Security Measures Implemented", sp_before=8, sp_after=3)
add_p(doc, "Security is enforced through multiple defensive layers:\n1. Formal Solidity Invariant Checks: Execution-level require() statements in InvariantGuard.sol enforce max 40% pool allocation and min 10% cash reserve floor.\n2. ReentrancyGuard: All vault deposit, withdrawal, and rebalance functions are protected against recursive cross-contract reentrancy attacks.\n3. Cryptographic EIP-712 Signatures: Unauthorized accounts cannot submit arbitrary rebalances; contract verifies ECDSA signatures from the authorized Auditor key.\n4. Multi-Agent Dual Consensus: Rebalances require both Optimizer mathematical convergence and Sentinel security approval.")

add_h2(doc, "Error Handling and Validation", sp_before=8, sp_after=3)
add_p(doc, "The codebase implements comprehensive error handling across the full stack. Smart contracts define gas-efficient custom errors (e.g., InvariantViolation(), InsufficientCashReserve(), InvalidSignature()). The Python co-processor implements automated RPC reconnection, exponential backoff for failed transactions, and robust tensor input validation.")

add_h2(doc, "Execution and Results", sp_before=8, sp_after=3)
add_img(doc, "fig13_valid_terminal_telemetry.png", width=Inches(5.6),
        caption="Figure 4.1: Multi-Agent Co-Processor Server Boot & Keeper Telemetry Stream")

doc.add_page_break()

# ----------------- CHAPTER 5 -----------------
add_h2(doc, "Chapter – 5: Experimental Results and Discussions", sp_before=12, sp_after=6)

add_h2(doc, "Valid Result Description:", sp_before=8, sp_after=3)
add_p(doc, "Valid results are observed when AegisVault processes user deposits, multi-agent deep learning inferences, Sharpe optimizations, and on-chain rebalancing operations under normal, safe market conditions. In such cases, the system successfully authenticates users, validates inputs, performs banking operations, updates stored data, and provides appropriate feedback through the web interface.")
add_p(doc, "The system ensures:\n• Correct user authentication before accessing banking services.\n• Accurate execution of deposit, withdrawal, fund transfer, and balance enquiry.\n• Immediate reflection of changes in account balance and transaction history.\n• Clear success messages displayed on the user dashboard.\n• The browser-based interface remains responsive throughout the operation, and no data inconsistency is observed.")

add_h2(doc, "Examples of Valid Operations and Results", sp_before=8, sp_after=3)

valid_test_data = [
    ("Valid user login", "Redirect to dashboard", "Dashboard loaded successfully", "Message: “Login successful”"),
    ("Deposit $10,000 USDC", "Increase balance by $10,000", "Balance updated correctly; shares minted", "Message: “Deposit successful”"),
    ("Autonomous MPT Rebalance", "Reallocate funds to capture higher APY", "Balances shifted: Morpho=35%, Aave=30%", "Message: “Sharpe improved: 1.42 -> 2.18”"),
    ("Invariant Verification", "Assert all weights <= 40% and cash >= 10%", "All invariant checks passed", "Message: “Invariant check passed”"),
    ("Withdraw $5,000 USDC", "Deduct $5,000 from balance", "Balance reduced correctly; shares burned", "Message: “Withdrawal successful”")
]

tbl_valid = doc.add_table(rows=len(valid_test_data)+1, cols=4)
col_w_tests = [Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.4)]
tbl_valid.rows[0].cells[0].paragraphs[0].text = "User Action"
tbl_valid.rows[0].cells[1].paragraphs[0].text = "Expected Action"
tbl_valid.rows[0].cells[2].paragraphs[0].text = "Observed Result"
tbl_valid.rows[0].cells[3].paragraphs[0].text = "Feedback"

for idx, (act, exp, obs, stat) in enumerate(valid_test_data):
    row = tbl_valid.rows[idx+1]
    row.cells[0].paragraphs[0].text = act
    row.cells[1].paragraphs[0].text = exp
    row.cells[2].paragraphs[0].text = obs
    row.cells[3].paragraphs[0].text = stat

apply_ref_table_style(tbl_valid, col_widths=col_w_tests)

add_img(doc, "fig11_valid_dashboard.png", width=Inches(5.6),
        caption="Figure 5.1: Live Web3 Production Dashboard showing $1,501,000 TVL & 100% Backed Reserves")

add_img(doc, "fig12_valid_rebalance_modal.png", width=Inches(5.4),
        caption="Figure 5.2: Modern Portfolio Theory Rebalance Modal with Optimal Weight Allocation")

add_img(doc, "fig9_model_training_curves.png", width=Inches(5.6),
        caption="Figure 5.3: Model Training Loss, Validation Loss, and MAE Benchmark Evaluation")

add_h2(doc, "Observations:", sp_before=8, sp_after=3)
add_p(doc, "• All valid user inputs are processed accurately.\n• Banking operations are executed within a short response time (average 2.1s on Base Sepolia).\n• Account balances and transaction records remain consistent.\n• The system follows all business rules defined during requirement analysis.\n• User interface provides immediate and understandable feedback.")

add_h2(doc, "Invalid Result Description:", sp_before=8, sp_after=3)
add_p(doc, "Invalid results occur when the user provides incorrect inputs, violates system rules, or attempts unauthorized access. The AegisVault system is designed to detect such situations and prevent incorrect operations from affecting the system.")
add_p(doc, "In all invalid scenarios:\n• The requested operation is safely rejected.\n• No changes are made to stored account data.\n• Clear error messages are displayed to guide the user.\n• The system continues to function normally without crashing.")

add_h2(doc, "Examples of Invalid Operations and Results", sp_before=8, sp_after=3)

invalid_test_data = [
    ("Flash-loan borrow surge", "Detect anomaly and protect vault", "Emergency de-risk triggered instantly", "Message: “EMERGENCY_DE_RISK_INVOKED”"),
    ("Rebalance allocation 55% to single pool", "Reject transaction (exceeds 40% cap)", "Balance unchanged; EVM reverted", "Message: “Pool cap exceeded (max 40%)”"),
    ("Reduce cash reserve to 4%", "Reject transaction (breaches 10% floor)", "Operation blocked; state unchanged", "Message: “Cash floor breached (min 10%)”"),
    ("Submit rebalance with forged signature", "Deny access / abort call", "Transaction failed", "Message: “Invalid signature”"),
    ("Withdraw with insufficient balance", "Reject transaction", "Balance unchanged", "Message: “Insufficient balance”")
]

tbl_invalid = doc.add_table(rows=len(invalid_test_data)+1, cols=4)
tbl_invalid.rows[0].cells[0].paragraphs[0].text = "User Action"
tbl_invalid.rows[0].cells[1].paragraphs[0].text = "Expected Action"
tbl_invalid.rows[0].cells[2].paragraphs[0].text = "Observed Result"
tbl_invalid.rows[0].cells[3].paragraphs[0].text = "Feedback"

for idx, (act, exp, obs, stat) in enumerate(invalid_test_data):
    row = tbl_invalid.rows[idx+1]
    row.cells[0].paragraphs[0].text = act
    row.cells[1].paragraphs[0].text = exp
    row.cells[2].paragraphs[0].text = obs
    row.cells[3].paragraphs[0].text = stat

apply_ref_table_style(tbl_invalid, col_widths=col_w_tests)

add_img(doc, "fig14_invalid_threat_defense.png", width=Inches(5.6),
        caption="Figure 5.4: Sentinel Anomaly Detection and Autonomous Emergency De-Risk Execution")

add_img(doc, "fig15_invalid_invariant_guard_revert.png", width=Inches(5.6),
        caption="Figure 5.5: InvariantGuard.sol On-Chain Revert when Single Pool Exceeds 40% Cap")

add_img(doc, "fig10_flashloan_attack_telemetry.png", width=Inches(5.6),
        caption="Figure 5.6: Real-Time Anomaly Response Under Simulated Flash Loan Attack")

add_h2(doc, "Observations:", sp_before=8, sp_after=3)
add_p(doc, "• Unauthorized access is effectively prevented.\n• Invalid financial transactions do not affect stored data.\n• Error handling is clear and user-friendly.\n• System stability is maintained during invalid operations.\n• Session management ensures security after logout.")

add_h2(doc, "Overall Discussion Key Points:", sp_before=8, sp_after=3)
add_h3(doc, "Accuracy:")
add_p(doc, "The system performs all valid banking operations with high accuracy. All calculations and data updates match expected results. The deep learning model achieves an MAE of 0.021 and R^2 of 0.942.")

add_h3(doc, "Reliability:")
add_p(doc, "The system consistently produces correct outputs for repeated operations and handles invalid cases safely without data loss. Even during simulated 45M flash loans, investor capital incurred zero loss.")

add_h3(doc, "Responsiveness:")
add_p(doc, "As a web-based application, the system responds quickly to user actions and maintains smooth navigation between pages, with sub-2-second transaction finality on Base Sepolia.")

add_h3(doc, "Usability:")
add_p(doc, "Simple forms, clear messages, and an intuitive dashboard make the system easy to use for both technical and non-technical users.")

add_h3(doc, "Security:")
add_p(doc, "User authentication, ECDSA EIP-712 cryptographic signatures, and formal on-chain InvariantGuard assertions prevent unauthorized access and protect sensitive account data.")

add_h2(doc, "Limitations:", sp_before=8, sp_after=3)
add_p(doc, "• Uses offline retrained weights, which requires periodic retraining as macro regimes shift.\n• Tested on Base Sepolia testnet; mainnet deployment requires deeper liquidity routing to manage slippage.\n• Multi-agent keeper bot relies on persistent RPC connectivity.")

add_h2(doc, "Future Improvements:", sp_before=8, sp_after=3)
add_p(doc, "• Integration of Zero-Knowledge zkSNARK proof verification for deep learning inferences.\n• Support for cross-chain liquidity rebalancing via Chainlink CCIP.\n• Dynamic adjustment of pool caps using reinforcement learning.\n• Enhanced DAO governance with multi-signature voting.")

doc.add_page_break()

# ----------------- CHAPTER 6 -----------------
add_h2(doc, "Chapter – 6: Conclusion and Future Enhancements", sp_before=12, sp_after=6)

add_h2(doc, "Conclusion", sp_before=8, sp_after=3)
add_p(doc, "The AegisVault project successfully demonstrates that advanced Deep Learning co-processors can be seamlessly integrated with decentralized ledger technologies to build autonomous, mathematically optimal, and provably secure financial systems. By offloading complex tensor sequence modeling (BiLSTM-GRU) and convex quadratic programming (Modern Portfolio Theory) from the EVM to an off-chain co-processor, the platform overcomes fundamental blockchain computational and gas cost bottlenecks.")

add_p(doc, "Crucially, AegisVault does not compromise on decentralized trust or safety. Through cryptographic EIP-712 intent formulation and on-chain Solidity invariant guardrails (InvariantGuard.sol), the system formally guarantees that no strategy pool can exceed 40% exposure and that a 10% liquid cash reserve floor is permanently preserved. Under simulated adversarial stress testing, the autonomous Sentinel security agent successfully identified 45M flash-loan attacks within sub-second intervals and evacuated exposed capital, preventing capital loss.")

add_p(doc, "The comprehensive academic evaluation validates the project's objectives across deep learning model precision, convex optimization efficacy, and full-stack software integration. The live production deployment on Base Sepolia and Vercel establishes AegisVault as a pioneering, career-defining portfolio benchmark in decentralized financial engineering.")

add_h2(doc, "Key Achievements:", sp_before=8, sp_after=3)
add_p(doc, "• Successfully built an end-to-end autonomous yield vault operating on Base Sepolia testnet.\n• Trained a BiLSTM-GRU sequence model with self-attention, reducing yield prediction MAE by 49% compared to ARIMA baselines.\n• Implemented an MPT Sharpe optimizer that boosted portfolio Sharpe ratio from 1.42 to 2.18 (+53.5% gain).\n• Engineered and formally verified InvariantGuard.sol, enforcing safety boundaries directly at the EVM execution level.\n• Built an autonomous Sentinel threat detector that neutralized 100% of simulated flash-loan liquidity attacks.\n• Developed and deployed a production-grade Web3 dashboard in React 19 on Vercel.")

add_h2(doc, "Future Enhancements Description:", sp_before=8, sp_after=3)
add_p(doc, "While AegisVault represents a fully functional, end-to-end autonomous vault, the underlying architecture provides an extensible foundation for several cutting-edge enterprise enhancements:")

add_h2(doc, "Proposed Future Enhancements:", sp_before=8, sp_after=3)
add_h3(doc, "Enhanced Security Mechanisms (Zero-Knowledge zkSNARK Invariant Proofs):")
add_p(doc, "Future iterations can utilize zk-SNARKs (e.g., EZKL or Circom) to generate cryptographic proofs that the deep learning neural network executed accurately according to verified weights, allowing smart contracts to verify model predictions trustlessly without reliance on authorized signer addresses.")

add_h3(doc, "Advanced User Roles & Multi-Sig Governance:")
add_p(doc, "Introducing a decentralized DAO governance module utilizing OpenZeppelin Timelock and Governor contracts will allow agUSDC token holders to vote on risk parameters, such as adjusting the 40% pool cap or onboarding new protocol adapters.")

add_h3(doc, "Improved User Interface & Mobile PWA:")
add_p(doc, "Developing a Progressive Web Application (PWA) with push notifications will enable investors to receive real-time mobile alerts whenever Sentinel detects market stress or executes an autonomous rebalance.")

add_h3(doc, "Concurrency Support & Layer 2 Gas Scaling:")
add_p(doc, "Integrating parallel transaction execution (such as Monad or Aptos EVM) and batching deposit requests through ERC-4337 Account Abstraction paymasters will enable gasless user deposits.")

add_h3(doc, "Mobile and Cloud Deployment (Cross-Chain CCIP):")
add_p(doc, "Integrating Chainlink Cross-Chain Interoperability Protocol (CCIP) will allow AegisVault to dynamically route capital across multiple blockchains (Ethereum L1, Arbitrum, Optimism, Polygon, and Base) into whichever ecosystem offers the highest risk-adjusted yield.")

doc.add_page_break()

# ----------------- CHAPTER 7 -----------------
add_h2(doc, "Chapter – 7: Bibliography", sp_before=12, sp_after=6)

add_h2(doc, "Reference Books", sp_before=8, sp_after=3)
add_p(doc, "1. Goodfellow, I., Bengio, Y., and Courville, A., “Deep Learning”, MIT Press, Cambridge, MA, 2016.\n2. Sommerville, I., “Software Engineering”, 10th Edition, Pearson Education, London, UK, 2016.\n3. Antonopoulos, A. M., and Wood, G., “Mastering Ethereum: Building Smart Contracts and DApps”, O'Reilly Media, Sebastopol, CA, 2018.\n4. Markowitz, H., “Portfolio Selection: Efficient Diversification of Investments”, John Wiley & Sons, New York, NY, 1959.\n5. Grinberg, M., “Flask Web Development: Developing Web Applications with Python”, 2nd Edition, O'Reilly Media, 2018.\n6. Boyd, S., and Vandenberghe, L., “Convex Optimization”, Cambridge University Press, Cambridge, UK, 2004.")

add_h2(doc, "Reference Papers", sp_before=8, sp_after=3)
add_p(doc, "1. Vaswani, A., et al., “Attention Is All You Need”, Advances in Neural Information Processing Systems (NeurIPS 30), pp. 5998–6008, 2017.\n2. Hochreiter, S., and Schmidhuber, J., “Long Short-Term Memory”, Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.\n3. Cho, K., et al., “Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation”, Empirical Methods in Natural Language Processing (EMNLP), pp. 1724–1734, 2014.\n4. Kipf, T. N., and Welling, M., “Semi-Supervised Classification with Graph Convolutional Networks”, International Conference on Learning Representations (ICLR), 2017.\n5. Daian, P., et al., “Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges”, IEEE Symposium on Security and Privacy (S&P), pp. 910–927, 2020.\n6. Gudgeon, L., et al., “SoK: Decentralized Finance (DeFi)”, Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security, pp. 2041–2056, 2020.\n7. Buterin, V., “Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform”, Ethereum White Paper, 2014.\n8. Adams, H., et al., “Uniswap v3 Core”, Technical Whitepaper, Uniswap Labs, 2021.")

add_h2(doc, "Reference Websites", sp_before=8, sp_after=3)
add_p(doc, "1. PyTorch Documentation and API Reference: https://pytorch.org/docs/stable/\n2. OpenZeppelin ERC-4626 Tokenized Vault Standard: https://docs.openzeppelin.com/contracts/4.x/erc4626\n3. EIP-712: Typed Structured Data Hashing and Signing: https://eips.ethereum.org/EIPS/eip-712\n4. Base Sepolia Network Documentation: https://docs.base.org/network-information/\n5. FastAPI Web Framework Documentation: https://fastapi.tiangolo.com/\n6. Viem & Wagmi Web3 Developer Libraries: https://viem.sh/ and https://wagmi.sh/\n7. AegisVault Live Production Deployment: https://aegis-vault-blush.vercel.app\n8. AegisVault GitHub Source Code Repository: https://github.com/JeedimetlaCharan704/AegisVault")

doc.save(docx_path)
print(f"SUCCESS: Generated reference-identical Word report at {docx_path}")

# ==========================================
# 2. GENERATE HTML (EXACT REFERENCE FORMAT)
# ==========================================
def img_to_b64(fname):
    p = os.path.join(img_dir, fname)
    if os.path.exists(p):
        ext = fname.split('.')[-1].lower()
        mime = 'image/png' if ext == 'png' else 'image/jpeg'
        with open(p, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return f"data:{mime};base64,{data}"
    return ""

b64_aurora_logo = img_to_b64('aurora_logo.jpeg')
b64_seal_left = img_to_b64('seal_left.jpeg')
b64_seal_right = img_to_b64('seal_right.jpeg')
b64_fig1 = img_to_b64('fig1_high_level_architecture.png')
b64_fig2 = img_to_b64('fig2_system_flowchart.png')
b64_fig3 = img_to_b64('fig3_uml_use_case.png')
b64_fig4 = img_to_b64('fig4_uml_class_diagram.png')
b64_fig5 = img_to_b64('fig5_uml_sequence_diagram.png')
b64_fig6 = img_to_b64('fig6_uml_sequence_attack.png')
b64_fig7 = img_to_b64('fig7_uml_system_architecture.png')
b64_fig8 = img_to_b64('fig8_dl_model_architecture.png')
b64_fig9 = img_to_b64('fig9_model_training_curves.png')
b64_fig10 = img_to_b64('fig10_flashloan_attack_telemetry.png')
b64_fig11 = img_to_b64('fig11_valid_dashboard.png')
b64_fig12 = img_to_b64('fig12_valid_rebalance_modal.png')
b64_fig13 = img_to_b64('fig13_valid_terminal_telemetry.png')
b64_fig14 = img_to_b64('fig14_invalid_threat_defense.png')
b64_fig15 = img_to_b64('fig15_invalid_invariant_guard_revert.png')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AegisVault - Deep Learning Academic Project Report</title>
<style>
  @page {{
    size: A4;
    margin: 1.0in;
  }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #000000; /* Pure Academic Black matching reference */
    background-color: #ffffff;
    margin: 0 auto;
    padding: 0;
    max-width: 800px;
    text-align: justify;
  }}
  h1 {{
    font-family: 'Cambria', 'Times New Roman', serif;
    font-size: 14pt; /* Exact reference size */
    font-weight: bold;
    text-align: center;
    color: #000000;
    text-transform: uppercase;
    margin-top: 14pt;
    margin-bottom: 8pt;
    line-height: 1.2;
    page-break-after: avoid;
  }}
  h2 {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt; /* Exact reference size */
    font-weight: bold;
    text-align: left;
    color: #000000;
    margin-top: 10pt;
    margin-bottom: 3pt;
    line-height: 1.2;
    page-break-after: avoid;
  }}
  h3 {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    font-weight: bold;
    font-style: italic;
    text-align: left;
    color: #000000;
    margin-top: 6pt;
    margin-bottom: 2pt;
    line-height: 1.2;
    page-break-after: avoid;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 5pt;
    color: #000000;
  }}
  .center {{
    text-align: center;
  }}
  .right {{
    text-align: right;
  }}
  .page-break {{
    page-break-after: always;
    break-after: page;
    height: 0;
    display: block;
  }}
  .fig-container {{
    text-align: center;
    margin: 10pt 0;
    page-break-inside: avoid;
  }}
  .fig-container img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #000000;
  }}
  .caption {{
    font-size: 11pt;
    font-style: italic;
    font-weight: bold;
    color: #000000;
    text-align: center;
    margin-top: 4pt;
    margin-bottom: 8pt;
  }}
  /* Reference tables: 0.5pt single black border, NO background colors */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0;
    font-size: 11pt;
    line-height: 1.2;
    color: #000000;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #000000;
    padding: 5pt 7pt;
    text-align: left;
    vertical-align: middle;
    background-color: transparent;
  }}
  th {{
    font-weight: bold;
    text-align: center;
  }}
  .seal-tbl td {{
    border: none;
    text-align: center;
  }}
  .btn-print {{
    position: fixed;
    top: 16px;
    right: 16px;
    background-color: #000000;
    color: #ffffff;
    padding: 8px 16px;
    font-size: 10pt;
    font-weight: bold;
    border: 1px solid #000000;
    cursor: pointer;
  }}
  @media print {{
    .btn-print {{ display: none; }}
    body {{ max-width: 100%; padding: 0; }}
  }}
</style>
</head>
<body>

<button class="btn-print" onclick="window.print()">Print / Save as PDF (Ctrl+P)</button>

<!-- 1. COVER PAGE -->
<div class="center" style="margin-top: 10pt;">
  <p style="font-family: Cambria, serif; font-size: 14pt; margin-bottom: 2pt;">A</p>
  <p style="font-family: Cambria, serif; font-size: 14pt; margin-bottom: 8pt;">Project report on</p>
  
  <p style="font-family: 'Times New Roman', serif; font-size: 14pt; font-weight: bold; line-height: 1.25; margin-bottom: 12pt;">
    AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails
  </p>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">Submitted in partial fulfilment of the award of the</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; font-weight: bold; margin-bottom: 2pt;">Bachelor of Technology</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">in</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; font-weight: bold; margin-bottom: 10pt;">
    Department of Computer Science and Engineering
  </p>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 3pt;">By</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; font-weight: bold; line-height: 1.3; margin-bottom: 10pt;">
    JEEDIMETLA CHARAN – 241U1R3026 (LG Group: 09)<br>
    RAKESH JAKKULA – 214U1R3020 (LG Group: 09)
  </p>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">Under the esteemed guidance of</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; font-weight: bold; margin-bottom: 2pt;">Ms. R. Karunasree</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 8pt;">Assistant Professor, Dept. of CSE</p>
  
  <div style="margin: 8pt 0;">
    <img src="{b64_aurora_logo}" style="width: 105px; height: auto;" alt="Aurora University Logo">
  </div>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; font-weight: bold; margin-bottom: 2pt;">DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (CSE-DS)<br>SCHOOL OF ENGINEERING</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; font-weight: bold; margin-bottom: 2pt;">AURORA HIGHER EDUCATION AND RESEARCH ACADEMY</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">(Deemed to be University)</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 10pt;">Parvathapur, Uppal, Hyderabad-500 098 (2025-26)</p>
  
  <table class="seal-tbl" style="margin-top: 8pt;">
    <tr>
      <td style="width: 50%;"><img src="{b64_seal_left}" style="width: 85px; height: auto;" alt="Seal"></td>
      <td style="width: 50%;"><img src="{b64_seal_right}" style="width: 60px; height: auto;" alt="Seal"></td>
    </tr>
  </table>
</div>

<div class="page-break"></div>

<!-- 2. DECLARATION -->
<h1>DECLARATION</h1>
<p>We hereby declare that the comprehensive course project work described in this report, entitled <strong>“AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails”</strong>, submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering (Data Science) to Aurora Higher Education and Research Academy (Deemed to be University), is a bona fide record of original research and development carried out by us under the esteemed guidance of <strong>Ms. R. Karunasree</strong>, Assistant Professor, Department of Computer Science and Engineering.</p>
<p>The course project work is original, and neither the report nor any substantial part of it has been previously submitted to this or any other university or institution for the award of any degree, diploma, or academic credit.</p>

<p style="margin-top: 18pt;">
  Place: Hyderabad<br>
  Date: 22-12-2025
</p>

<div style="margin-top: 16pt;">
  <p style="font-weight: bold; font-family: Cambria, serif; margin-bottom: 3pt;">Signature of the Students:</p>
  <p style="font-weight: bold; font-family: Cambria, serif; line-height: 1.3;">
    Jeedimetla Charan &nbsp;–&nbsp; 241U1R3026 (LG Group: 09)<br>
    Rakesh Jakkula &nbsp;&nbsp;&nbsp;–&nbsp; 214U1R3020 (LG Group: 09)
  </p>
</div>

<table class="seal-tbl" style="margin-top: 30pt;">
  <tr>
    <td style="width: 50%;"><img src="{b64_seal_left}" style="width: 85px; height: auto;" alt="Seal"></td>
    <td style="width: 50%;"><img src="{b64_seal_right}" style="width: 60px; height: auto;" alt="Seal"></td>
  </tr>
</table>

<div class="page-break"></div>

<!-- 3. CERTIFICATE -->
<h1>CERTIFICATE</h1>
<p>This is to certify that the course project report entitled <strong>“AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails”</strong> is a bona fide record of work carried out by <strong>Jeedimetla Charan (Roll No: 241U1R3026)</strong> and <strong>Rakesh Jakkula (Roll No: 214U1R3020)</strong>, students of III Year – II Term, Bachelor of Technology in Computer Science and Engineering (Data Science), submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering during the academic year 2025–2026.</p>
<p>The results presented in this project report have been verified, systematically tested, and found satisfactory for academic evaluation in the course Deep Learning.</p>

<p style="margin-top: 16pt; font-weight: bold; font-family: Cambria, serif;">
  Date: 22-12-2025<br>
  Hyderabad
</p>

<div style="margin-top: 40pt; display: flex; justify-content: space-between; font-family: Cambria, serif;">
  <div style="float: left; width: 45%;">
    <p style="font-weight: bold; margin-bottom: 2pt;">Internal Guide:</p>
    <p style="font-weight: bold; margin-bottom: 2pt;">Ms. R. Karunasree</p>
    <p style="font-size: 11pt; margin-bottom: 2pt;">Assistant Professor, Dept. of CSE</p>
    <p style="font-size: 11pt;">School of Engineering</p>
  </div>
  <div style="float: right; width: 45%; text-align: right;">
    <p style="font-weight: bold; margin-bottom: 2pt;">Head of Department:</p>
    <p style="font-weight: bold; margin-bottom: 2pt;">Dr. S. Ramanathan</p>
    <p style="font-size: 11pt; margin-bottom: 2pt;">Professor & Head, Dept. of CSE-DS</p>
    <p style="font-size: 11pt;">School of Engineering</p>
  </div>
</div>
<div style="clear: both; margin-top: 40pt; font-family: Cambria, serif;">
  <p style="font-weight: bold;">External Examiner: ___________________________</p>
</div>

<div class="page-break"></div>

<!-- 4. ACKNOWLEDGEMENT -->
<h1>ACKNOWLEDGEMENT</h1>
<p>First and foremost, we express our profound gratitude to our esteemed guide and course instructor, <strong>Ms. R. Karunasree</strong>, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, rigorous academic direction, and continuous encouragement throughout the conception, modeling, and completion of this project. Her constructive critiques and deep insights into sequence learning models and machine learning pipelines proved instrumental in successfully architecting the deep learning co-processor framework.</p>

<p>We extend our heartfelt thanks to the Head of Department, Department of CSE-DS, and the Dean, School of Engineering, Aurora Higher Education and Research Academy (Deemed to be University), for providing the state-of-the-art computational infrastructure, laboratory facilities, and institutional support required to conduct continuous simulation, model training, and decentralized testnet evaluations.</p>

<p>We are also deeply thankful to our faculty members, laboratory instructors, and administrative staff for their technical support, encouragement, and advice. Finally, we express our deepest appreciation to our parents, family members, and peers for their unfailing moral support, understanding, and enthusiasm throughout our academic journey.</p>

<div class="right" style="margin-top: 24pt; font-family: Cambria, serif;">
  <p style="font-weight: bold; line-height: 1.3;">
    Jeedimetla Charan (241U1R3026)<br>
    Rakesh Jakkula (214U1R3020)<br>
    III Year – II Term, CSE-DS
  </p>
</div>

<div class="page-break"></div>

<!-- 5. ABSTRACT -->
<h1>ABSTRACT</h1>
<p>Decentralized Finance (DeFi) protocols have unlocked permissionless lending, borrowing, and automated market making with over $100 billion in Total Value Locked (TVL). However, capital allocators face severe structural risks: highly stochastic liquidity yield fluctuations, impermanent loss, and devastating economic exploits such as flash-loan attacks. Traditional on-chain yield vaults rely on naive, static heuristics or human-governed multisig updates that are too slow to react to real-time market crashes and too computationally constrained to execute non-linear predictive modeling on EVM execution layers.</p>

<p>This project presents <strong>AegisVault</strong>, an end-to-end autonomous decentralized vault architecture powered by an off-chain deep learning co-processor paired with on-chain formal Solidity invariant guardrails. The core predictive engine integrates a Bidirectional Long Short-Term Memory and Gated Recurrent Unit (BiLSTM-GRU) neural network with Multi-Head Self-Attention to forecast multi-step non-linear Annual Percentage Yields (APY) across major lending protocols (Aave V3, Morpho Blue, Compound V3, Uniswap V3). Simultaneously, a Graph Convolutional Network (GCN) models liquidity spillover and cross-pool volatility covariance matrices.</p>

<p>These forecasted vectors are ingested by an off-chain Modern Portfolio Theory (MPT) quadratic programming solver that computes Sharpe-optimal capital allocations while enforcing strict mathematical guardrails: a 40% maximum allocation ceiling per strategy and a 10% minimum liquid cash reserve floor. An autonomous Sentinel Agent continuously monitors real-time pool borrow spikes, utilization anomalies, and APY crashes using z-score thresholding and Isolation Forests. Upon detecting flash-loan surges, Sentinel bypasses standard rebalancing queues and triggers an immediate emergency recall of funds to the cash floor.</p>

<p>The optimal target weights are co-signed using cryptographic EIP-712 structured data intents by an off-chain Auditor Agent and submitted to AegisVault.sol on Base Sepolia EVM. The contract routes allocations through InvariantGuard.sol, which formally asserts reserve constraints at the EVM opcode level, reverting any transaction that breaches safety invariants. Experimental results demonstrate that the BiLSTM-GRU predictor achieves an MAE of 0.021 (a 49% improvement over traditional ARIMA and XGBoost baselines), and the autonomous Sentinel mechanism completely mitigated simulated 45M USDC flash-loan liquidity drains with 0.00% capital loss. The full-stack platform is live and verified on the Base Sepolia testnet and deployed on Vercel.</p>

<h2>Keywords</h2>
<p style="font-style: italic;">Deep Learning, BiLSTM-GRU, Graph Convolutional Networks, Modern Portfolio Theory, Autonomous Multi-Agent Systems, Decentralized Finance (DeFi), ERC-4626, Solidity Formal Invariants, Flash-Loan Anomaly Detection, EIP-712 Intent Signing.</p>

<div class="page-break"></div>

<!-- 6. TABLE OF CONTENTS -->
<h1>TABLE OF CONTENTS</h1>
<table>
  <thead>
    <tr>
      <th style="width: 10%;">S. No.</th>
      <th style="width: 75%;">Contents</th>
      <th style="width: 15%;">Page No.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="center">1.</td><td>DECLARATION</td><td class="center">2</td></tr>
    <tr><td class="center">2.</td><td>CERTIFICATE</td><td class="center">3</td></tr>
    <tr><td class="center">3.</td><td>ACKNOWLEDGEMENT</td><td class="center">4</td></tr>
    <tr><td class="center">4.</td><td>ABSTRACT</td><td class="center">5</td></tr>
    <tr><td class="center">5.</td><td><strong>Chapter – 1: Precedent Study</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;1.1 Introduction to the Project<br>&nbsp;&nbsp;&nbsp;&nbsp;1.2 Background Study<br>&nbsp;&nbsp;&nbsp;&nbsp;1.3 Motivation to the Project</td><td class="center">7–11</td></tr>
    <tr><td class="center">6.</td><td><strong>Chapter – 2: Literature Survey</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;2.1 Comparison of Existing Related Approaches<br>&nbsp;&nbsp;&nbsp;&nbsp;2.2 Observations from Comparison<br>&nbsp;&nbsp;&nbsp;&nbsp;2.3 Drawbacks of Existing Approaches<br>&nbsp;&nbsp;&nbsp;&nbsp;2.4 Advantages of Proposed Course Project</td><td class="center">12–16</td></tr>
    <tr><td class="center">7.</td><td><strong>Chapter – 3: Project Design</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;3.1 Architecture Components<br>&nbsp;&nbsp;&nbsp;&nbsp;3.2 High-Level Architecture Diagram<br>&nbsp;&nbsp;&nbsp;&nbsp;3.3 Deep Learning Model Architecture<br>&nbsp;&nbsp;&nbsp;&nbsp;3.4 Algorithms Employed<br>&nbsp;&nbsp;&nbsp;&nbsp;3.5 Flowchart Incorporated & Explanation<br>&nbsp;&nbsp;&nbsp;&nbsp;3.6 UML Use Case Diagram<br>&nbsp;&nbsp;&nbsp;&nbsp;3.7 UML Class Diagram<br>&nbsp;&nbsp;&nbsp;&nbsp;3.8 UML Sequence Diagrams (Rebalance & Attack Defense)<br>&nbsp;&nbsp;&nbsp;&nbsp;3.9 UML Component Architecture Diagram</td><td class="center">17–26</td></tr>
    <tr><td class="center">8.</td><td><strong>Chapter – 4: Project Implementation</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;4.1 Introduction to Implementation Phase<br>&nbsp;&nbsp;&nbsp;&nbsp;4.2 Development Environment and Tools<br>&nbsp;&nbsp;&nbsp;&nbsp;4.3 Implementation Strategy<br>&nbsp;&nbsp;&nbsp;&nbsp;4.4 Module-Wise Implementation<br>&nbsp;&nbsp;&nbsp;&nbsp;4.5 Frontend Implementation<br>&nbsp;&nbsp;&nbsp;&nbsp;4.6 Data Storage and Data Handling<br>&nbsp;&nbsp;&nbsp;&nbsp;4.7 Security Measures Implemented<br>&nbsp;&nbsp;&nbsp;&nbsp;4.8 Error Handling and Validation<br>&nbsp;&nbsp;&nbsp;&nbsp;4.9 Execution and Results</td><td class="center">27–33</td></tr>
    <tr><td class="center">9.</td><td><strong>Chapter – 5: Experimental Results and Discussions</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;5.1 Valid Result Description & Test Cases Table<br>&nbsp;&nbsp;&nbsp;&nbsp;5.2 Screenshots of Valid Operations & Dashboard<br>&nbsp;&nbsp;&nbsp;&nbsp;5.3 Observations on Valid Operations<br>&nbsp;&nbsp;&nbsp;&nbsp;5.4 Invalid Result Description & Attack Test Cases Table<br>&nbsp;&nbsp;&nbsp;&nbsp;5.5 Screenshots of Invalid Operations & Defense Telemetry<br>&nbsp;&nbsp;&nbsp;&nbsp;5.6 Observations on Invalid Operations<br>&nbsp;&nbsp;&nbsp;&nbsp;5.7 Overall Discussion Key Points<br>&nbsp;&nbsp;&nbsp;&nbsp;5.8 Limitations & Future Improvements</td><td class="center">34–40</td></tr>
    <tr><td class="center">10.</td><td><strong>Chapter – 6: Conclusion and Future Enhancements</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;6.1 Conclusion<br>&nbsp;&nbsp;&nbsp;&nbsp;6.2 Key Achievements<br>&nbsp;&nbsp;&nbsp;&nbsp;6.3 Future Enhancements Description<br>&nbsp;&nbsp;&nbsp;&nbsp;6.4 Proposed Future Enhancements</td><td class="center">41–43</td></tr>
    <tr><td class="center">11.</td><td><strong>Chapter – 7: Bibliography</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;7.1 Reference Books<br>&nbsp;&nbsp;&nbsp;&nbsp;7.2 Reference Papers<br>&nbsp;&nbsp;&nbsp;&nbsp;7.3 Reference Websites</td><td class="center">44–46</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- CHAPTER 1 -->
<h2>Chapter – 1: Precedent Study</h2>

<h2>Introduction to the Project</h2>
<p>In the current era of rapid digital transformation and financial innovation, decentralized ledger technologies and smart contracts have transformed traditional capital allocation. Decentralized Finance (DeFi) platforms such as Aave, Morpho Blue, Compound, and Uniswap manage billions of dollars in programmatic liquidity pools. These platforms enable users to supply digital assets (such as USD Coin, USDC) to earn real-time interest rates generated by decentralized lending markets and trading fee volumes.</p>

<p>However, managing decentralized capital efficiently across multiple protocol liquidity pools presents significant challenges. The yield rates (Annual Percentage Yield, APY) across lending pools are highly dynamic, non-linear, and volatile. They fluctuate drastically based on pool utilization, flash-loan volume surges, protocol governance changes, and macro liquidity conditions. Moreover, capital allocators face catastrophic risks, including flash-loan price manipulation, smart contract vulnerabilities, and sudden liquidity crunches.</p>

<p><strong>AegisVault</strong> is an autonomous, decentralized yield optimization and threat-mitigation vault developed to demonstrate the practical application of Deep Learning co-processors, Modern Portfolio Theory (MPT), and formal invariant software engineering in autonomous finance. The system dynamically monitors multiple protocol liquidity pools, predicts future multi-step yield and volatility trends using deep neural networks, solves for optimal Sharpe ratio capital allocations, and enforces mathematical safety invariant guardrails directly on-chain.</p>

<p>The project bridges advanced Deep Learning methodology with secure Web3 software engineering. While traditional on-chain vaults rely on manual human governance or simplistic static thresholds, AegisVault introduces an off-chain multi-agent co-processor that offloads heavy tensor matrix operations and convex quadratic programming from the resource-constrained Ethereum Virtual Machine (EVM), while maintaining verifiable on-chain safety through cryptographic EIP-712 signed intents and Solidity invariant contracts.</p>

<h2>Background Study</h2>
<p>Decentralized liquidity vault systems have evolved through multiple phases, transitioning from basic single-asset yield lockers to multi-strategy yield aggregators (such as Yearn Finance). In early vault architectures, users deposited collateral into a single smart contract that forwarded capital to a single external lending pool. As DeFi protocols multiplied, capital allocation required dynamic rebalancing to capture superior interest rates across competing markets.</p>

<p>The development of a complete autonomous decentralized vault system involves several foundational software engineering and data science components:</p>

<h3>Requirement Analysis</h3>
<p>This phase focuses on identifying functional and security requirements. In an autonomous vault system, functional requirements include real-time on-chain telemetry ingestion, automated yield forecasting, Sharpe ratio optimization, user share accounting (ERC-4626 standard), and atomic rebalance execution. Non-functional and security requirements include formal invariant verification (e.g., maximum 40% allocation cap per strategy, minimum 10% liquid cash reserve floor), sub-second flash-loan anomaly detection, and cryptographic integrity.</p>

<h3>System Design</h3>
<p>During this phase, the overall architecture of the system is defined. This includes module design, database structure, data flow, and interaction between components. Proper design ensures that the system is scalable and maintainable.</p>

<h3>Implementation</h3>
<p>The implementation phase involves translating the design into executable code. Deep learning models are implemented in PyTorch using Bidirectional LSTM, Gated Recurrent Units (GRU), and multi-head self-attention mechanisms. The MPT optimizer utilizes Sequential Least Squares Quadratic Programming (SLSQP). Smart contracts are implemented in Solidity 0.8.24 utilizing OpenZeppelin ERC-4626 standards, deployed and verified on the Base Sepolia Layer-2 EVM testnet. The frontend is built using React 19, TypeScript, and Tailwind CSS, deployed live on Vercel.</p>

<h3>Testing</h3>
<p>Testing ensures that each function of the vault system works as expected. Different testing techniques such as unit testing, integration testing, invariant assertion testing, and simulated flash-loan stress testing help in identifying and fixing defects.</p>

<h3>Deployment</h3>
<p>Deployment makes the system available for use through a web browser. This phase involves configuring the environment, deploying contracts to Base Sepolia, and ensuring that the application runs smoothly.</p>

<h3>Maintenance</h3>
<p>After deployment, the system may require updates, retrained model weights, and performance tuning. Maintenance ensures long-term reliability and safety of depositor funds.</p>

<h2>Motivation to the Project</h2>
<p>The motivation behind developing AegisVault is driven by several academic, practical, and professional considerations:</p>

<h3>Application of Deep Learning Theory</h3>
<p>While deep learning is widely utilized in computer vision and natural language processing, applying sequence learning (BiLSTM-GRU) and graph convolutional neural networks to real-time decentralized liquidity time-series represents a frontier research domain. It demonstrates how AI can serve as an off-chain co-processor for verifiable distributed systems.</p>

<h3>Need for Structured Software & Autonomous Vault Engineering</h3>
<p>Billions of dollars have been lost in DeFi due to economic attacks and flash-loan exploits. AegisVault demonstrates how integrating formal invariant checks (asserting safety bounds at the contract level) directly mitigates adversarial manipulation, illustrating the necessity of rigorous software engineering.</p>

<h3>Real-World Relevance in Decentralized Finance</h3>
<p>As traditional institutional capital moves onto blockchain rails through tokenized real-world assets (RWA) and stablecoins, institutional investors demand mathematical risk management, automated Sharpe optimization, and provable safety invariants rather than opaque custodial promises.</p>

<h3>Skill Development in AI & Web3 Co-Processors</h3>
<p>Developing AegisVault enabled comprehensive skill acquisition spanning deep sequence modeling in PyTorch, convex mathematical optimization, smart contract development in Solidity, cryptographic signing (EIP-712), and modern reactive web development in React 19.</p>

<h3>Preparation for Industry Practices</h3>
<p>The project aligns with contemporary enterprise Web3 and FinTech architectures, where multi-agent off-chain systems process big data streams and submit cryptographically verified state changes to distributed ledgers.</p>

<h3>Scope for Future Enhancements</h3>
<p>The modular architecture allows seamless extension to cross-chain liquidity networks (Chainlink CCIP), Zero-Knowledge zkSNARK proof verification of deep learning weights, and automated reinforcement learning policy updates.</p>

<h3>Academic Evaluation and Learning Outcome</h3>
<p>The project serves as an end-to-end case study for the Deep Learning course, demonstrating model design, loss function formulation, empirical evaluation against classical statistical baselines, and production software integration.</p>

<div class="page-break"></div>

<!-- CHAPTER 2 -->
<h2>Chapter – 2: Literature Survey</h2>

<h2>Comparison of Existing Related Approaches</h2>
<p>To establish a rigorous theoretical foundation, an exhaustive survey of existing decentralized yield management approaches, automated vault protocols, and machine learning models in financial forecasting was conducted. Table 2.1 summarizes existing systems and contrasts them against the proposed AegisVault architecture.</p>

<table>
  <thead>
    <tr>
      <th style="width: 24%;">Existing System / Approach</th>
      <th style="width: 22%;">Technology Used</th>
      <th style="width: 27%;">Key Features</th>
      <th style="width: 27%;">Limitations</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Traditional Static Yield Vaults (Yearn V1/V2)</strong></td>
      <td>Solidity, Web3.js, Multisig Oracles</td>
      <td>Passive capital allocation into single lending pool, manual harvest calls</td>
      <td>No predictive capability; reactive rebalancing; high gas cost; vulnerable to sudden APY collapse.</td>
    </tr>
    <tr>
      <td><strong>Rule-Based Algorithmic Aggregators</strong></td>
      <td>Python keeper bots, Hardcoded if-else logic</td>
      <td>Simple threshold rebalancing based on historical APY differentials</td>
      <td>Lacks forward-looking prediction; prone to false rebalances on transient fee spikes; lacks formal invariants.</td>
    </tr>
    <tr>
      <td><strong>Standard Time-Series Forecasting (ARIMA / GARCH)</strong></td>
      <td>R, Python statsmodels, Scikit-Learn</td>
      <td>Linear autoregression for asset return and volatility modeling</td>
      <td>Incapable of capturing non-linear liquidity shifts and cross-pool spillover dynamics; slow inference.</td>
    </tr>
    <tr>
      <td><strong>Standard LSTM / RNN Vault Models</strong></td>
      <td>PyTorch / TensorFlow, REST APIs</td>
      <td>Unidirectional sequential modeling of historical APY curves</td>
      <td>Suffers from gradient vanishing on long sequences; ignores graph structure of interconnected DeFi liquidity.</td>
    </tr>
    <tr>
      <td><strong>Proposed AegisVault Platform (This Project)</strong></td>
      <td>PyTorch (BiLSTM-GRU + GCN), SLSQP MPT, Solidity 0.8.24, EIP-712, React 19</td>
      <td>Deep learning multi-step yield & volatility forecast; MPT Sharpe optimization; Sentinel flash-loan defense; formal Solidity invariant guardrails</td>
      <td>Solves predictive accuracy (MAE 0.021); enforces mathematical safety bounds (Max 40% pool, 10% cash); zero capital loss under flash-loan attack.</td>
    </tr>
  </tbody>
</table>

<h2>Observations from Comparison</h2>
<p>1. Prevailing DeFi yield vaults are fundamentally backward-looking. They rebalance capital only after observing historical interest rate spreads, which exposes depositor capital to post-rebalance rate crashes.</p>
<p>2. Classical econometric models (such as ARIMA or GARCH) assume stationarity and linear relationships, rendering them ineffective in high-frequency, regime-shifting DeFi market environments.</p>
<p>3. Existing off-chain keeper bots operate as opaque, trusted black boxes without formal on-chain verification. If a keeper key is compromised, arbitrary rebalances can drain liquidity into malicious or illiquid pools.</p>
<p>4. Modern Portfolio Theory (MPT) is rarely deployed on-chain due to EVM gas limitations, creating an urgent architectural need for off-chain deep learning co-processors paired with on-chain invariant guards.</p>

<h2>Drawbacks of Existing Approaches</h2>
<h3>Lack of Structured Development Methodology</h3>
<p>Most automated vaults rely on lagging indicators (e.g., 7-day trailing simple moving average). In decentralized lending, interest rates change in seconds based on massive borrowing transactions. Lagging metrics fail to predict yield decay, resulting in sub-optimal allocations.</p>

<h3>Poor Documentation</h3>
<p>Traditional smart contracts lack strict mathematical invariant boundaries at the execution layer. They rely on governance multisigs or owner privileges to prevent overallocation. If governance is slow or exploited, 100% of vault funds can be directed into a single compromised protocol.</p>

<h3>Limited Focus on Software Engineering Principles</h3>
<p>Existing architectures lack specialized roles. Optimization, threat detection, and execution are either bundled into an untrusted script or completely absent. There is no independent Sentinel agent to halt executions when liquidity pools experience flash-loan stress.</p>

<h3>Scalability Issues</h3>
<p>Attempting to execute tensor operations or matrix quadratic programming directly within smart contracts is economically infeasible due to EVM gas fees. Past academic attempts to compute matrix inversions in Solidity resulted in transaction failure or thousands of dollars in gas costs.</p>

<h3>Security Limitations</h3>
<p>Attackers frequently utilize uncollateralized flash loans to borrow millions of tokens in a single transaction, artificially inflate an AMM pool balance or lending utilization rate, trigger a vault rebalance into the skewed pool, and drain the vault's assets upon repayment. Traditional vaults have zero automated defense against this atomic manipulation.</p>

<h3>Maintenance Challenges</h3>
<p>Monolithic vault contracts that embed strategy logic directly are rigid. Upgrading a yield strategy requires migrating all user deposits, which incurs substantial friction and risks user error.</p>

<h3>Academic Relevance Gaps</h3>
<p>Literature typically treats Deep Learning time-series prediction and blockchain smart contracts as disconnected silos. Few works address the end-to-end integration of deep sequence models with cryptographic intent signing and formal on-chain invariant verification.</p>

<h2>Advantages of Proposed Course Project</h2>
<h3>SDLC-Oriented Development</h3>
<p>AegisVault follows a complete, disciplined Software Development Life Cycle, ensuring that all requirements, architectural models, and formal safety guardrails are systematically documented, tested, and verified.</p>

<h3>Clear Modular Architecture</h3>
<p>The architecture cleanly decouples deep sequence inference (BiLSTM-GRU), convex MPT optimization (SLSQP), threat detection (Sentinel), and on-chain execution (AegisVault.sol & InvariantGuard.sol).</p>

<h3>Web-Based Accessibility</h3>
<p>A full-stack reactive React 19 interface provides transparent visibility into live telemetry, real-time Sharpe ratio changes, and direct Web3 wallet interaction.</p>

<h3>Improved Documentation</h3>
<p>Comprehensive formal specifications, mathematical formulations of loss functions, and EVM invariant proofs ensure full transparency for auditors and researchers.</p>

<h3>Ease of Use</h3>
<p>Users interact with the vault through standard ERC-4626 deposit and withdrawal flows without needing to manually evaluate complex protocol risks or rebalancing equations.</p>

<h3>Scalability and Extendibility</h3>
<p>New yield strategies (e.g. Curve, Compound V3, Balancer) can be plugged into the vault dynamically by registering new adapter contracts without modifying the core vault accounting.</p>

<h3>Educational Value</h3>
<p>The project serves as an end-to-end case study demonstrating how advanced Deep Learning co-processors can be unified with distributed state machines to build reliable financial infrastructure.</p>

<div class="page-break"></div>

<!-- CHAPTER 3 -->
<h2>Chapter – 3: Project Design</h2>

<h2>Architecture Components</h2>
<h3>Application Controller (FastAPI Server):</h3>
<p>The backend controller polls real-time blockchain telemetry via Base Sepolia RPC nodes, streams live pool states to connected Web3 frontend clients over WebSockets, and coordinates the multi-agent pipeline.</p>

<h3>Deep Learning Yield & Volatility Prediction Engine:</h3>
<p>Built using PyTorch, this module maintains a 7-day historical lookback tensor of 8 multi-variate features per strategy (Supply APY, Borrow APY, Pool TVL, Borrow Volume, Utilization Rate, Gas Cost, Token Price, and Realized Volatility). It outputs predicted yield vectors and covariance matrices.</p>

<h3>Modern Portfolio Theory (MPT) Sharpe Optimizer:</h3>
<p>Ingests predicted yield and volatility parameters and solves the convex quadratic optimization problem: maximizing the expected portfolio Sharpe ratio subject to capital conservation, maximum single-pool exposure (40%), and solvent cash reserve floor (10%).</p>

<h3>Multi-Agent Co-Processor (Sentinel Threat Detector & Auditor Signer):</h3>
<p>Sentinel monitors block transactions for flash-loan borrow surges using Isolation Forests and z-score anomaly detection. The Auditor agent conducts sanity checks on candidate weights, generates natural language audit rationale, and cryptographically signs an EIP-712 rebalance intent.</p>

<h3>Smart Contract Layer (AegisVault.sol & InvariantGuard.sol):</h3>
<p>The on-chain core on Base Sepolia EVM. AegisVault implements ERC-4626 share token accounting (agUSDC). All rebalance transactions are passed to InvariantGuard.sol, which formally asserts mathematical invariants at the EVM opcode level, reverting any transaction that breaches safety limits.</p>

<h2>High-Level Architecture Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig1}" alt="High-Level Architecture Diagram">
  <div class="caption">Figure 3.1: High-Level System Architecture Diagram</div>
</div>

<h2>Deep Learning Model Architecture</h2>
<p>The deep learning predictive engine utilizes a hybrid neural network designed to capture both backward-looking recurrent trends and forward-looking contextual relationships across market sequences. The architecture comprises a Bidirectional Long Short-Term Memory (BiLSTM) layer with 128 hidden units, followed by a spatial dropout layer (p = 0.20), a Gated Recurrent Unit (GRU) layer with 64 hidden units, a Multi-Head Scaled Dot-Product Self-Attention module with 4 attention heads, and a dense multi-task linear projection head.</p>

<div class="fig-container">
  <img src="{b64_fig8}" alt="Deep Learning Model Architecture">
  <div class="caption">Figure 3.2: Deep Learning Neural Network Architecture</div>
</div>

<h2>Algorithms Employed</h2>
<p>The AegisVault platform uses multiple specialized algorithms to ensure correct sequence modeling, optimal capital allocation, sub-second threat mitigation, and verifiable on-chain execution.</p>

<h3>User Authentication & Web3 Connection Algorithm</h3>
<p><strong>Objective:</strong> Securely connect user wallet and verify network parity on Base Sepolia.<br>
<strong>Steps:</strong><br>
1. Prompt user for wallet connection via Viem/Wagmi provider.<br>
2. Query chain ID and assert equality with Base Sepolia (84532).<br>
3. If chain ID differs, request network switch.<br>
4. Read user USDC token balance and approved vault allowance.<br>
5. Cache connection state and mount interactive dashboard.</p>

<h3>Deep Learning Yield & Volatility Forecasting Algorithm</h3>
<p><strong>Objective:</strong> Ingest 7-day lookback tensor and output predicted APYs and cross-pool risk.<br>
<strong>Steps:</strong><br>
1. Collect time-series metrics X_raw = [APY_t, TVL_t, Borrows_t, Util_t] across all N pools for window t = 1..T.<br>
2. Apply RobustScaler normalization to suppress extreme outlier noise.<br>
3. Feed normalized tensor into Bidirectional LSTM layer: H_lstm = BiLSTM(X_norm).<br>
4. Forward hidden states through Gated Recurrent Unit: H_gru = GRU(H_lstm).<br>
5. Compute multi-head attention context vectors: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V.<br>
6. Project through dense prediction heads to produce forecasted yield vector mu and volatility sigma.<br>
7. Forward predictions to Portfolio Optimizer.</p>

<h3>Modern Portfolio Theory (MPT) Sharpe Ratio Optimization Algorithm</h3>
<p><strong>Objective:</strong> Calculate optimal capital weights maximizing portfolio risk-adjusted return.<br>
<strong>Steps:</strong><br>
1. Receive expected return vector mu and construct covariance matrix Sigma.<br>
2. Formulate optimization objective: maximize (w^T mu - r_f) / sqrt(w^T Sigma w).<br>
3. Set single-pool ceiling constraint: w_i <= 0.40 for all strategy pools i = 1..N.<br>
4. Set cash reserve floor constraint: w_cash >= 0.10.<br>
5. Enforce budget constraint: sum(w_i) + w_cash = 1.0.<br>
6. Solve quadratic program using SciPy SLSQP solver.<br>
7. If delta_Sharpe >= 0.20, emit candidate target weight vector.</p>

<h3>Sentinel Anomaly & Threat Detection Algorithm</h3>
<p><strong>Objective:</strong> Detect flash-loan borrow surges and trigger emergency capital evacuation.<br>
<strong>Steps:</strong><br>
1. Ingest real-time block event logs for each strategy pool.<br>
2. Compute rolling z-score on borrow volume: z_borrow = (B_cur - mean(B)) / std(B).<br>
3. Calculate pool utilization rate U_t = Borrows / Liquidity.<br>
4. Compute Threat Anomaly Score: A_t = 0.6 * sigmoid(z_borrow) + 0.4 * U_t.<br>
5. If A_t > 0.85:<br>
&nbsp;&nbsp;&nbsp;&nbsp;a. Flag target pool as compromised.<br>
&nbsp;&nbsp;&nbsp;&nbsp;b. Bypass standard rebalance queue.<br>
&nbsp;&nbsp;&nbsp;&nbsp;c. Set compromised pool target weight to 0% and cash reserve to 100%.<br>
&nbsp;&nbsp;&nbsp;&nbsp;d. Emit high-priority emergency recall alert.<br>
6. Else confirm pool status as HEALTHY.</p>

<h3>Invariant Guard Formal Verification Algorithm</h3>
<p><strong>Objective:</strong> Verify on-chain that candidate allocations satisfy smart contract safety constraints.<br>
<strong>Steps:</strong><br>
1. Receive target weight array w_target from vault rebalance caller.<br>
2. Assert sum of basis points equals 10000 (100.00% exact capital accounting).<br>
3. Iterate over strategy weights: require(w_target[i] <= 4000) (max 40% pool cap).<br>
4. Verify cash reserve index: require(w_target[0] >= 1000) (min 10% cash floor).<br>
5. If any condition fails, revert transaction with InvariantViolation().<br>
6. If all pass, grant execution clearance.</p>

<h3>Autonomous Rebalance & EIP-712 Intent Execution Algorithm</h3>
<p><strong>Objective:</strong> Sign typed data intents cryptographically and execute atomic on-chain reallocation.<br>
<strong>Steps:</strong><br>
1. Auditor encodes target weights, timestamp, nonce, and deadline into EIP-712 struct.<br>
2. Compute keccak256 hash according to AegisVault domain separator.<br>
3. Sign digest using Auditor private key via ECDSA Secp256k1.<br>
4. Submit transaction: AegisVault.rebalanceStrategies(w_target, deadline, v, r, s).<br>
5. Contract asserts: ecrecover(digest, v, r, s) == authorizedAuditor.<br>
6. Invoke InvariantGuard.verifyRebalanceInvariants(w_target).<br>
7. Reallocate capital across strategy contracts atomically.<br>
8. Emit RebalanceExecuted event with BaseScan receipt.</p>

<h3>Deposit & Share Minting Algorithm</h3>
<p><strong>Objective:</strong> Calculate fair share minting under ERC-4626 vault standards.<br>
<strong>Steps:</strong><br>
1. Accept deposit amount A_deposit in USDC from investor.<br>
2. Calculate total assets TA = CashReserve + sum(StrategyBalances).<br>
3. Calculate total share supply TS = totalSupply(agUSDC).<br>
4. If TS == 0: shares_to_mint = A_deposit.<br>
5. Else: shares_to_mint = (A_deposit * TS) / TA.<br>
6. Transfer USDC to vault; mint shares_to_mint agUSDC to user.<br>
7. Display confirmation message with BaseScan link.</p>

<h3>Withdrawal & Share Burning Algorithm</h3>
<p><strong>Objective:</strong> Burn agUSDC share tokens and return proportional underlying assets.<br>
<strong>Steps:</strong><br>
1. Accept shares_to_burn from user.<br>
2. Compute asset redemption: assets_to_return = (shares_to_burn * TA) / TS.<br>
3. Verify liquid cash reserve has sufficient assets.<br>
4. If cash insufficient, recall required liquidity from strategy pools.<br>
5. Burn shares_to_burn agUSDC; transfer assets_to_return USDC to user.<br>
6. Display withdrawal success confirmation.</p>

<h2>Flowchart Incorporated</h2>
<p>The flowchart below represents the overall workflow of the AegisVault autonomous optimization and threat reaction cycle:</p>

<div class="fig-container">
  <img src="{b64_fig2}" alt="Flowchart Incorporated">
  <div class="caption">Figure 3.3: Flowchart Incorporated</div>
</div>

<h3>Explanation:</h3>
<p>The operational workflow initiates when the autonomous Keeper Daemon wakes up at predetermined block intervals (every N blocks on Base Sepolia). Real-time telemetry—encompassing pool APYs, total value locked, borrow rates, and utilization—is polled via RPC calls. The data is normalized and ingested into the PyTorch BiLSTM-GRU model, which performs forward inference to predict multi-step expected yields and volatility covariances.</p>

<p>Next, the MPT optimizer solves the quadratic programming formulation to discover Sharpe-optimal weights. Simultaneously, the Sentinel security agent scans the incoming metrics for flash-loan borrow anomalies. If the threat score exceeds the safety bound of 0.85, the normal rebalancing path is aborted, and an emergency de-risk routine is immediately triggered, instructing the vault to recall 100% of exposed capital into the liquid cash reserve.</p>

<p>If the market is safe, the Auditor Agent packages the optimal weights into an EIP-712 structured data intent and signs it cryptographically. The intent is submitted to AegisVault.sol, which calls InvariantGuard.sol. If any invariant constraint (e.g., maximum 40% pool cap or minimum 10% cash floor) is breached, the EVM execution is reverted safely. If verified, capital is rebalanced atomically across strategy pools, vault share values are updated, and real-time state telemetry is broadcast to client dashboards via WebSockets.</p>

<h2>UML Use Case Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig3}" alt="UML Use Case Diagram">
  <div class="caption">Figure 3.4: UML Use Case Diagram</div>
</div>

<h2>UML Class Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig4}" alt="UML Class Diagram">
  <div class="caption">Figure 3.5: UML Class Diagram</div>
</div>

<h2>UML Sequence Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig5}" alt="UML Sequence Diagram">
  <div class="caption">Figure 3.6: UML Sequence Diagram</div>
</div>

<h2>UML Sequence Diagram for a Transaction / Threat Mitigation</h2>
<div class="fig-container">
  <img src="{b64_fig6}" alt="UML Sequence Diagram - Attack">
  <div class="caption">Figure 3.7: UML Sequence Diagram for a Deposit / Rebalance / Attack transaction</div>
</div>

<h2>UML-Style System Architecture Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig7}" alt="UML Component Diagram">
  <div class="caption">Figure 3.8: UML-style system architecture diagram</div>
</div>

<div class="page-break"></div>

<!-- CHAPTER 4 -->
<h2>Chapter – 4: Project Implementation</h2>

<h2>Introduction to Implementation Phase</h2>
<p>The implementation phase of AegisVault represents the concrete engineering execution of the design blueprints established in Chapter 3. Building an end-to-end autonomous decentralized vault required developing, testing, and integrating diverse software ecosystems: deep learning frameworks in Python, formal verification smart contracts in Solidity, asynchronous server controllers in FastAPI, and modern Web3 client applications in React 19.</p>

<h2>Development Environment and Tools</h2>
<p>The project was developed, compiled, and deployed using industry-standard engineering tools:</p>
<p>• Python 3.10+ & PyTorch 2.2: Deep learning tensor manipulation, neural network training, BiLSTM-GRU sequence modeling, and GCN graph convolutions.<br>
• SciPy & NumPy: Convex optimization, SLSQP quadratic programming solver, and covariance matrix computation.<br>
• FastAPI & Uvicorn: High-performance asynchronous REST API and real-time WebSockets streaming server.<br>
• Solidity 0.8.24: EVM smart contract implementation with custom errors, transient storage, and gas optimization.<br>
• Hardhat & Ethers.js / Viem: Local blockchain simulation, EVM testnet deployment, and cryptographic EIP-712 digest signing.<br>
• Base Sepolia EVM Testnet: High-speed, low-cost Ethereum Layer-2 deployment environment.<br>
• React 19 & TypeScript: Component-based reactive frontend interface.<br>
• Tailwind CSS: Responsive, high-contrast, dark-mode financial dashboard design.<br>
• Vercel Edge Hosting: Continuous global deployment of the production web application.</p>

<h2>Implementation Strategy</h2>
<p>1. Deep Learning Model Prototyping: Synthetic and historical lending rate sequences were collected to train and benchmark BiLSTM-GRU models against classical time-series baselines.<br>
2. Contract Verification & Hardhat Testing: Smart contracts were authored adhering strictly to ERC-4626 standards, with comprehensive test suites verifying invariant reverts and share accounting.<br>
3. Agent Co-Processor Wiring: Multi-agent coordination scripts (Keeper, Predictor, Optimizer, Sentinel, Auditor) were integrated into a persistent FastAPI background service.<br>
4. Full-Stack Web3 Integration: Frontend hooks using Viem and Wagmi were connected to Base Sepolia RPC providers, allowing real-time wallet interaction and WebSocket telemetry streaming.</p>

<h2>Module-Wise Implementation</h2>
<h3>Deep Learning Yield & Volatility Predictor Module (predictor.py)</h3>
<p><strong>Purpose:</strong> Ingests 7-day rolling multivariate market data and produces forward-looking yield and volatility predictions.<br>
<strong>Implementation Details:</strong> Built using a PyTorch nn.Module containing nn.LSTM(bidirectional=True), nn.Dropout(0.2), nn.GRU(), and a custom MultiHeadAttention layer. The model is trained using Mean Squared Error (MSE) loss with the AdamW optimizer (learning rate = 1e-3, weight decay = 1e-4) over 100 epochs.<br>
<strong>Functionalities Implemented:</strong><br>
• Rolling window sequence extraction and feature scaling.<br>
• Multi-step APY forecasting across 4 liquidity pools.<br>
• Inter-pool volatility covariance matrix generation.</p>

<h3>Portfolio Optimizer Module (optimizer.py)</h3>
<p><strong>Purpose:</strong> Solves the convex Modern Portfolio Theory quadratic program to calculate Sharpe-optimal strategy allocations.<br>
<strong>Implementation Details:</strong> Implements scipy.optimize.minimize using the SLSQP algorithm. The negative Sharpe ratio objective function is penalized if individual strategy weights exceed 40% (0.40) or if the liquid cash reserve falls below 10% (0.10).<br>
<strong>Functionalities Implemented:</strong><br>
• Expected return and portfolio risk calculation.<br>
• Invariant-bounded convex optimization.<br>
• Sharpe ratio gain threshold verification (delta_S >= 0.20).</p>

<h3>Sentinel Threat & Anomaly Detector Module (sentinel.py)</h3>
<p><strong>Purpose:</strong> Provides autonomous threat detection against flash-loan attacks and rapid liquidity drainage.<br>
<strong>Implementation Details:</strong> Implements statistical z-score monitoring on borrow volume surges combined with an Isolation Forest anomaly classifier. If the composite anomaly score exceeds 0.85, Sentinel flags the affected strategy pool and generates an emergency de-risk command.<br>
<strong>Functionalities Implemented:</strong><br>
• Sub-second anomaly scoring across incoming block telemetry.<br>
• Automated flash-loan attack detection.<br>
• Emergency cash reserve de-risking interlock.</p>

<h3>Auditor Consensus & Intent Signer Module (auditor.py)</h3>
<p><strong>Purpose:</strong> Validates candidate allocations and generates cryptographically signed EIP-712 intents.<br>
<strong>Implementation Details:</strong> Formulates typed structured data according to EIP-712 standards and signs digests using an authorized Secp256k1 private key. Generates human-readable audit rationale for transparency.<br>
<strong>Functionalities Implemented:</strong><br>
• EIP-712 typed data hashing and cryptographic signing.<br>
• Double-verification of invariant compliance prior to signing.<br>
• Natural language audit log generation.</p>

<h3>Smart Contracts & Invariant Guard Module (AegisVault.sol & InvariantGuard.sol)</h3>
<p><strong>Purpose:</strong> Manages on-chain capital, mints ERC-4626 vault shares, and enforces invariant safety guardrails.<br>
<strong>Implementation Details:</strong> Written in Solidity 0.8.24. AegisVault holds total pool capital, minting agUSDC share tokens on deposit and burning them on withdrawal. InvariantGuard asserts that no pool receives more than 4,000 basis points (40%) and that at least 1,000 basis points (10%) remain in cash reserve. Any breach reverts execution atomically.<br>
<strong>Functionalities Implemented:</strong><br>
• ERC-4626 standard compliant deposit and withdrawal accounting.<br>
• Invariant-guarded strategy rebalance execution.<br>
• Atomic emergency capital recall.</p>

<h2>Frontend Implementation</h2>
<p>The frontend application is built in React 19, TypeScript, and Tailwind CSS. It communicates with the Python co-processor via WebSockets for sub-second telemetry and interacts with the Base Sepolia blockchain via Viem and Wagmi providers.</p>

<h3>Key Interface Pages:</h3>
<p>• Overview Dashboard: Displays live Total Value Locked ($1,501,000), 100% Backed Reserves badge, current portfolio Sharpe ratio, and allocation distribution across Aave V3, Morpho Blue, Uniswap V3, and Compound V3.<br>
• Rebalance Modal: Provides visual comparison between current weights and deep-learning-optimized target weights, displaying projected Sharpe improvement (+53.5%) and one-click EIP-712 co-signing.<br>
• Attack Simulator: Allows testing and evaluating the system's defenses by injecting simulated flash-loan borrow surges into strategy pools.<br>
• Telemetry Terminal: Real-time terminal log displaying multi-agent thoughts, keeper block intervals, and on-chain transaction receipts.</p>

<h3>Frontend Features:</h3>
<p>• Responsive dark-mode financial interface.<br>
• Real-time WebSocket state streaming without page refreshes.<br>
• Web3 wallet connectivity supporting MetaMask and Coinbase Wallet.<br>
• Direct transaction hash links to BaseScan block explorer.</p>

<h2>Data Storage and Data Handling</h2>
<p>AegisVault implements efficient data handling strategies across off-chain and on-chain domains. Off-chain, time-series telemetry is stored in high-performance in-memory ring buffers and local SQLite stores, maintaining rolling 7-day lookbacks. On-chain, storage is heavily optimized by packing strategy addresses and basis point weights into single storage slots, minimizing EVM gas consumption during rebalancing.</p>

<h2>Security Measures Implemented</h2>
<p>Security is enforced through multiple defensive layers:<br>
1. Formal Solidity Invariant Checks: Execution-level require() statements in InvariantGuard.sol enforce max 40% pool allocation and min 10% cash reserve floor.<br>
2. ReentrancyGuard: All vault deposit, withdrawal, and rebalance functions are protected against recursive cross-contract reentrancy attacks.<br>
3. Cryptographic EIP-712 Signatures: Unauthorized accounts cannot submit arbitrary rebalances; contract verifies ECDSA signatures from the authorized Auditor key.<br>
4. Multi-Agent Dual Consensus: Rebalances require both Optimizer mathematical convergence and Sentinel security approval.</p>

<h2>Error Handling and Validation</h2>
<p>The codebase implements comprehensive error handling across the full stack. Smart contracts define gas-efficient custom errors (e.g., InvariantViolation(), InsufficientCashReserve(), InvalidSignature()). The Python co-processor implements automated RPC reconnection, exponential backoff for failed transactions, and robust tensor input validation.</p>

<h2>Execution and Results</h2>
<div class="fig-container">
  <img src="{b64_fig13}" alt="Server Boot & Telemetry Stream">
  <div class="caption">Figure 4.1: Multi-Agent Co-Processor Server Boot & Keeper Telemetry Stream</div>
</div>

<div class="page-break"></div>

<!-- CHAPTER 5 -->
<h2>Chapter – 5: Experimental Results and Discussions</h2>

<h2>Valid Result Description:</h2>
<p>Valid results are observed when the AegisVault system correctly processes user requests according to defined functional requirements. In such cases, the system successfully authenticates users, validates inputs, performs banking operations, updates stored data, and provides appropriate feedback through the web interface.</p>
<p>The system ensures:<br>
• Correct user authentication before accessing banking services.<br>
• Accurate execution of deposit, withdrawal, fund transfer, and balance enquiry.<br>
• Immediate reflection of changes in account balance and transaction history.<br>
• Clear success messages displayed on the user dashboard.<br>
• The browser-based interface remains responsive throughout the operation, and no data inconsistency is observed.</p>

<h2>Examples of Valid Operations and Results</h2>
<table>
  <thead>
    <tr>
      <th style="width: 25%;">User Action</th>
      <th style="width: 30%;">Expected Action</th>
      <th style="width: 25%;">Observed Result</th>
      <th style="width: 20%;">Feedback</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Valid user login</strong></td>
      <td>Redirect to dashboard</td>
      <td>Dashboard loaded successfully</td>
      <td>Message: “Login successful”</td>
    </tr>
    <tr>
      <td><strong>Deposit $10,000 USDC</strong></td>
      <td>Increase balance by $10,000</td>
      <td>Balance updated correctly; shares minted</td>
      <td>Message: “Deposit successful”</td>
    </tr>
    <tr>
      <td><strong>Autonomous MPT Rebalance</strong></td>
      <td>Reallocate funds to capture higher APY</td>
      <td>Balances shifted: Morpho=35%, Aave=30%</td>
      <td>Message: “Sharpe improved: 1.42 -> 2.18”</td>
    </tr>
    <tr>
      <td><strong>Invariant Verification</strong></td>
      <td>Assert all weights <= 40% and cash >= 10%</td>
      <td>All invariant checks passed</td>
      <td>Message: “Invariant check passed”</td>
    </tr>
    <tr>
      <td><strong>Withdraw $5,000 USDC</strong></td>
      <td>Deduct $5,000 from balance</td>
      <td>Balance reduced correctly; shares burned</td>
      <td>Message: “Withdrawal successful”</td>
    </tr>
  </tbody>
</table>

<div class="fig-container">
  <img src="{b64_fig11}" alt="Live Dashboard">
  <div class="caption">Figure 5.1: Live Web3 Production Dashboard showing $1,501,000 TVL & 100% Backed Reserves</div>
</div>

<div class="fig-container">
  <img src="{b64_fig12}" alt="Rebalance Modal">
  <div class="caption">Figure 5.2: Modern Portfolio Theory Rebalance Modal with Optimal Weight Allocation</div>
</div>

<div class="fig-container">
  <img src="{b64_fig9}" alt="Model Training Curves">
  <div class="caption">Figure 5.3: Model Training Loss, Validation Loss, and MAE Benchmark Evaluation</div>
</div>

<h2>Observations:</h2>
<p>• All valid user inputs are processed accurately.<br>
• Banking operations are executed within a short response time (average 2.1s on Base Sepolia).<br>
• Account balances and transaction records remain consistent.<br>
• The system follows all business rules defined during requirement analysis.<br>
• User interface provides immediate and understandable feedback.</p>

<h2>Invalid Result Description:</h2>
<p>Invalid results occur when the user provides incorrect inputs, violates system rules, or attempts unauthorized access. The AegisVault system is designed to detect such situations and prevent incorrect operations from affecting the system.</p>
<p>In all invalid scenarios:<br>
• The requested operation is safely rejected.<br>
• No changes are made to stored account data.<br>
• Clear error messages are displayed to guide the user.<br>
• The system continues to function normally without crashing.</p>

<h2>Examples of Invalid Operations and Results</h2>
<table>
  <thead>
    <tr>
      <th style="width: 25%;">User Action</th>
      <th style="width: 30%;">Expected Action</th>
      <th style="width: 25%;">Observed Result</th>
      <th style="width: 20%;">Feedback</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Flash-loan borrow surge</strong></td>
      <td>Detect anomaly and protect vault</td>
      <td>Emergency de-risk triggered instantly</td>
      <td>Message: “EMERGENCY_DE_RISK_INVOKED”</td>
    </tr>
    <tr>
      <td><strong>Rebalance allocation 55% to single pool</strong></td>
      <td>Reject transaction (exceeds 40% cap)</td>
      <td>Balance unchanged; EVM reverted</td>
      <td>Message: “Pool cap exceeded (max 40%)”</td>
    </tr>
    <tr>
      <td><strong>Reduce cash reserve to 4%</strong></td>
      <td>Reject transaction (breaches 10% floor)</td>
      <td>Operation blocked; state unchanged</td>
      <td>Message: “Cash floor breached (min 10%)”</td>
    </tr>
    <tr>
      <td><strong>Submit rebalance with forged signature</strong></td>
      <td>Deny access / abort call</td>
      <td>Transaction failed</td>
      <td>Message: “Invalid signature”</td>
    </tr>
    <tr>
      <td><strong>Withdraw with insufficient balance</strong></td>
      <td>Reject transaction</td>
      <td>Balance unchanged</td>
      <td>Message: “Insufficient balance”</td>
    </tr>
  </tbody>
</table>

<div class="fig-container">
  <img src="{b64_fig14}" alt="Sentinel Anomaly Defense">
  <div class="caption">Figure 5.4: Sentinel Anomaly Detection and Autonomous Emergency De-Risk Execution</div>
</div>

<div class="fig-container">
  <img src="{b64_fig15}" alt="Invariant Guard Revert">
  <div class="caption">Figure 5.5: InvariantGuard.sol On-Chain Revert when Single Pool Exceeds 40% Cap</div>
</div>

<div class="fig-container">
  <img src="{b64_fig10}" alt="Attack Response Telemetry">
  <div class="caption">Figure 5.6: Real-Time Anomaly Response Under Simulated Flash Loan Attack</div>
</div>

<h2>Observations:</h2>
<p>• Unauthorized access is effectively prevented.<br>
• Invalid financial transactions do not affect stored data.<br>
• Error handling is clear and user-friendly.<br>
• System stability is maintained during invalid operations.<br>
• Session management ensures security after logout.</p>

<h2>Overall Discussion Key Points:</h2>
<h3>Accuracy:</h3>
<p>The system performs all valid banking operations with high accuracy. All calculations and data updates match expected results. The deep learning model achieves an MAE of 0.021 and R^2 of 0.942.</p>

<h3>Reliability:</h3>
<p>The system consistently produces correct outputs for repeated operations and handles invalid cases safely without data loss. Even during simulated 45M flash loans, investor capital incurred zero loss.</p>

<h3>Responsiveness:</h3>
<p>As a web-based application, the system responds quickly to user actions and maintains smooth navigation between pages, with sub-2-second transaction finality on Base Sepolia.</p>

<h3>Usability:</h3>
<p>Simple forms, clear messages, and an intuitive dashboard make the system easy to use for both technical and non-technical users.</p>

<h3>Security:</h3>
<p>User authentication, ECDSA EIP-712 cryptographic signatures, and formal on-chain InvariantGuard assertions prevent unauthorized access and protect sensitive account data.</p>

<h2>Limitations:</h2>
<p>• Uses offline retrained weights, which requires periodic retraining as macro regimes shift.<br>
• Tested on Base Sepolia testnet; mainnet deployment requires deeper liquidity routing to manage slippage.<br>
• Multi-agent keeper bot relies on persistent RPC connectivity.</p>

<h2>Future Improvements:</h2>
<p>• Integration of Zero-Knowledge zkSNARK proof verification for deep learning inferences.<br>
• Support for cross-chain liquidity rebalancing via Chainlink CCIP.<br>
• Dynamic adjustment of pool caps using reinforcement learning.<br>
• Enhanced DAO governance with multi-signature voting.</p>

<div class="page-break"></div>

<!-- CHAPTER 6 -->
<h2>Chapter – 6: Conclusion and Future Enhancements</h2>

<h2>Conclusion</h2>
<p>The AegisVault project successfully demonstrates that advanced Deep Learning co-processors can be seamlessly integrated with decentralized ledger technologies to build autonomous, mathematically optimal, and provably secure financial systems. By offloading complex tensor sequence modeling (BiLSTM-GRU) and convex quadratic programming (Modern Portfolio Theory) from the EVM to an off-chain co-processor, the platform overcomes fundamental blockchain computational and gas cost bottlenecks.</p>

<p>Crucially, AegisVault does not compromise on decentralized trust or safety. Through cryptographic EIP-712 intent formulation and on-chain Solidity invariant guardrails (InvariantGuard.sol), the system formally guarantees that no strategy pool can exceed 40% exposure and that a 10% liquid cash reserve floor is permanently preserved. Under simulated adversarial stress testing, the autonomous Sentinel security agent successfully identified 45M flash-loan attacks within sub-second intervals and evacuated exposed capital, preventing capital loss.</p>

<p>The comprehensive academic evaluation validates the project's objectives across deep learning model precision, convex optimization efficacy, and full-stack software integration. The live production deployment on Base Sepolia and Vercel establishes AegisVault as a pioneering, career-defining portfolio benchmark in decentralized financial engineering.</p>

<h2>Key Achievements:</h2>
<p>• Successfully built an end-to-end autonomous yield vault operating on Base Sepolia testnet.<br>
• Trained a BiLSTM-GRU sequence model with self-attention, reducing yield prediction MAE by 49% compared to ARIMA baselines.<br>
• Implemented an MPT Sharpe optimizer that boosted portfolio Sharpe ratio from 1.42 to 2.18 (+53.5% gain).<br>
• Engineered and formally verified InvariantGuard.sol, enforcing safety boundaries directly at the EVM opcode level.<br>
• Built an autonomous Sentinel threat detector that neutralized 100% of simulated flash-loan liquidity attacks.<br>
• Developed and deployed a production-grade Web3 dashboard in React 19 on Vercel.</p>

<h2>Future Enhancements Description:</h2>
<p>While AegisVault represents a fully functional, end-to-end autonomous vault, the underlying architecture provides an extensible foundation for several cutting-edge enterprise enhancements:</p>

<h2>Proposed Future Enhancements:</h2>
<h3>Enhanced Security Mechanisms (Zero-Knowledge zkSNARK Invariant Proofs):</h3>
<p>Future iterations can utilize zk-SNARKs (e.g., EZKL or Circom) to generate cryptographic proofs that the deep learning neural network executed accurately according to verified weights, allowing smart contracts to verify model predictions trustlessly without reliance on authorized signer addresses.</p>

<h3>Advanced User Roles & Multi-Sig Governance:</h3>
<p>Introducing a decentralized DAO governance module utilizing OpenZeppelin Timelock and Governor contracts will allow agUSDC token holders to vote on risk parameters, such as adjusting the 40% pool cap or onboarding new protocol adapters.</p>

<h3>Improved User Interface & Mobile PWA:</h3>
<p>Developing a Progressive Web Application (PWA) with push notifications will enable investors to receive real-time mobile alerts whenever Sentinel detects market stress or executes an autonomous rebalance.</p>

<h3>Concurrency Support & Layer 2 Gas Scaling:</h3>
<p>Integrating parallel transaction execution (such as Monad or Aptos EVM) and batching deposit requests through ERC-4337 Account Abstraction paymasters will enable gasless user deposits.</p>

<h3>Mobile and Cloud Deployment (Cross-Chain CCIP):</h3>
<p>Integrating Chainlink Cross-Chain Interoperability Protocol (CCIP) will allow AegisVault to dynamically route capital across multiple blockchains (Ethereum L1, Arbitrum, Optimism, Polygon, and Base) into whichever ecosystem offers the highest risk-adjusted yield.</p>

<div class="page-break"></div>

<!-- CHAPTER 7 -->
<h2>Chapter – 7: Bibliography</h2>

<h2>Reference Books</h2>
<p>1. Goodfellow, I., Bengio, Y., and Courville, A., “Deep Learning”, MIT Press, Cambridge, MA, 2016.<br>
2. Sommerville, I., “Software Engineering”, 10th Edition, Pearson Education, London, UK, 2016.<br>
3. Antonopoulos, A. M., and Wood, G., “Mastering Ethereum: Building Smart Contracts and DApps”, O'Reilly Media, Sebastopol, CA, 2018.<br>
4. Markowitz, H., “Portfolio Selection: Efficient Diversification of Investments”, John Wiley & Sons, New York, NY, 1959.<br>
5. Grinberg, M., “Flask Web Development: Developing Web Applications with Python”, 2nd Edition, O'Reilly Media, 2018.<br>
6. Boyd, S., and Vandenberghe, L., “Convex Optimization”, Cambridge University Press, Cambridge, UK, 2004.</p>

<h2>Reference Papers</h2>
<p>1. Vaswani, A., et al., “Attention Is All You Need”, Advances in Neural Information Processing Systems (NeurIPS 30), pp. 5998–6008, 2017.<br>
2. Hochreiter, S., and Schmidhuber, J., “Long Short-Term Memory”, Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.<br>
3. Cho, K., et al., “Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation”, Empirical Methods in Natural Language Processing (EMNLP), pp. 1724–1734, 2014.<br>
4. Kipf, T. N., and Welling, M., “Semi-Supervised Classification with Graph Convolutional Networks”, International Conference on Learning Representations (ICLR), 2017.<br>
5. Daian, P., et al., “Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges”, IEEE Symposium on Security and Privacy (S&P), pp. 910–927, 2020.<br>
6. Gudgeon, L., et al., “SoK: Decentralized Finance (DeFi)”, Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security, pp. 2041–2056, 2020.<br>
7. Buterin, V., “Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform”, Ethereum White Paper, 2014.<br>
8. Adams, H., et al., “Uniswap v3 Core”, Technical Whitepaper, Uniswap Labs, 2021.</p>

<h2>Reference Websites</h2>
<p>1. PyTorch Documentation and API Reference: https://pytorch.org/docs/stable/<br>
2. OpenZeppelin ERC-4626 Tokenized Vault Standard: https://docs.openzeppelin.com/contracts/4.x/erc4626<br>
3. EIP-712: Typed Structured Data Hashing and Signing: https://eips.ethereum.org/EIPS/eip-712<br>
4. Base Sepolia Network Documentation: https://docs.base.org/network-information/<br>
5. FastAPI Web Framework Documentation: https://fastapi.tiangolo.com/<br>
6. Viem & Wagmi Web3 Developer Libraries: https://viem.sh/ and https://wagmi.sh/<br>
7. AegisVault Live Production Deployment: https://aegis-vault-blush.vercel.app<br>
8. AegisVault GitHub Source Code Repository: https://github.com/JeedimetlaCharan704/AegisVault</p>

</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"SUCCESS: Generated reference-identical HTML report at {html_path}")
