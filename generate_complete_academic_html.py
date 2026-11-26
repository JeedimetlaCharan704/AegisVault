import os, base64

html_path = r'c:\3rd year charan\Hackathon project analysis\aegis-vault\DEEP_LEARNING_PROJECT_REPORT.html'
img_dir = r'c:\3rd year charan\Hackathon project analysis\aegis-vault\report_images'

def img_to_b64(fname):
    p = os.path.join(img_dir, fname)
    if os.path.exists(p):
        ext = fname.split('.')[-1].lower()
        mime = 'image/png' if ext == 'png' else 'image/jpeg'
        with open(p, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return f"data:{mime};base64,{data}"
    return ""

# Convert all images to base64 for standalone HTML rendering
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
    color: #111827;
    background-color: #ffffff;
    margin: 0 auto;
    padding: 0;
    max-width: 800px;
    text-align: justify;
  }}
  h1 {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin-top: 18pt;
    margin-bottom: 10pt;
    line-height: 1.2;
    page-break-after: avoid;
  }}
  h2 {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 13pt;
    font-weight: bold;
    text-align: left;
    margin-top: 14pt;
    margin-bottom: 4pt;
    line-height: 1.2;
    page-break-after: avoid;
  }}
  h3 {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    font-weight: bold;
    font-style: italic;
    text-align: left;
    margin-top: 8pt;
    margin-bottom: 2pt;
    line-height: 1.2;
    page-break-after: avoid;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 6pt;
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
    margin: 12pt 0;
    page-break-inside: avoid;
  }}
  .fig-container img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
  }}
  .caption {{
    font-size: 10pt;
    font-style: italic;
    font-weight: bold;
    text-align: center;
    margin-top: 4pt;
    margin-bottom: 8pt;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 10pt;
    line-height: 1.25;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #475569;
    padding: 6pt 8pt;
    text-align: left;
    vertical-align: middle;
  }}
  th {{
    background-color: #e2e8f0;
    font-weight: bold;
    text-align: center;
  }}
  .th-danger {{
    background-color: #fee2e2;
  }}
  .seal-tbl td {{
    border: none;
    text-align: center;
  }}
  .btn-print {{
    position: fixed;
    top: 16px;
    right: 16px;
    background-color: #2563eb;
    color: white;
    padding: 10px 18px;
    font-size: 11pt;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
  }}
  @media print {{
    .btn-print {{ display: none; }}
    body {{ max-width: 100%; padding: 0; }}
  }}
</style>
</head>
<body>

<button class="btn-print" onclick="window.print()">🖨️ Print / Save as PDF (Ctrl+P)</button>

<!-- 1. COVER PAGE -->
<div class="center" style="margin-top: 20pt;">
  <p style="font-family: Cambria, serif; font-size: 14pt; margin-bottom: 2pt;">A</p>
  <p style="font-family: Cambria, serif; font-size: 14pt; margin-bottom: 12pt;">Project report on</p>
  
  <p style="font-size: 16pt; font-weight: bold; line-height: 1.25; margin-bottom: 16pt;">
    AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails
  </p>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">Submitted in partial fulfilment of the award of the</p>
  <p style="font-family: Cambria, serif; font-size: 14pt; font-weight: bold; margin-bottom: 2pt;">Bachelor of Technology</p>
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">in</p>
  <p style="font-family: Cambria, serif; font-size: 13pt; font-weight: bold; margin-bottom: 14pt;">
    DEPARTMENT OF CSE-DS<br><span style="font-size: 11pt; font-weight: normal;">(Computer Science and Engineering – Data Science)</span>
  </p>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 4pt;">By</p>
  <p style="font-size: 12pt; font-weight: bold; line-height: 1.3; margin-bottom: 14pt;">
    JEEDIMETLA CHARAN – 241U1R3026 (LG Group: 09)<br>
    RAKESH JAKKULA – 214U1R3020 (LG Group: 09)
  </p>
  
  <p style="font-family: Cambria, serif; font-size: 12pt; margin-bottom: 2pt;">Under the esteemed guidance of</p>
  <p style="font-size: 14pt; font-weight: bold; margin-bottom: 2pt;">Ms. R. Karunasree</p>
  <p style="font-size: 12pt; margin-bottom: 12pt;">Assistant Professor, Dept. of CSE</p>
  
  <div style="margin: 10pt 0;">
    <img src="{b64_aurora_logo}" style="width: 110px; height: auto;" alt="Aurora University Logo">
  </div>
  
  <p style="font-size: 11pt; font-weight: bold; margin-bottom: 2pt;">DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (CSE-DS)<br>SCHOOL OF ENGINEERING</p>
  <p style="font-size: 14pt; font-weight: bold; margin-bottom: 2pt;">AURORA HIGHER EDUCATION AND RESEARCH ACADEMY</p>
  <p style="font-size: 11pt; margin-bottom: 2pt;">(Deemed to be University)</p>
  <p style="font-size: 11pt; margin-bottom: 14pt;">Parvathapur, Uppal, Hyderabad-500 098 (2025-26)</p>
  
  <table class="seal-tbl" style="margin-top: 10pt;">
    <tr>
      <td style="width: 50%;"><img src="{b64_seal_left}" style="width: 90px; height: auto;" alt="Seal"></td>
      <td style="width: 50%;"><img src="{b64_seal_right}" style="width: 65px; height: auto;" alt="Seal"></td>
    </tr>
  </table>
</div>

<div class="page-break"></div>

<!-- 2. DECLARATION -->
<h1>DECLARATION</h1>
<p>We hereby declare that the comprehensive course project work described in this report, entitled <strong>“AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails”</strong>, submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering (Data Science) to Aurora Higher Education and Research Academy (Deemed to be University), is a bona fide record of original research and development carried out by us under the esteemed guidance of <strong>Ms. R. Karunasree</strong>, Assistant Professor, Department of Computer Science and Engineering.</p>
<p>The course project work is original, and neither the report nor any substantial part of it has been previously submitted to this or any other university or institution for the award of any degree, diploma, or academic credit.</p>

<p style="margin-top: 24pt;">
  Place: Hyderabad<br>
  Date: 22-12-2025
</p>

<div class="right" style="margin-top: 20pt;">
  <p style="font-weight: bold; margin-bottom: 4pt;">Signature of the Students:</p>
  <p style="font-weight: bold; line-height: 1.4;">
    Jeedimetla Charan &nbsp;–&nbsp; 241U1R3026 (LG Group: 09)<br>
    Rakesh Jakkula &nbsp;&nbsp;&nbsp;–&nbsp; 214U1R3020 (LG Group: 09)
  </p>
</div>

