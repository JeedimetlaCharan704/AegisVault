from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from common import  add_p, add_h1, add_h2, add_h3, add_img, apply_ref_table_style

def build_chapter4_docx(doc):
    add_h2(doc, "Chapter – 4: Project Implementation", sp_before=14, sp_after=8)

    add_h3(doc, "4.1 Introduction to Implementation Phase")
    add_p(doc, "The implementation phase of AegisVault represents the concrete engineering execution of the architectural models, mathematical formulations, and algorithmic specifications established in Chapter 3. Implementing a hybrid deep learning and decentralized smart contract system requires strict synchronization between off-chain probabilistic neural sequence processing and on-chain deterministic, gas-constrained state transitions. Every component was developed adhering to production standards of modularity, test-driven development (TDD), and formal security verification.")

    add_h3(doc, "4.2 Development Environment and Tools")
    add_p(doc, "The development ecosystem was configured to support high-performance deep learning computation, rapid smart contract compilation and testing, and modern reactive client interfaces. Table 4.1 delineates the complete development stack and tooling utilized across all layers.")

    # Table 4.1
    env_data = [
        ("Component Layer", "Technology / Framework", "Version", "Functional Role in AegisVault"),
        ("Deep Learning Co-Processor", "Python / PyTorch", "Python 3.10 / PyTorch 2.1", "BiLSTM-GRU neural network training, inference, and tensor computation"),
        ("Convex Optimization", "SciPy Optimize (SLSQP)", "1.11.3", "Sequential Least Squares Programming for convex Sharpe MPT solver"),
        ("API & WebSockets", "FastAPI / Uvicorn", "0.104.1 / 0.24.0", "Asynchronous REST endpoints and high-speed telemetry WebSocket server"),
        ("Blockchain Client Library", "Web3.py / eth-account", "6.11.1 / 0.10.0", "JSON-RPC EVM interaction and EIP-712 cryptographic intent signing"),
        ("Smart Contract Tooling", "Solidity / Hardhat", "0.8.20 / 2.19.1", "ERC-4626 vault implementation, EVM compilation, and local network fork"),
        ("Formal Invariant Testing", "Foundry / Echidna", "0.2.0", "Property-based fuzz testing and formal invariant verification of guardrails"),
        ("Frontend Client App", "React 19 / Vite / Tailwind", "19.0.0 / 5.0.0", "Reactive user dashboard, telemetry graphs, and interactive Web3 controls"),
        ("Web3 Wallet Connectivity", "Wagmi / Viem / Ethers", "2.5.0 / 2.7.0", "MetaMask wallet connection, transaction signing, and BaseScan explorer integration"),
        ("Target Blockchain Ledger", "Base Sepolia Testnet", "Ethereum L2 Rollup", "EVM testnet deployment with sub-cent gas fees and 2-second block times")
    ]
    tbl_env = doc.add_table(rows=len(env_data), cols=4)
    col_w_env = [Inches(1.5), Inches(1.5), Inches(1.3), Inches(2.1)]
    for r_idx, row in enumerate(tbl_env.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.paragraphs[0].text = env_data[r_idx][c_idx]
            if r_idx == 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    apply_ref_table_style(tbl_env, col_widths=col_w_env)
    add_p(doc, "Table 4.1: Comprehensive Development Environment, Frameworks, and Tools.",
          font_name="Times New Roman", size_pt=11, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, sp_before=4, sp_after=8)

    add_h3(doc, "4.3 Implementation Strategy")
    add_p(doc, "The implementation strategy was structured around a decoupled asynchronous microservice pattern. By maintaining an explicit boundary between off-chain heavy numerical processing and on-chain deterministic execution, the system achieves maximum computational efficiency while preserving zero-trust decentralized security. Smart contracts never blindly accept external instructions; instead, every off-chain state suggestion must be accompanied by a valid cryptographic signature and must pass strict EVM opcode-level invariant assertions.")

    add_h3(doc, "4.4 Module-Wise Implementation")
    add_p(doc, "The system codebase is partitioned into five specialized modules, each encapsulated within dedicated source files:")

    add_h3(doc, "4.4.1 Deep Learning Yield & Volatility Predictor Module (predictor.py)")
    add_p(doc, "Purpose: Ingests 7-day rolling multivariate market data and produces forward-looking yield expectations (mu_hat) and covariance matrices (Sigma_hat).\n"
          "Implementation Details: Implemented as a PyTorch nn.Module incorporating nn.LSTM(bidirectional=True, hidden_size=128), nn.GRU(hidden_size=128), and a custom MultiHeadAttention layer with 4 attention heads. Inputs are standardized using rolling mean and variance buffers. Forward inference executes in under 28 milliseconds on standard CPU hardware.")

    add_h3(doc, "4.4.2 Convex Modern Portfolio Theory Optimizer Module (optimizer.py)")
    add_p(doc, "Purpose: Formulates and solves the convex quadratic MPT optimization problem under operational liquidity constraints.\n"
          "Implementation Details: Uses scipy.optimize.minimize with the SLSQP algorithm. Implements exact Jacobian gradients for the objective function. Constraints enforce sum(w) == 1.0, w_i <= 0.40 for all strategies, and w_cash >= 0.10. Execution completes in under 15 milliseconds.")

    add_h3(doc, "4.4.3 Autonomous Sentinel Threat Daemon (sentinel.py)")
    add_p(doc, "Purpose: Provides continuous real-time anomaly detection to protect against flash-loan liquidity drainage attacks.\n"
          "Implementation Details: Operates an asynchronous event loop subscribing to block headers and mempool transactions. Computes running z-scores on borrowing velocity and pool utilization. When z > 3.0, Sentinel flags an emergency condition, generates a 100% cash recall payload, and dispatches an emergency transaction within 420 milliseconds.")

    add_h3(doc, "4.4.4 Cryptographic Auditor Intent Signer (auditor.py)")
    add_p(doc, "Purpose: Validates candidate allocations against business rules and generates cryptographically signed EIP-712 structured data payloads.\n"
          "Implementation Details: Formulates typed structured data conforming to EIP-712 specifications. Evaluates candidate weights against safety rules. If valid, signs the Keccak-256 hash digest using an authorized ECDSA private key via eth_account.messages.encode_typed_data.")

    add_h3(doc, "4.4.5 Autonomous Keeper Scheduler (keeper.py)")
    add_p(doc, "Purpose: Orchestrates the periodic execution lifecycle of the multi-agent co-processor.\n"
          "Implementation Details: Implemented as a background daemon polling the Base Sepolia RPC every N blocks. Coordinates data fetching, model inference, convex optimization, and transaction dispatch.")

    add_h3(doc, "4.4.6 Smart Contract Suite (AegisVault.sol & InvariantGuard.sol)")
    add_p(doc, "Purpose: Manages on-chain capital pooling, share minting/burning, and formal invariant assertion.\n"
          "Implementation Details: AegisVault.sol inherits OpenZeppelin ERC4626Upgradeable.sol. InvariantGuard.sol is deployed as an immutable security guardrail containing formal Solidity require assertions enforcing the 40% strategy ceiling and 10% cash floor at the EVM opcode level.")

    add_h3(doc, "4.5 Frontend Implementation")
    add_p(doc, "The frontend client application was constructed using React 19, Vite, and Tailwind CSS. The interface provides real-time Web3 wallet connectivity via Wagmi and Viem, allowing users to connect their MetaMask wallet, approve USDC token spending, and deposit capital into AegisVault with one click. Real-time portfolio analytics, historical APY yield comparison charts, and live agent reasoning telemetry are rendered using Recharts and WebSockets. Users can simulate flash-loan attacks directly from the UI and observe sub-second autonomous threat mitigation.")

    add_h3(doc, "4.6 Data Storage and Data Handling")
    add_p(doc, "AegisVault implements efficient data handling across off-chain and on-chain domains. Off-chain, historical lending rate sequences and pool utilization metrics are maintained in rolling circular memory buffers and cached in Redis. Model weight tensors are serialized using PyTorch (.pt format). On-chain, the vault minimizes gas overhead by packing strategy allocation structs into 256-bit EVM storage slots, ensuring gas-efficient reads and writes during rebalancing.")

    add_h3(doc, "4.7 Security Measures Implemented")
    add_p(doc, "System security is architected using defense-in-depth principles across multiple layers:")
    add_p(doc, "• Cryptographic EIP-712 Intent Signing: Prevents unauthorized transaction injection. Only allocations co-signed by the authorized Auditor key are accepted by the smart contract.")
    add_p(doc, "• Nonce and Timestamp Invalidation: Every EIP-712 intent includes a monotonically increasing nonce and a short expiration deadline, completely preventing replay attacks.")
    add_p(doc, "• Opcode Invariant Enforcement: InvariantGuard.sol enforces the 40% pool cap and 10% cash floor directly in EVM execution memory, reverting any malicious or erroneous transaction.")
    add_p(doc, "• OpenZeppelin ReentrancyGuard: All external state-changing vault functions are protected by nonReentrant modifiers, preventing recursive call exploits.")

    add_h3(doc, "4.8 Error Handling and Validation")
    add_p(doc, "The architecture incorporates comprehensive error handling and validation routines. Off-chain agents validate tensor shapes, handle RPC connection drops with exponential backoff retries, and fallback to conservative cash allocations if the deep learning model encounters numerical instability. On-chain, custom Solidity errors (e.g., InvariantViolation(), IntentExpired(), InvalidAuditorSignature()) provide gas-efficient failure diagnostics and immediate state rollback upon assertion failure.")

    add_h3(doc, "4.9 Execution and Deployment Workflow")
    add_p(doc, "The complete system is deployed and operational in a live environment: smart contracts are deployed and verified on Base Sepolia testnet, the FastAPI backend agent server is running with active WebSocket telemetry streaming, and the frontend web application is hosted on Vercel with continuous integration and automated GitHub deployments.")

    doc.add_page_break()
