from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from common import  add_p, add_h1, add_h2, add_h3, add_img, apply_ref_table_style

def build_chapter3_docx(doc):
    add_h2(doc, "Chapter – 3: Project Design", sp_before=14, sp_after=8)

    add_h3(doc, "3.1 Architecture Components")
    add_p(doc, "The architectural framework of AegisVault is engineered as a decoupled, asynchronous multi-agent co-processor system interfacing with an EVM-compatible decentralized ledger (Base Sepolia). The architecture comprises six specialized functional components:")
    add_p(doc, "1. Autonomous Keeper Daemon (keeper.py): A persistent background scheduler that polls on-chain state, aggregates real-time market data across target lending pools at block-interval cadences, and initiates predictive evaluations.")
    add_p(doc, "2. Deep Learning Predictor Engine (predictor.py): A neural co-processor powered by PyTorch, executing a hybrid BiLSTM-GRU network with Multi-Head Self-Attention and Graph Convolutional Networks (GCN) to forecast multi-step APYs and cross-pool risk matrices.")
    add_p(doc, "3. Convex Portfolio Optimizer (optimizer.py): A quantitative mathematical solver executing Sequential Least Squares Programming (SLSQP) to maximize the annualized Sharpe ratio subject to non-linear variance and liquidity constraints.")
    add_p(doc, "4. Autonomous Sentinel Threat Daemon (sentinel.py): An asynchronous security monitoring engine utilizing multivariate Isolation Forests and Z-score thresholding to detect flash-loan borrow surges and trigger sub-second de-risking routines.")
    add_p(doc, "5. Cryptographic Auditor Agent (auditor.py): A security validation layer that verifies candidate portfolio allocations against invariant rules, generates EIP-712 typed structured intents, and signs payloads with an authorized ECDSA private key.")
    add_p(doc, "6. Smart Contract Suite (AegisVault.sol & InvariantGuard.sol): On-chain smart contracts implementing the ERC-4626 vault token standard, verifying EIP-712 cryptographic signatures, and enforcing opcode-level safety invariants.")

    add_h3(doc, "3.2 High-Level Architecture Diagram")
    add_p(doc, "Figure 3.1 illustrates the end-to-end operational interaction between the decentralized Web3 client interface, the off-chain Python multi-agent co-processor, and the on-chain smart contract ecosystem deployed on the Base Sepolia network.")
    add_img(doc, "fig1_high_level_architecture.png", width=Inches(4.8),
            caption="Figure 3.1: High-Level System Architecture of AegisVault.")
    add_p(doc, "As depicted in Figure 3.1, users interact with the vault through a modern Web3 client interface. The Keeper Daemon initiates scheduled rebalancing cycles by retrieving pool states via JSON-RPC. The Predictor and Optimizer agents derive Sharpe-optimal weights, which the Auditor Agent signs via EIP-712. The signed intent is relayed to AegisVault.sol, which invokes InvariantGuard.sol to formally verify all allocation bounds before updating strategy balances.")

    add_h3(doc, "3.3 Deep Learning Model Architecture")
    add_p(doc, "To accurately model the extreme stochasticity and non-linear regime shifts inherent in decentralized lending rates, the deep learning predictive engine integrates three neural processing stages: Bidirectional Sequence Modeling, Multi-Head Self-Attention, and Spatial Graph Convolutions.")
    add_img(doc, "fig8_dl_model_architecture.png", width=Inches(4.8),
            caption="Figure 3.2: Deep Learning BiLSTM-GRU & Attention Neural Network Architecture.")

    add_p(doc, "Mathematical Formulation and Equation Derivations:")
    add_p(doc, "The input to the network is a 3D tensor X in R^{B x T x D}, where batch size B = 32, lookback window T = 168 hours (7 days), and feature dimension D = 8. For each lending pool i at time t, the feature vector x_{i,t} comprises: [APY, Utilization Rate, Borrow Velocity, Total Value Locked, Liquidity Reserve Ratio, Pool Imbalance Index, Volatility Trend, Gas Price Impact].")

    add_p(doc, "1. Bidirectional LSTM Layer: The first recurrent stage processes input sequences in both forward and backward temporal directions to capture past context and anticipatory market shifts:")
    add_p(doc, "Forward pass: h_{t}^{(f)} = LSTM_{fwd}(x_t, h_{t-1}^{(f)}) in R^{128}\n"
          "Backward pass: h_{t}^{(b)} = LSTM_{bwd}(x_t, h_{t+1}^{(b)}) in R^{128}\n"
          "Concatenated output: h_t^{(1)} = [h_{t}^{(f)}; h_{t}^{(b)}] in R^{256}")

    add_p(doc, "2. Gated Recurrent Unit (GRU) Layer: The concatenated representations are routed into a 128-dimensional GRU layer to refine temporal state transitions with efficient parameterization:")
    add_p(doc, "Reset gate: r_t = sigma(W_r h_t^{(1)} + U_r s_{t-1} + b_r)\n"
          "Update gate: z_t = sigma(W_z h_t^{(1)} + U_z s_{t-1} + b_z)\n"
          "Candidate state: s_tilde_t = tanh(W_s h_t^{(1)} + U_s (r_t dot s_{t-1}) + b_s)\n"
          "Hidden state: s_t = (1 - z_t) dot s_{t-1} + z_t dot s_tilde_t in R^{128}")

    add_p(doc, "3. Multi-Head Self-Attention Mechanism: A 4-head self-attention module allows the model to dynamically weight critical past shock events (e.g., sudden borrowing spikes) across the 168-hour temporal receptive field:")
    add_p(doc, "Q = S W_Q,  K = S W_K,  V = S W_V   (where W_Q, W_K, W_V in R^{128 x 128})\n"
          "Head_i = Attention(Q_i, K_i, V_i) = softmax((Q_i K_i^T) / sqrt(d_k)) V_i\n"
          "MultiHead(S) = [Head_1; Head_2; Head_3; Head_4] W_O in R^{128}")

    add_p(doc, "4. Graph Convolutional Network (GCN) Covariance Modeling: To capture cross-pool liquidity contagion, inter-protocol lending dependencies are structured as a graph G = (V, E, A), where nodes V represent the 4 lending pools and adjacency matrix A encodes inter-pool asset correlations. Spatial propagation is defined as:")
    add_p(doc, "H^{(l+1)} = ReLU(D_tilde^{-1/2} A_tilde D_tilde^{-1/2} H^{(l)} W_{GCN}^{(l)})\n"
          "where A_tilde = A + I_N is the adjacency matrix with added self-loops, and D_tilde is the degree matrix.")

    add_p(doc, "5. Composite Multi-Task Loss Function: The model is trained end-to-end utilizing a combined objective function comprising Huber Loss for robust yield forecasting and Frobenius Covariance Loss:")
    add_p(doc, "L_{total} = L_{Huber}(mu_hat, mu) + lambda_1 ||Sigma_hat - Sigma||_F^2 + lambda_2 ||Theta||_2^2\n"
          "where Huber loss prevents outlier distortion from flash borrowing spikes, and L2 weight decay enforces generalization.")

    add_h3(doc, "3.4 Algorithms Employed (Algorithms 1 to 8)")
    add_p(doc, "The autonomous operation of AegisVault is governed by eight formal, mathematically defined algorithms spanning off-chain deep learning inference, quantitative convex optimization, cryptographic signing, and on-chain invariant enforcement.")

    # Algorithm 1
    add_h3(doc, "Algorithm 1: BiLSTM-GRU Multi-Step APY and Covariance Forecasting")
    add_p(doc, "Input: Historical 7-day rolling multivariate market tensor X in R^{B x 168 x 8}.\n"
          "Output: Forward predicted yield vector mu_hat in R^N and cross-pool covariance matrix Sigma_hat in R^{N x N}.\n"
          "Steps:\n"
          "1. Normalize tensor features using rolling z-score standardization: X_norm = (X - mu_roll) / sigma_roll.\n"
          "2. Execute forward and backward LSTM passes to compute bidirectional context tensor H_1 in R^{B x 168 x 256}.\n"
          "3. Pass H_1 through GRU recurrent layer to yield temporal feature representation S in R^{B x 168 x 128}.\n"
          "4. Compute Multi-Head Self-Attention over S: A_out = MultiHeadAttention(Q, K, V).\n"
          "5. Route pool representations through GCN layer with adjacency matrix A_tilde to model spatial liquidity contagion.\n"
          "6. Project pooled latent representations through dual dense linear heads to yield predicted APYs mu_hat and covariance Sigma_hat.\n"
          "7. Return mu_hat and Sigma_hat to the Portfolio Optimizer.")

    # Algorithm 2
    add_h3(doc, "Algorithm 2: Convex Quadratic MPT Optimization under EVM Invariant Constraints")
    add_p(doc, "Input: Predicted yield vector mu_hat in R^N, covariance matrix Sigma_hat in R^{N x N}, risk-free rate r_f = 0.02, cash floor c_min = 0.10, pool cap w_max = 0.40.\n"
          "Output: Sharpe-optimal allocation vector w* in R^{N+1}.\n"
          "Steps:\n"
          "1. Formulate objective function: Maximize S(w) = (w^T mu_hat - r_f) / sqrt(w^T Sigma_hat w).\n"
          "2. Reformulate into convex quadratic minimization: Minimize f(w) = 0.5 * w^T Sigma_hat w - gamma * w^T mu_hat.\n"
          "3. Define equality constraint: sum_{i=1}^N w_i + w_{cash} = 1.0.\n"
          "4. Define inequality bounds: 0.0 <= w_i <= 0.40 for all strategies i in {1, ..., N}.\n"
          "5. Define cash reserve inequality constraint: w_{cash} >= 0.10.\n"
          "6. Solve constrained optimization via Sequential Least Squares Programming (SLSQP).\n"
          "7. Validate that candidate weights strictly satisfy sum(w) == 1.0 and bounds within epsilon = 1e-6.\n"
          "8. Output optimal allocation vector w*.")

    # Algorithm 3
    add_h3(doc, "Algorithm 3: Sentinel Autonomous Flash-Loan Anomaly Detection & Emergency De-Risk")
    add_p(doc, "Input: Live mempool stream, pool utilization rates U_i, borrow velocity V_borrow, APY crash metric.\n"
          "Output: Emergency de-risk trigger status and urgent capital recall directive.\n"
          "Steps:\n"
          "1. Compute real-time utilization z-score: z_U = (U_i - mu_{U,i}) / sigma_{U,i}.\n"
          "2. Compute borrow velocity spike ratio: R_borrow = Delta Borrow_i(1 block) / TVL_i.\n"
          "3. Evaluate anomaly condition: If z_U > 3.0 OR R_borrow > 0.35 OR APY_drop > 80%:\n"
          "4.     Flag severe flash-loan liquidity drainage exploit.\n"
          "5.     Bypass standard Keeper scheduling queues immediately.\n"
          "6.     Construct Emergency Recall Payload: Set target vulnerable pool weight w_i = 0.0, cash weight w_{cash} = 1.0.\n"
          "7.     Transmit high-priority signed transaction to AegisVault.sol via dedicated fast RPC relayer.\n"
          "8.     Broadcast security telemetry to WebSocket clients within 420 milliseconds.")

    # Algorithm 4
    add_h3(doc, "Algorithm 4: Cryptographic EIP-712 Typed Intent Generation & ECDSA Verification")
    add_p(doc, "Input: Target allocation weights w*, nonce, expiration timestamp, vault domain separator.\n"
          "Output: Cryptographically signed intent struct and ECDSA signature (v, r, s).\n"
          "Steps:\n"
          "1. Construct EIP-712 Domain Separator: HASH(EIP712Domain(name, version, chainId, verifyingContract)).\n"
          "2. Construct RebalanceIntent TypeHash: HASH('RebalanceIntent(uint256[] weights,uint256 nonce,uint256 deadline)').\n"
          "3. Pack and hash intent payload: structHash = keccak256(abi.encode(TypeHash, keccak256(weights), nonce, deadline)).\n"
          "4. Generate digest: digest = keccak256(abi.encodePacked('\\x19\\x01', DomainSeparator, structHash)).\n"
          "5. Sign digest off-chain using Auditor ECDSA private key to yield (v, r, s).\n"
          "6. On-chain (AegisVault.sol): Verify ecrecover(digest, v, r, s) == authorizedAuditor.\n"
          "7. Verify deadline >= block.timestamp and nonce == currentNonce++.")

    # Algorithm 5
    add_h3(doc, "Algorithm 5: InvariantGuard Formal Invariant Assertion & EVM Opcode Revert")
    add_p(doc, "Input: Candidate strategy allocation amounts, proposed cash balance, total vault assets TA.\n"
          "Output: Boolean execution approval or immediate EVM state revert.\n"
          "Steps:\n"
          "1. Calculate proposed total assets: sumAssets = proposedCash + sum(proposedStrategyAssets).\n"
          "2. Assert conservation of assets: require(sumAssets == TA, 'Invariant: Asset Conservation Failure').\n"
          "3. Assert cash reserve floor: require(proposedCash * 10000 / TA >= 1000, 'Invariant: Cash Below 10% Floor').\n"
          "4. For each strategy i in strategies:\n"
          "5.     Assert maximum strategy ceiling: require(proposedStrategyAssets[i] * 10000 / TA <= 4000, 'Invariant: Strategy Exceeds 40% Cap').\n"
          "6. If any assertion evaluates to false, execute EVM REVERT opcode, rolling back all state modifications with zero loss.\n"
          "7. If all assertions pass, return true.")

    # Algorithm 6
    add_h3(doc, "Algorithm 6: AegisVault ERC-4626 Share Minting & Liquidity Deposit Execution")
    add_p(doc, "Input: Deposit amount assets in USDC, receiver address receiver.\n"
          "Output: Minted vault share tokens shares.\n"
          "Steps:\n"
          "1. Query total assets TA and total supply TS of agUSDC vault shares.\n"
          "2. Calculate shares to mint: shares = (assets * TS) / TA (if TS == 0, shares = assets).\n"
          "3. Transfer assets from user to AegisVault via IERC20.transferFrom.\n"
          "4. Route assets into liquid cash reserve buffer.\n"
          "5. Mint shares of agUSDC to receiver via _mint(receiver, shares).\n"
          "6. Emit Deposit(msg.sender, receiver, assets, shares) event.")

    # Algorithm 7
    add_h3(doc, "Algorithm 7: AegisVault Proportional Share Redemption & Capital Withdrawal")
    add_p(doc, "Input: Burn share amount shares, receiver address receiver, owner address owner.\n"
          "Output: Redeemed underlying assets assets in USDC.\n"
          "Steps:\n"
          "1. Calculate asset redemption amount: assets = (shares * TA) / TS.\n"
          "2. If msg.sender != owner, verify allowance and deduct shares.\n"
          "3. Check available liquid cash reserve C.\n"
          "4. If C < assets, recall deficit (assets - C) proportionally from active lending strategies.\n"
          "5. Burn shares from owner via _burn(owner, shares).\n"
          "6. Transfer assets to receiver via IERC20.transfer.\n"
          "7. Emit Withdraw(msg.sender, receiver, owner, assets, shares) event.")

    # Algorithm 8
    add_h3(doc, "Algorithm 8: Autonomous Keeper Daemon Lifecycle & Periodic Evaluation Loop")
    add_p(doc, "Input: Block polling interval N = 10, Sharpe improvement threshold Delta_S = 0.15.\n"
          "Output: Continuous autonomous vault state synchronization and execution triggers.\n"
          "Steps:\n"
          "1. Sleep until currentBlock >= lastEvaluatedBlock + N.\n"
          "2. Retrieve real-time pool states (utilization, APY, TVL) across Aave, Morpho, Compound, Uniswap.\n"
          "3. Check Sentinel alert flag: If Sentinel triggered, immediately invoke Emergency De-Risk routine.\n"
          "4. Otherwise, construct multivariate lookback tensor X and call Predictor Module (Algorithm 1).\n"
          "5. Ingest predictions and solve MPT optimization for candidate weights w_new (Algorithm 2).\n"
          "6. Calculate candidate Sharpe ratio S_new and current portfolio Sharpe S_current.\n"
          "7. If (S_new - S_current) > Delta_S:\n"
          "8.     Request Auditor Agent to sign EIP-712 intent (Algorithm 4).\n"
          "9.     Submit rebalance transaction to AegisVault.sol on Base Sepolia.\n"
          "10. Update lastEvaluatedBlock = currentBlock and loop to Step 1.")

    add_h3(doc, "3.5 Flowchart Incorporated & Explanation")
    add_p(doc, "Figure 3.3 presents the detailed operational flowchart depicting the decision-making pipeline of AegisVault, tracing the path from Keeper wake-up to on-chain state execution.")
    add_img(doc, "fig2_system_flowchart.png", width=Inches(3.8),
            caption="Figure 3.3: Modern Portfolio Theory Optimization & Anomaly Defense Flowchart.")
    add_p(doc, "The flowchart illustrates the dual-path logic: under standard conditions, market data is evaluated via BiLSTM-GRU and MPT optimization; if candidate Sharpe improvement exceeds 0.15, EIP-712 intents are generated, signed, verified by InvariantGuard, and executed on-chain. If Sentinel detects an anomaly, the normal pipeline is bypassed for instant emergency de-risking.")

    add_h3(doc, "3.6 UML Use Case Diagram")
    add_p(doc, "Figure 3.4 illustrates the UML Use Case Diagram defining the interactions between human actors (Liquidity Providers, System Administrators) and automated actors (Keeper Daemon, Sentinel Daemon, Auditor Agent, Base Sepolia EVM).")
    add_img(doc, "fig3_uml_use_case.png", width=Inches(4.8),
            caption="Figure 3.4: UML Use Case Diagram for Autonomous Multi-Agent Vault System.")

    add_p(doc, "The use cases encompass six primary functional interactions: (1) Deposit USDC & Mint agUSDC shares, (2) Redeem Shares & Withdraw Liquidity, (3) Autonomous Periodic APY Forecasting, (4) Convex Portfolio Rebalancing, (5) Real-Time Flash-Loan Anomaly Detection, and (6) Opcode Invariant Enforcement. Table 3.1 details the actor-use case mapping.")

    # Table 3.1
    uc_data = [
        ("Use Case ID", "Use Case Name", "Primary Actor", "Preconditions", "Postconditions"),
        ("UC-01", "Deposit Capital", "Liquidity Provider", "Connected Web3 wallet with USDC", "agUSDC shares minted; cash reserve updated"),
        ("UC-02", "Withdraw Capital", "Liquidity Provider", "Holding agUSDC shares", "Shares burned; USDC transferred to user"),
        ("UC-03", "Forecast APY Rates", "Keeper / Predictor", "Lookback tensor available", "Forward yield and covariance generated"),
        ("UC-04", "Execute Rebalance", "Optimizer / Auditor", "Sharpe delta > 0.15", "EIP-712 intent signed and executed on-chain"),
        ("UC-05", "Emergency De-Risk", "Sentinel Daemon", "Anomaly z-score > 3.0", "Funds recalled to 100% cash; pool de-risked"),
        ("UC-06", "Enforce Invariants", "Base Sepolia EVM", "Rebalance transaction initiated", "Formal 40% cap & 10% floor asserted")
    ]
    tbl_uc = doc.add_table(rows=len(uc_data), cols=5)
    col_w_uc = [Inches(1.0), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.5)]
    for r_idx, row in enumerate(tbl_uc.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.paragraphs[0].text = uc_data[r_idx][c_idx]
            if r_idx == 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    apply_ref_table_style(tbl_uc, col_widths=col_w_uc)
    add_p(doc, "Table 3.1: Detailed Use Case Specification and Operational Boundaries.",
          font_name="Times New Roman", size_pt=11, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, sp_before=4, sp_after=8)

    add_h3(doc, "3.7 UML Class Diagram")
    add_p(doc, "Figure 3.5 provides the comprehensive UML Class Diagram detailing the object-oriented structure, class attributes, method signatures, and relationships governing both off-chain Python agents and on-chain Solidity contracts.")
    add_img(doc, "fig4_uml_class_diagram.png", width=Inches(4.8),
            caption="Figure 3.5: UML Class Diagram Representing Co-Processor Agents and Smart Contracts.")
    add_p(doc, "The class hierarchy cleanly decouples off-chain data classes (Predictor, PortfolioOptimizer, SentinelGuard, AuditorSigner) from on-chain smart contract interfaces (IERC4626, AegisVault, InvariantGuard, IStrategyAdapter). Relationships denote dependency injection and cryptographic verification interfaces.")

    add_h3(doc, "3.8 UML Sequence Diagrams (Rebalance & Attack Defense)")
    add_p(doc, "To rigorously document system execution timing and inter-agent message exchanges, two comprehensive UML Sequence Diagrams are modeled:")

    add_h3(doc, "3.8.1 Autonomous Rebalancing Workflow Sequence")
    add_p(doc, "Figure 3.6 details the end-to-end execution sequence during a standard automated rebalancing operation initiated by the Keeper Daemon.")
    add_img(doc, "fig5_uml_sequence_diagram.png", width=Inches(4.8),
            caption="Figure 3.6: UML Sequence Diagram: Autonomous Rebalancing Workflow.")
    add_p(doc, "The sequence traces the asynchronous lifecycle: the Keeper triggers market state fetching, the Predictor outputs forward APYs, the Optimizer computes candidate weights w*, the Auditor verifies and EIP-712 signs the intent, and AegisVault calls InvariantGuard to assert constraints before updating strategy balances.")

    add_h3(doc, "3.8.2 Flash-Loan Threat Detection and Defense Sequence")
    add_p(doc, "Figure 3.7 illustrates the high-speed defensive sequence when a flash-loan anomaly is injected into the lending pools.")
    add_img(doc, "fig6_uml_sequence_attack.png", width=Inches(4.8),
            caption="Figure 3.7: UML Sequence Diagram: Flash-Loan Attack Detection and Defense.")
    add_p(doc, "When an exploit causes pool utilization to spike past z > 3.0, Sentinel detects the anomaly in <100ms, halts pending rebalancing queues, packages an emergency recall payload (setting strategy allocation to 0% and cash to 100%), and submits an emergency transaction that executes in 420ms, preventing 100% of capital loss.")

    add_h3(doc, "3.9 UML Component Architecture Diagram")
    add_p(doc, "Figure 3.8 depicts the UML Component Architecture Diagram, detailing the microservice modularity, interface boundaries, and communication protocols connecting the UI, agent co-processor, and decentralized ledger.")
    add_img(doc, "fig7_uml_system_architecture.png", width=Inches(4.8),
            caption="Figure 3.8: UML Component Architecture Diagram.")
    add_p(doc, "The component architecture reinforces clean encapsulation: the React frontend interfaces with the Python backend via REST/WebSockets and with the Base Sepolia blockchain via Viem/JSON-RPC. The Python co-processor agents communicate via internal message buses, and interact with smart contracts through Web3.py.")

    doc.add_page_break()