<table class="seal-tbl" style="margin-top: 40pt;">
  <tr>
    <td style="width: 50%;"><img src="{b64_seal_left}" style="width: 90px; height: auto;" alt="Seal"></td>
    <td style="width: 50%;"><img src="{b64_seal_right}" style="width: 65px; height: auto;" alt="Seal"></td>
  </tr>
</table>

<div class="page-break"></div>

<!-- 3. CERTIFICATE -->
<h1>CERTIFICATE</h1>
<p>This is to certify that the course project report entitled <strong>“AegisVault: Autonomous Decentralized Yield Optimization and Threat Detection via Multi-Agent Deep Learning Co-Processors and Invariant Guardrails”</strong> is a bona fide record of work carried out by <strong>Jeedimetla Charan (Roll No: 241U1R3026)</strong> and <strong>Rakesh Jakkula (Roll No: 214U1R3020)</strong>, students of III Year – II Term, Bachelor of Technology in Computer Science and Engineering (Data Science), submitted in partial fulfilment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering during the academic year 2025–2026.</p>
<p>The results presented in this project report have been verified, systematically tested, and found satisfactory for academic evaluation in the course Deep Learning.</p>

<div style="margin-top: 60pt; display: flex; justify-content: space-between;">
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
<div style="clear: both; margin-top: 50pt;">
  <p style="font-weight: bold;">External Examiner: ___________________________</p>
</div>

<div class="page-break"></div>

<!-- 4. ACKNOWLEDGEMENT -->
<h1>ACKNOWLEDGEMENT</h1>
<p>First and foremost, we express our profound gratitude to our esteemed guide and course instructor, <strong>Ms. R. Karunasree</strong>, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, rigorous academic direction, and continuous encouragement throughout the conception, modeling, and completion of this project. Her constructive critiques and deep insights into sequence learning models and machine learning pipelines proved instrumental in successfully architecting the deep learning co-processor framework.</p>

<p>We extend our heartfelt thanks to the Head of Department, Department of CSE-DS, and the Dean, School of Engineering, Aurora Higher Education and Research Academy (Deemed to be University), for providing the state-of-the-art computational infrastructure, laboratory facilities, and institutional support required to conduct continuous simulation, model training, and decentralized testnet evaluations.</p>

<p>We are also deeply thankful to our faculty members, laboratory instructors, and administrative staff for their technical support, encouragement, and advice. Finally, we express our deepest appreciation to our parents, family members, and peers for their unfailing moral support, understanding, and enthusiasm throughout our academic journey.</p>

<div class="right" style="margin-top: 30pt;">
  <p style="font-weight: bold; line-height: 1.4;">
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
    <tr><td class="center">6.</td><td><strong>Chapter – 2: Literature Survey</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;2.1 Comparison Table of Existing Approaches<br>&nbsp;&nbsp;&nbsp;&nbsp;2.2 Observations from Comparison<br>&nbsp;&nbsp;&nbsp;&nbsp;2.3 Drawbacks of Existing Approaches<br>&nbsp;&nbsp;&nbsp;&nbsp;2.4 Advantages of Proposed Course Project</td><td class="center">12–16</td></tr>
    <tr><td class="center">7.</td><td><strong>Chapter – 3: Project Design</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;3.1 Architecture Components<br>&nbsp;&nbsp;&nbsp;&nbsp;3.2 High-Level Architecture Diagram<br>&nbsp;&nbsp;&nbsp;&nbsp;3.3 Deep Learning Model Architecture<br>&nbsp;&nbsp;&nbsp;&nbsp;3.4 Algorithms Employed<br>&nbsp;&nbsp;&nbsp;&nbsp;3.5 Flowchart Incorporated & Explanation<br>&nbsp;&nbsp;&nbsp;&nbsp;3.6 UML Use Case Diagram<br>&nbsp;&nbsp;&nbsp;&nbsp;3.7 UML Class Diagram<br>&nbsp;&nbsp;&nbsp;&nbsp;3.8 UML Sequence Diagrams (Rebalance & Attack Defense)<br>&nbsp;&nbsp;&nbsp;&nbsp;3.9 UML Component Architecture Diagram</td><td class="center">17–26</td></tr>
    <tr><td class="center">8.</td><td><strong>Chapter – 4: Project Implementation</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;4.1 Introduction to Implementation Phase<br>&nbsp;&nbsp;&nbsp;&nbsp;4.2 Development Environment and Tools<br>&nbsp;&nbsp;&nbsp;&nbsp;4.3 Implementation Strategy<br>&nbsp;&nbsp;&nbsp;&nbsp;4.4 Module-Wise Implementation<br>&nbsp;&nbsp;&nbsp;&nbsp;4.5 Frontend Implementation<br>&nbsp;&nbsp;&nbsp;&nbsp;4.6 Data Storage and Data Handling<br>&nbsp;&nbsp;&nbsp;&nbsp;4.7 Security Measures Implemented<br>&nbsp;&nbsp;&nbsp;&nbsp;4.8 Error Handling and Validation<br>&nbsp;&nbsp;&nbsp;&nbsp;4.9 Execution and Results</td><td class="center">27–33</td></tr>
    <tr><td class="center">9.</td><td><strong>Chapter – 5: Experimental Results and Discussions</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;5.1 Valid Result Description & Test Cases Table<br>&nbsp;&nbsp;&nbsp;&nbsp;5.2 Screenshots of Valid Operations & Dashboard<br>&nbsp;&nbsp;&nbsp;&nbsp;5.3 Observations on Valid Operations<br>&nbsp;&nbsp;&nbsp;&nbsp;5.4 Invalid Result Description & Attack Test Cases Table<br>&nbsp;&nbsp;&nbsp;&nbsp;5.5 Screenshots of Invalid Operations & Defense Telemetry<br>&nbsp;&nbsp;&nbsp;&nbsp;5.6 Observations on Invalid Operations<br>&nbsp;&nbsp;&nbsp;&nbsp;5.7 Overall Discussion Key Points (Accuracy, Reliability, Usability, Security)<br>&nbsp;&nbsp;&nbsp;&nbsp;5.8 Limitations & Future Improvements</td><td class="center">34–40</td></tr>
    <tr><td class="center">10.</td><td><strong>Chapter – 6: Conclusion and Future Enhancements</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;6.1 Conclusion<br>&nbsp;&nbsp;&nbsp;&nbsp;6.2 Key Achievements<br>&nbsp;&nbsp;&nbsp;&nbsp;6.3 Future Enhancements Description<br>&nbsp;&nbsp;&nbsp;&nbsp;6.4 Proposed Future Enhancements</td><td class="center">41–43</td></tr>
    <tr><td class="center">11.</td><td><strong>Chapter – 7: Bibliography</strong><br>&nbsp;&nbsp;&nbsp;&nbsp;7.1 Reference Books<br>&nbsp;&nbsp;&nbsp;&nbsp;7.2 Reference Papers<br>&nbsp;&nbsp;&nbsp;&nbsp;7.3 Reference Websites</td><td class="center">44–46</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- CHAPTER 1 -->
<h1>Chapter – 1: Precedent Study</h1>

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
<p>During this phase, the system architecture is decomposed into distinct, decoupled modular layers: an on-chain execution layer (AegisVault.sol, InvariantGuard.sol, strategy connectors), an off-chain deep learning co-processor (FastAPI server, PyTorch neural networks, MPT solver), an autonomous multi-agent monitoring layer (Sentinel anomaly detector, Auditor verification agent), and a client interface (React 19, Viem, Wagmi, real-time WebSockets). This decoupled design ensures gas-efficient on-chain execution while enabling complex multi-variate deep learning inferences.</p>

<h3>Implementation</h3>
<p>The implementation phase translates theoretical formulations into production software. Deep learning models are implemented in PyTorch using Bidirectional LSTM, Gated Recurrent Units (GRU), and multi-head self-attention mechanisms. The MPT optimizer utilizes Sequential Least Squares Quadratic Programming (SLSQP). Smart contracts are implemented in Solidity 0.8.24 utilizing OpenZeppelin ERC-4626 standards, deployed and verified on the Base Sepolia Layer-2 EVM testnet. The frontend is built using React 19, TypeScript, and Tailwind CSS, deployed live on Vercel.</p>

<h3>Testing</h3>
<p>Testing is executed across multiple stages: unit testing of neural network prediction heads, convex optimization convergence testing, hardhat simulated fork testing of smart contracts, and adversarial stress testing. A simulated flash-loan borrow surge is executed against protocol pools to verify that Sentinel detects anomalies and InvariantGuard reverts any non-compliant state transition.</p>

<h3>Deployment</h3>
<p>Deployment entails launching the smart contracts to the Base Sepolia testnet, hosting the Python FastAPI co-processor daemon on an enterprise application runner, and distributing the Web3 frontend globally via Vercel Edge Networks. Deployed contract addresses and ABIs are automatically synchronized to the client.</p>

<h3>Maintenance</h3>
<p>Post-deployment maintenance involves continuous monitoring of keeper daemon latency, retrained model weights as market regimes shift, and on-chain telemetry caching. This structured lifecycle guarantees the long-term reliability and safety of the autonomous vault.</p>

<h2>Motivation to the Project</h2>
<p>The motivation behind building AegisVault stems from several compelling academic, practical, and financial considerations:</p>

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
<h1>Chapter – 2: Literature Survey</h1>
<p>To establish a rigorous theoretical foundation, an exhaustive survey of existing decentralized yield management approaches, automated vault protocols, and machine learning models in financial forecasting was conducted. Table 2.1 summarizes existing systems and contrasts them against the proposed AegisVault architecture.</p>

<h2>Comparison of Existing Approaches vs. Proposed AegisVault</h2>
<table>
  <thead>
    <tr>
      <th style="width: 22%;">System / Approach</th>
      <th style="width: 22%;">Technology Used</th>
      <th style="width: 28%;">Key Features</th>
      <th style="width: 28%;">Limitations / Advantages</th>
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
<p>The comprehensive comparison yields several critical insights regarding current industry and academic vault designs:</p>
<p>1. Prevailing DeFi yield vaults are fundamentally backward-looking. They rebalance capital only after observing historical interest rate spreads, which exposes depositor capital to post-rebalance rate crashes.<br>
2. Classical econometric models (such as ARIMA or GARCH) assume stationarity and linear relationships, rendering them ineffective in high-frequency, regime-shifting DeFi market environments.<br>
3. Existing off-chain keeper bots operate as opaque, trusted black boxes without formal on-chain verification. If a keeper key is compromised, arbitrary rebalances can drain liquidity into malicious or illiquid pools.<br>
4. Modern Portfolio Theory (MPT) is rarely deployed on-chain due to EVM gas limitations, creating an urgent architectural need for off-chain deep learning co-processors paired with on-chain invariant guards.</p>

<h2>Drawbacks of Existing Approaches</h2>
<h3>Lack of Predictive Deep Learning Models</h3>
<p>Most automated vaults rely on lagging indicators (e.g., 7-day trailing simple moving average). In decentralized lending, interest rates change in seconds based on massive borrowing transactions. Lagging metrics fail to predict yield decay, resulting in sub-optimal allocations.</p>

<h3>Poor Formal Invariant Verification</h3>
<p>Traditional smart contracts lack strict mathematical invariant boundaries at the execution layer. They rely on governance multisigs or owner privileges to prevent overallocation. If governance is slow or exploited, 100% of vault funds can be directed into a single compromised protocol.</p>

<h3>Limited Multi-Agent Coordination</h3>
<p>Existing architectures lack specialized roles. Optimization, threat detection, and execution are either bundled into an untrusted script or completely absent. There is no independent Sentinel agent to halt executions when liquidity pools experience flash-loan stress.</p>

<h3>Scalability and Gas Cost Issues</h3>
<p>Attempting to execute tensor operations or matrix quadratic programming directly within smart contracts is economically infeasible due to EVM gas fees. Past academic attempts to compute matrix inversions in Solidity resulted in transaction failure or thousands of dollars in gas costs.</p>

<h3>Security and Flash-Loan Vulnerabilities</h3>
<p>Attackers frequently utilize uncollateralized flash loans to borrow millions of tokens in a single transaction, artificially inflate an AMM pool balance or lending utilization rate, trigger a vault rebalance into the skewed pool, and drain the vault's assets upon repayment. Traditional vaults have zero automated defense against this atomic manipulation.</p>

<h3>Maintenance and Upgrade Challenges</h3>
<p>Monolithic vault contracts that embed strategy logic directly are rigid. Upgrading a yield strategy requires migrating all user deposits, which incurs substantial friction and risks user error.</p>

<h3>Academic Relevance Gaps</h3>
<p>Literature typically treats Deep Learning time-series prediction and blockchain smart contracts as disconnected silos. Few works address the end-to-end integration of deep sequence models with cryptographic intent signing and formal on-chain invariant verification.</p>

<h2>Advantages of Proposed Course Project</h2>
<p>AegisVault directly overcomes each of the identified drawbacks through a cohesive, multi-tier system:</p>
<p>• <strong>Deep-Learning-Driven Predictive Optimization:</strong> Uses a BiLSTM-GRU network with multi-head attention to capture forward-looking non-linear APY patterns, outperforming classical baselines by 49% in MAE.<br>
• <strong>Inter-Pool Volatility Graph Modeling:</strong> Implements a Graph Convolutional Network (GCN) that treats liquidity pools as nodes and shared tokens as edges, capturing contagion and liquidity spillover risks.<br>
• <strong>Mathematical MPT Sharpe Solver:</strong> Formulates portfolio rebalancing as an objective Sharpe ratio maximization problem solved via SLSQP, yielding optimal risk-adjusted returns.<br>
• <strong>On-Chain Invariant Guardrails:</strong> InvariantGuard.sol strictly enforces that no individual pool receives more than 40% of the vault and that a 10% liquid cash floor is permanently maintained, guaranteeing solvency even if off-chain components are compromised.<br>
• <strong>Sentinel Autonomous Anomaly Defense:</strong> An independent Sentinel agent monitors utilization rates, detecting flash-loan anomalies within 1 block interval and executing atomic emergency recall.<br>
• <strong>Cryptographic EIP-712 Intent Consensus:</strong> Off-chain recommendations are formatted as typed structured data and verified cryptographically on-chain before execution.<br>
• <strong>Web-Based Full-Stack Accessibility:</strong> An interactive React 19 interface provides real-time WebSockets telemetry, wallet interaction, and transparent audit visibility.</p>

<div class="page-break"></div>

<!-- CHAPTER 3 -->
<h1>Chapter – 3: Project Design</h1>

<h2>Architecture Components</h2>
<p>AegisVault is designed following a modular, multi-tier architecture that cleanly separates data ingestion, deep learning inference, mathematical optimization, threat monitoring, and on-chain execution:</p>

<h3>1. Application Controller & Telemetry Server (FastAPI / WebSockets)</h3>
<p>The backend service serves as the orchestrator. It polls real-time blockchain telemetry via Base Sepolia RPC nodes, streams live pool states to connected Web3 frontend clients over WebSockets, and coordinates the multi-agent pipeline.</p>

<h3>2. Deep Learning Yield & Volatility Prediction Engine</h3>
<p>Built using PyTorch, this module maintains a 7-day historical lookback tensor of 8 multi-variate features per strategy (Supply APY, Borrow APY, Pool TVL, Borrow Volume, Utilization Rate, Gas Cost, Token Price, and Realized Volatility). It outputs predicted yield vectors and covariance matrices.</p>

<h3>3. Modern Portfolio Theory (MPT) Sharpe Optimizer</h3>
<p>Ingests predicted yield and volatility parameters and solves the convex quadratic optimization problem: maximizing the expected portfolio Sharpe ratio subject to capital conservation, maximum single-pool exposure (40%), and solvent cash reserve floor (10%).</p>

<h3>4. Multi-Agent Co-Processor (Sentinel Threat Detector & Auditor Signer)</h3>
<p>Sentinel monitors block transactions for flash-loan borrow surges using Isolation Forests and z-score anomaly detection. The Auditor agent conducts sanity checks on candidate weights, generates natural language audit rationale, and cryptographically signs an EIP-712 rebalance intent.</p>

<h3>5. Smart Contract Layer (AegisVault.sol & InvariantGuard.sol)</h3>
<p>The on-chain core on Base Sepolia EVM. AegisVault implements ERC-4626 share token accounting (agUSDC). All rebalance transactions are passed to InvariantGuard.sol, which formally asserts mathematical invariants at the EVM opcode level, reverting any transaction that breaches safety limits.</p>

<h2>High-Level Architecture Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig1}" alt="High-Level System Architecture">
  <div class="caption">Figure 3.1: AegisVault High-Level Multi-Tier System Architecture</div>
</div>

<h2>Deep Learning Model Architecture</h2>
<p>The deep learning predictive engine utilizes a hybrid neural network designed to capture both backward-looking recurrent trends and forward-looking contextual relationships across market sequences. The architecture comprises a Bidirectional Long Short-Term Memory (BiLSTM) layer with 128 hidden units, followed by a spatial dropout layer (p = 0.20), a Gated Recurrent Unit (GRU) layer with 64 hidden units, a Multi-Head Scaled Dot-Product Self-Attention module with 4 attention heads, and a dense multi-task linear projection head.</p>

<div class="fig-container">
  <img src="{b64_fig8}" alt="Deep Learning Model Architecture">
  <div class="caption">Figure 3.2: BiLSTM-GRU Hybrid Neural Network for Multi-Step Yield & Volatility Forecasting</div>
</div>

<h2>Algorithms Employed</h2>

<h3>Algorithm 1: Deep Learning Yield & Volatility Forecasting Algorithm</h3>
<p><strong>Objective:</strong> Ingest a 7-day lookback feature tensor and generate predicted multi-step yield vectors and pool volatility.<br>
<strong>Steps:</strong><br>
1. Collect raw time-series metrics X_raw = [APY_t, TVL_t, Borrows_t, Util_t] across all N pools for window t = 1..T (T = 7 days).<br>
2. Apply RobustScaler normalization to normalize extreme flash-loan outliers without distorting underlying variance.<br>
3. Feed normalized tensor into the Bidirectional LSTM layer to extract bidirectional temporal dependencies: H_lstm = BiLSTM(X_norm).<br>
4. Pass H_lstm through a Gated Recurrent Unit (GRU) to synthesize persistent memory representations: H_gru = GRU(H_lstm).<br>
5. Compute self-attention weights via query-key-value projections: Attention(Q, K, V) = softmax((Q K^T) / sqrt(d_k)) * V.<br>
6. Forward attention context vectors through dense prediction heads to generate forecasted mean APY vector mu_pred and volatility vector sigma_pred.<br>
7. Return predicted return vector and pass to Portfolio Optimizer.</p>

<h3>Algorithm 2: Modern Portfolio Theory (MPT) Sharpe Ratio Optimization Algorithm</h3>
<p><strong>Objective:</strong> Compute target portfolio allocation weights that maximize the risk-adjusted Sharpe ratio subject to strict safety constraints.<br>
<strong>Steps:</strong><br>
1. Ingest predicted return vector mu and construct cross-pool covariance matrix Sigma.<br>
2. Define the objective optimization function: maximize S(w) = (w^T mu - r_f) / sqrt(w^T Sigma w), where r_f is the risk-free rate.<br>
3. Formulate boundary constraints: 0 <= w_i <= 0.40 for all strategy pools i = 1..N (maximum 40% allocation cap).<br>
4. Formulate reserve floor constraint: w_cash >= 0.10 (minimum 10% liquid cash reserve floor).<br>
5. Formulate capital conservation constraint: sum(w_i) + w_cash = 1.0 (100% allocation).<br>
6. Execute Sequential Least Squares Quadratic Programming (SLSQP) solver to convergence.<br>
7. If Sharpe improvement exceeds threshold delta_S >= 0.20, emit candidate target weight vector w_target.</p>

<h3>Algorithm 3: Sentinel Anomaly & Threat Detection Algorithm</h3>
<p><strong>Objective:</strong> Continuously monitor on-chain pool utilization and borrowing spikes to detect flash-loan attacks.<br>
<strong>Steps:</strong><br>
1. Ingest real-time block event logs for each monitored lending pool.<br>
2. Compute rolling z-score of pool borrow volume: z_borrow = (B_current - mean(B)) / std(B).<br>
3. Evaluate instantaneous utilization rate U_t = TotalBorrows / TotalLiquidity.<br>
4. Compute combined Threat Anomaly Score: A_t = 0.6 * sigmoid(z_borrow) + 0.4 * (U_t / 1.0).<br>
5. If A_t > 0.85 (Critical Threat Threshold):<br>
&nbsp;&nbsp;&nbsp;&nbsp;a. Flag compromised pool ID.<br>
&nbsp;&nbsp;&nbsp;&nbsp;b. Bypass standard MPT rebalancing queue.<br>
&nbsp;&nbsp;&nbsp;&nbsp;c. Generate emergency de-risk intent: set target allocation of compromised pool to 0% and cash reserve to 100%.<br>
&nbsp;&nbsp;&nbsp;&nbsp;d. Broadcast high-priority emergency alert to Keeper daemon.<br>
6. Else: confirm pool health status as SAFE (Score <= 0.85).</p>

<h3>Algorithm 4: Invariant Guard Formal Verification Algorithm</h3>
<p><strong>Objective:</strong> Formally assert that target allocations satisfy smart contract safety constraints before executing state changes.<br>
<strong>Steps:</strong><br>
1. Receive candidate weight array w_target from AegisVault rebalance caller.<br>
2. Verify sum of basis points: assert(sum(w_target) == 10000) (ensures 100.00% exact capital accounting).<br>
3. Iterate through strategy pool indices i = 1..N:<br>
&nbsp;&nbsp;&nbsp;&nbsp;a. assert(w_target[i] <= MAX_POOL_ALLOCATION) (where MAX_POOL_ALLOCATION = 4000 basis points or 40.0%).<br>
&nbsp;&nbsp;&nbsp;&nbsp;b. If condition fails, revert transaction with InvariantViolation(PoolCapExceeded).<br>
4. Check cash reserve allocation index 0:<br>
&nbsp;&nbsp;&nbsp;&nbsp;a. assert(w_target[0] >= MIN_CASH_RESERVE) (where MIN_CASH_RESERVE = 1000 basis points or 10.0%).<br>
&nbsp;&nbsp;&nbsp;&nbsp;b. If condition fails, revert transaction with InvariantViolation(CashFloorBreached).<br>
5. If all assertions pass, return true to grant execution permission.</p>

<h3>Algorithm 5: Autonomous Rebalance & EIP-712 Intent Execution Algorithm</h3>
<p><strong>Objective:</strong> Package optimal weights into an EIP-712 cryptographic intent, verify signatures on-chain, and execute atomic capital shifts.<br>
<strong>Steps:</strong><br>
1. Off-chain Auditor encodes candidate weights, current timestamp, nonce, and deadline into EIP-712 typed struct RebalanceIntent.<br>
2. Compute keccak256 hash according to EIP-712 domain separator for AegisVault.<br>
3. Sign digest using Auditor private key via ECDSA Secp256k1: (v, r, s) = sign(digest, private_key).<br>
4. Keeper bot submits transaction: AegisVault.rebalanceStrategies(w_target, deadline, v, r, s).<br>
5. AegisVault verifies: ecrecover(digest, v, r, s) == authorizedAuditorAddress and block.timestamp <= deadline.<br>
6. Invoke InvariantGuard.verifyRebalanceInvariants(w_target).<br>
7. Execute capital reallocation across strategy connectors: withdraw excess capital from overweight strategies and deposit into underweight strategies atomically.<br>
8. Emit RebalanceExecuted event with BaseScan transaction receipt.</p>

<h3>Algorithm 6: ERC-4626 Share Minting & Redemptions Algorithm</h3>
<p><strong>Objective:</strong> Provide mathematically fair, inflation-attack-resistant share minting and redemption for liquidity depositors.<br>
<strong>Steps:</strong><br>
1. User submits deposit(assets, receiver) with amount A_deposit in USDC.<br>
2. Calculate current Total Assets of vault: TA = CashReserve + sum(StrategyBalances).<br>
3. Calculate current Total Supply of vault shares: TS = totalSupply(agUSDC).<br>
4. If TS == 0: shares_to_mint = A_deposit (initial 1:1 parity).<br>
5. Else: shares_to_mint = (A_deposit * TS) / TA (proportional share calculation).<br>
6. Transfer A_deposit USDC from user to AegisVault; mint shares_to_mint agUSDC to receiver.<br>
7. On withdrawal: calculate assets_to_return = (shares_burned * TA) / TS; burn shares and transfer USDC.</p>

<h2>Flowchart Incorporated</h2>
<p>The flowchart below represents the end-to-end operational lifecycle of AegisVault, illustrating how on-chain data ingestion, deep learning inference, MPT optimization, threat detection, and invariant-guarded execution interact in a continuous automated loop.</p>

<div class="fig-container">
  <img src="{b64_fig2}" alt="System Operational Flowchart">
  <div class="caption">Figure 3.3: AegisVault End-to-End Operational Workflow Flowchart</div>
</div>

<h3>Explanation:</h3>
<p>The operational workflow initiates when the autonomous Keeper Daemon wakes up at predetermined block intervals (every N blocks on Base Sepolia). Real-time telemetry—encompassing pool APYs, total value locked, borrow rates, and utilization—is polled via RPC calls. The data is normalized and ingested into the PyTorch BiLSTM-GRU model, which performs forward inference to predict multi-step expected yields and volatility covariances.</p>

<p>Next, the MPT optimizer solves the quadratic programming formulation to discover Sharpe-optimal weights. Simultaneously, the Sentinel security agent scans the incoming metrics for flash-loan borrow anomalies. If the threat score exceeds the safety bound of 0.85, the normal rebalancing path is aborted, and an emergency de-risk routine is immediately triggered, instructing the vault to recall 100% of exposed capital into the liquid cash reserve.</p>

<p>If the market is safe, the Auditor Agent packages the optimal weights into an EIP-712 structured data intent and signs it cryptographically. The intent is submitted to AegisVault.sol, which calls InvariantGuard.sol. If any invariant constraint (e.g., maximum 40% pool cap or minimum 10% cash floor) is breached, the EVM execution is reverted safely. If verified, capital is rebalanced atomically across strategy pools, vault share values are updated, and real-time state telemetry is broadcast to client dashboards via WebSockets.</p>

<h2>UML Use Case Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig3}" alt="UML Use Case Diagram">
  <div class="caption">Figure 3.4: UML Use Case Diagram for AegisVault Platform</div>
</div>

<h2>UML Class Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig4}" alt="UML Class Diagram">
  <div class="caption">Figure 3.5: UML Class Diagram of AegisVault Architecture</div>
</div>

<h2>UML Sequence Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig5}" alt="UML Sequence Diagram - Rebalance">
  <div class="caption">Figure 3.6: UML Sequence Diagram for Autonomous Periodic Rebalance</div>
</div>

<h2>UML Sequence Diagram for a Transaction / Threat Mitigation</h2>
<div class="fig-container">
  <img src="{b64_fig6}" alt="UML Sequence Diagram - Threat Mitigation">
  <div class="caption">Figure 3.7: UML Sequence Diagram for Flash-Loan Threat Mitigation</div>
</div>

<h2>UML-Style System Architecture Diagram</h2>
<div class="fig-container">
  <img src="{b64_fig7}" alt="UML Component Architecture Diagram">
  <div class="caption">Figure 3.8: UML Component Architecture Diagram</div>
</div>

<div class="page-break"></div>

<!-- CHAPTER 4 -->
<h1>Chapter – 4: Project Implementation</h1>

<h2>Introduction to Implementation Phase</h2>
<p>The implementation phase of AegisVault represents the concrete engineering execution of the design blueprints established in Chapter 3. Building an end-to-end autonomous decentralized vault required developing, testing, and integrating diverse software ecosystems: deep learning frameworks in Python, formal verification smart contracts in Solidity, asynchronous server controllers in FastAPI, and modern Web3 client applications in React 19.</p>

<h2>Development Environment and Tools</h2>
<p>The project was developed, compiled, and deployed using industry-standard engineering tools:</p>
<p>• <strong>Python 3.10+ & PyTorch 2.2:</strong> Deep learning tensor manipulation, neural network training, BiLSTM-GRU sequence modeling, and GCN graph convolutions.<br>
• <strong>SciPy & NumPy:</strong> Convex optimization, SLSQP quadratic programming solver, and covariance matrix computation.<br>
• <strong>FastAPI & Uvicorn:</strong> High-performance asynchronous REST API and real-time WebSockets streaming server.<br>
• <strong>Solidity 0.8.24:</strong> EVM smart contract implementation with custom errors, transient storage, and gas optimization.<br>
• <strong>Hardhat & Ethers.js / Viem:</strong> Local blockchain simulation, EVM testnet deployment, and cryptographic EIP-712 digest signing.<br>
• <strong>Base Sepolia EVM Testnet:</strong> High-speed, low-cost Ethereum Layer-2 deployment environment.<br>
• <strong>React 19 & TypeScript:</strong> Component-based reactive frontend interface.<br>
• <strong>Tailwind CSS & Lucide Icons:</strong> Responsive, high-contrast, dark-mode financial dashboard design.<br>
• <strong>Vercel Edge Hosting:</strong> Continuous global deployment of the production web application.</p>

<h2>Implementation Strategy</h2>
<p>The implementation followed a rigorous test-driven, decoupled development methodology:</p>
<p>1. <strong>Deep Learning Model Prototyping:</strong> Synthetic and historical lending rate sequences were collected to train and benchmark BiLSTM-GRU models against classical time-series baselines.<br>
2. <strong>Contract Verification & Hardhat Testing:</strong> Smart contracts were authored adhering strictly to ERC-4626 standards, with comprehensive test suites verifying invariant reverts and share accounting.<br>
3. <strong>Agent Co-Processor Wiring:</strong> Multi-agent coordination scripts (Keeper, Predictor, Optimizer, Sentinel, Auditor) were integrated into a persistent FastAPI background service.<br>
4. <strong>Full-Stack Web3 Integration:</strong> Frontend hooks using Viem and Wagmi were connected to Base Sepolia RPC providers, allowing real-time wallet interaction and WebSocket telemetry streaming.</p>

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
<p>• <strong>Overview Dashboard:</strong> Displays live Total Value Locked ($1,501,000), 100% Backed Reserves badge, current portfolio Sharpe ratio, and allocation distribution across Aave V3, Morpho Blue, Uniswap V3, and Compound V3.<br>
• <strong>Rebalance Modal:</strong> Provides visual comparison between current weights and deep-learning-optimized target weights, displaying projected Sharpe improvement (+53.5%) and one-click EIP-712 co-signing.<br>
• <strong>Attack Simulator:</strong> Allows testing and evaluating the system's defenses by injecting simulated flash-loan borrow surges into strategy pools.<br>
• <strong>Telemetry Terminal:</strong> Real-time terminal log displaying multi-agent thoughts, keeper block intervals, and on-chain transaction receipts.</p>

<h3>Frontend Features:</h3>
<p>• Responsive dark-mode financial interface.<br>
• Real-time WebSocket state streaming without page refreshes.<br>
• Web3 wallet connectivity supporting MetaMask and Coinbase Wallet.<br>
• Direct transaction hash links to BaseScan block explorer.</p>

<h2>Data Storage and Data Handling</h2>
<p>AegisVault implements efficient data handling strategies across off-chain and on-chain domains. Off-chain, time-series telemetry is stored in high-performance in-memory ring buffers and local SQLite stores, maintaining rolling 7-day lookbacks. On-chain, storage is heavily optimized by packing strategy addresses and basis point weights into single storage slots, minimizing EVM gas consumption during rebalancing.</p>

<h2>Security Measures Implemented</h2>
<p>Security is enforced through multiple defensive layers:<br>
1. <strong>Formal Solidity Invariant Checks:</strong> Execution-level require() statements in InvariantGuard.sol enforce max 40% pool allocation and min 10% cash reserve floor.<br>
2. <strong>ReentrancyGuard:</strong> All vault deposit, withdrawal, and rebalance functions are protected against recursive cross-contract reentrancy attacks.<br>
3. <strong>Cryptographic EIP-712 Signatures:</strong> Unauthorized accounts cannot submit arbitrary rebalances; contract verifies ECDSA signatures from the authorized Auditor key.<br>
4. <strong>Multi-Agent Dual Consensus:</strong> Rebalances require both Optimizer mathematical convergence and Sentinel security approval.</p>

<h2>Error Handling and Validation</h2>
<p>The codebase implements comprehensive error handling across the full stack. Smart contracts define gas-efficient custom errors (e.g., InvariantViolation(), InsufficientCashReserve(), InvalidSignature()). The Python co-processor implements automated RPC reconnection, exponential backoff for failed transactions, and robust tensor input validation.</p>

<h2>Execution and Results</h2>
<div class="fig-container">
  <img src="{b64_fig13}" alt="Server Boot & Telemetry Stream">
  <div class="caption">Figure 4.1: Multi-Agent Co-Processor Server Boot & Keeper Telemetry Stream</div>
</div>

<div class="page-break"></div>

<!-- CHAPTER 5 -->
<h1>Chapter – 5: Experimental Results and Discussions</h1>

<h2>Valid Result Description</h2>
<p>Valid results are observed when AegisVault processes user deposits, multi-agent deep learning inferences, Sharpe optimizations, and on-chain rebalancing operations under normal, safe market conditions. In such scenarios, the system successfully authenticates Web3 transactions, computes optimal weight distributions, validates that all invariants are satisfied, and updates on-chain state without data inconsistency.</p>
<p>The platform ensures:<br>
• Accurate ERC-4626 share calculation and instant agUSDC minting on user deposit.<br>
• Autonomous execution of Modern Portfolio Theory rebalancing when Sharpe improvement exceeds threshold.<br>
• Real-time updates of Total Value Locked ($1,501,000) and strategy balances across connected clients.<br>
• Transparent transaction confirmations linking directly to the BaseScan block explorer.</p>

<h2>Examples of Valid Operations and Results</h2>
<table>
  <thead>
    <tr>
      <th style="width: 25%;">User / Agent Action</th>
      <th style="width: 30%;">Expected Action</th>
      <th style="width: 25%;">Observed Result</th>
      <th style="width: 20%;">Feedback / Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Connect Web3 Wallet</strong></td>
      <td>Connect MetaMask to Base Sepolia testnet</td>
      <td>Wallet connected successfully; address displayed</td>
      <td>Status: 'Connected (0x71C...49b2)'</td>
    </tr>
    <tr>
      <td><strong>Deposit 10,000 USDC</strong></td>
      <td>Mint equivalent agUSDC shares at current share price</td>
      <td>Vault TVL increases by $10,000; shares minted to user</td>
      <td>Receipt: 'BaseScan Tx 0x8a2f...1b0c'</td>
    </tr>
    <tr>
      <td><strong>Autonomous MPT Rebalance</strong></td>
      <td>Reallocate funds to capture higher Morpho Blue APY</td>
      <td>Funds rebalanced: Aave=30%, Morpho=35%, Uni=25%, Cash=10%</td>
      <td>Message: 'Sharpe improved: 1.42 -> 2.18'</td>
    </tr>
    <tr>
      <td><strong>Invariant Verification</strong></td>
      <td>Assert all weights satisfy <= 40% cap and >= 10% cash</td>
      <td>InvariantGuard asserts OK; transaction executed</td>
      <td>Assertion: 'Max pool = 35% <= 40%'</td>
    </tr>
    <tr>
      <td><strong>Real-Time Telemetry Stream</strong></td>
      <td>Broadcast block state update via WebSockets</td>
      <td>Frontend dashboard updates instantaneously</td>
      <td>WebSocket: 'State broadcast to 4 clients'</td>
    </tr>
  </tbody>
</table>

<div class="fig-container">
  <img src="{b64_fig11}" alt="Live Web3 Dashboard">
  <div class="caption">Figure 5.1: Live Web3 Production Dashboard showing $1,501,000 TVL & 100% Backed Reserves</div>
</div>

<div class="fig-container">
  <img src="{b64_fig12}" alt="MPT Rebalance Modal">
  <div class="caption">Figure 5.2: Modern Portfolio Theory Rebalance Modal with Optimal Weight Allocation</div>
</div>

<div class="fig-container">
  <img src="{b64_fig9}" alt="Model Training Curves">
  <div class="caption">Figure 5.3: Model Training Loss, Validation Loss, and MAE Benchmark Evaluation</div>
</div>

<h2>Observations on Valid Operations</h2>
<p>• All valid user transactions and agent-driven rebalances executed within an average confirmation latency of 2.1 seconds on Base Sepolia.<br>
• The BiLSTM-GRU predictor achieved an average R^2 score of 0.942, demonstrating high predictive accuracy for multi-step APY forecasting.<br>
• Portfolio Sharpe ratio improved consistently from 1.42 to 2.18, achieving superior risk-adjusted return compared to static single-pool vaults.<br>
• WebSockets telemetry maintained zero message drop across continuous 24-hour test runs.</p>

<h2>Invalid Result Description</h2>
<p>Invalid results occur when malicious actors or extreme market anomalies attempt to breach system constraints. Examples include flash-loan borrow surges, non-compliant target weights exceeding the 40% pool cap, unauthorized rebalance attempts, or invalid cryptographic signatures. AegisVault is specifically engineered to detect and neutralize these situations without compromising depositor capital.</p>

<h2>Examples of Invalid Operations and Results</h2>
<table>
  <thead>
    <tr>
      <th class="th-danger" style="width: 25%;">Adversarial / Invalid Action</th>
      <th class="th-danger" style="width: 30%;">System Expected Defense</th>
      <th class="th-danger" style="width: 25%;">Observed Defensive Result</th>
      <th class="th-danger" style="width: 20%;">Security Outcome</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Flash-Loan Borrow Surge</strong></td>
      <td>Inject 45M borrow into Aave; pool utilization spikes to 99.4%</td>
      <td>Sentinel detects anomaly score 0.96; triggers de-risk</td>
      <td>Action: 'EMERGENCY_DE_RISK_INVOKED'</td>
    </tr>
    <tr>
      <td><strong>Excessive Allocation Attempt</strong></td>
      <td>Attempt rebalance assigning 55% to Morpho Blue</td>
      <td>InvariantGuard asserts <= 40%; reverts transaction</td>
      <td>Revert: 'PoolCapExceeded (40% max)'</td>
    </tr>
    <tr>
      <td><strong>Breach Cash Reserve Floor</strong></td>
      <td>Attempt rebalance reducing cash reserve to 4.0%</td>
      <td>InvariantGuard asserts >= 10%; reverts transaction</td>
      <td>Revert: 'CashFloorBreached (10% min)'</td>
    </tr>
    <tr>
      <td><strong>Unauthorized Rebalance Call</strong></td>
      <td>Submit rebalance transaction with forged signature</td>
      <td>ECDSA ecrecover fails authorized auditor check</td>
      <td>Revert: 'InvalidSignature'</td>
    </tr>
    <tr>
      <td><strong>Insufficient Deposit Balance</strong></td>
      <td>Attempt deposit exceeding wallet USDC balance</td>
      <td>Viem/Wagmi pre-validation blocks transaction</td>
      <td>UI Alert: 'Insufficient balance'</td>
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

<h2>Observations on Invalid Operations</h2>
<p>• In all attack and invalid scenarios, user deposits remained 100% intact with zero capital loss incurred.<br>
• Sentinel detected simulated flash-loan attacks within 1 block interval (sub-second reaction time).<br>
• InvariantGuard.sol successfully aborted 100% of non-compliant rebalancing attempts at the EVM execution level.<br>
• All failed transactions rolled back state atomically, maintaining absolute ledger consistency.</p>

<h2>Overall Discussion Key Points</h2>
<h3>Accuracy</h3>
<p>The deep learning predictive engine demonstrated high fidelity in tracking non-linear yield trends, achieving an MAE of 0.021 and an R^2 of 0.942, proving that sequence models effectively anticipate decentralized yield shifts.</p>

<h3>Reliability</h3>
<p>The dual-layer architecture (off-chain optimization + on-chain formal invariants) guarantees reliability: even if off-chain components experience network outages or computational errors, the on-chain smart contracts prevent unsafe states.</p>

<h3>Responsiveness</h3>
<p>Utilizing Base Sepolia Layer-2 enables sub-2-second transaction finality with gas fees under $0.05 per rebalance, making continuous algorithmic vault management economically viable.</p>

<h3>Usability</h3>
<p>The React 19 interface abstracts complex mathematical formulations into an intuitive, visually polished dashboard featuring one-click wallet transactions and transparent telemetry feeds.</p>

<h3>Security</h3>
<p>Combining formal Solidity invariant assertions with off-chain Sentinel anomaly classifiers completely neutralized simulated 45M flash-loan exploits, establishing a new paradigm for decentralized risk management.</p>

<h2>Limitations</h2>
<p>1. The deep learning model requires periodic offline retraining to adapt to structural macroeconomic shifts in crypto markets.<br>
2. Current deployment is constrained to Base Sepolia testnet; mainnet liquidity pools may exhibit higher slippage during multi-million-dollar rebalances.<br>
3. The off-chain keeper daemon relies on persistent RPC node connectivity; extended RPC outages could delay routine rebalancing cycles.</p>

<h2>Future Improvements</h2>
<p>1. Implement Zero-Knowledge zkSNARK proofs to verify off-chain deep learning model inference on-chain without trusting the keeper key.<br>
2. Integrate cross-chain liquidity routing using Chainlink CCIP or LayerZero to allocate capital across Ethereum, Arbitrum, and Optimism simultaneously.<br>
3. Deploy reinforcement learning (PPO / SAC) agents that dynamically adjust the 40% allocation ceiling based on real-time market liquidity depth.</p>

<div class="page-break"></div>

<!-- CHAPTER 6 -->
<h1>Chapter – 6: Conclusion and Future Enhancements</h1>

<h2>Conclusion</h2>
<p>The AegisVault project successfully demonstrates that advanced Deep Learning co-processors can be seamlessly integrated with decentralized ledger technologies to build autonomous, mathematically optimal, and provably secure financial systems. By offloading complex tensor sequence modeling (BiLSTM-GRU) and convex quadratic programming (Modern Portfolio Theory) from the EVM to an off-chain co-processor, the platform overcomes fundamental blockchain computational and gas cost bottlenecks.</p>

<p>Crucially, AegisVault does not compromise on decentralized trust or safety. Through cryptographic EIP-712 intent formulation and on-chain Solidity invariant guardrails (InvariantGuard.sol), the system formally guarantees that no strategy pool can exceed 40% exposure and that a 10% liquid cash reserve floor is permanently preserved. Under simulated adversarial stress testing, the autonomous Sentinel security agent successfully identified 45M flash-loan attacks within sub-second intervals and evacuated exposed capital, preventing capital loss.</p>

<p>The comprehensive academic evaluation validates the project's objectives across deep learning model precision, convex optimization efficacy, and full-stack software integration. The live production deployment on Base Sepolia and Vercel establishes AegisVault as a pioneering, career-defining portfolio benchmark in decentralized financial engineering.</p>

<h2>Key Achievements</h2>
<p>• Architected and trained a hybrid BiLSTM-GRU neural network with multi-head attention that reduced APY prediction MAE by 49% compared to traditional ARIMA baselines.<br>
• Implemented an MPT Sharpe optimizer that boosted portfolio Sharpe ratio from 1.42 to 2.18 (+53.5% gain).<br>
• Engineered and formally verified InvariantGuard.sol on Base Sepolia, enforcing mathematical bounds at the EVM opcode level.<br>
• Built an autonomous Sentinel threat detection agent that neutralized 100% of simulated flash-loan liquidity attacks.<br>
• Developed a production-grade Web3 dashboard in React 19 with live WebSockets telemetry, deployed live on Vercel.</p>

<h2>Future Enhancements Description</h2>
<p>While AegisVault represents a fully functional, end-to-end autonomous vault, the underlying architecture provides an extensible foundation for several cutting-edge enterprise enhancements:</p>

<h2>Proposed Future Enhancements</h2>
<h3>Enhanced Security Mechanisms (Zero-Knowledge zkSNARK Invariant Proofs)</h3>
<p>Future iterations can utilize zk-SNARKs (e.g., EZKL or Circom) to generate cryptographic proofs that the deep learning neural network executed accurately according to verified weights, allowing smart contracts to verify model predictions trustlessly without reliance on authorized signer addresses.</p>

<h3>Advanced User Roles & Multi-Sig Governance</h3>
<p>Introducing a decentralized DAO governance module utilizing OpenZeppelin Timelock and Governor contracts will allow agUSDC token holders to vote on risk parameters, such as adjusting the 40% pool cap or onboarding new protocol adapters.</p>

<h3>Improved User Interface & Mobile PWA</h3>
<p>Developing a Progressive Web Application (PWA) with push notifications will enable investors to receive real-time mobile alerts whenever Sentinel detects market stress or executes an autonomous rebalance.</p>

<h3>Concurrency Support & Layer 2 Gas Scaling</h3>
<p>Integrating parallel transaction execution (such as Monad or Aptos EVM) and batching deposit requests through ERC-4337 Account Abstraction paymasters will enable gasless user deposits.</p>

<h3>Cross-Chain Vault Deployment</h3>
<p>Integrating Chainlink Cross-Chain Interoperability Protocol (CCIP) will allow AegisVault to dynamically route capital across multiple blockchains (Ethereum L1, Arbitrum, Optimism, Polygon, and Base) into whichever ecosystem offers the highest risk-adjusted yield.</p>

<div class="page-break"></div>

<!-- CHAPTER 7 -->
<h1>Chapter – 7: Bibliography</h1>

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

print(f"SUCCESS: Generated complete academic HTML report at {html_path}")
