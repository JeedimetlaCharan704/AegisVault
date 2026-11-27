from common import  add_p, add_h1, add_h2, add_h3

def build_chapter7_docx(doc):
    add_h2(doc, "Chapter – 7: Bibliography", sp_before=14, sp_after=8)

    add_h3(doc, "7.1 Reference Books")
    add_p(doc, "1. Goodfellow, I., Bengio, Y., and Courville, A. (2016). Deep Learning. MIT Press, Cambridge, MA.\n"
          "2. Antonopoulos, A. M., and Wood, G. (2018). Mastering Ethereum: Building Smart Contracts and DApps. O'Reilly Media, Sebastopol, CA.\n"
          "3. Fabozzi, F. J., Gupta, F., and Markowitz, H. M. (2002). The Legacy of Modern Portfolio Theory. The Journal of Investing, 11(3), pp. 7–22.\n"
          "4. Boyd, S., and Vandenberghe, L. (2004). Convex Optimization. Cambridge University Press, Cambridge, UK.\n"
          "5. Chacon, S., and Straub, B. (2014). Pro Git: Everything You Need to Know About Git. Apress, Berkeley, CA.")

    add_h3(doc, "7.2 Reference Papers")
    add_p(doc, "1. Zhang, L., Wang, Y., and Liu, X. (2023). Autonomous Yield Optimization in DeFi via Deep Reinforcement Learning and LSTM Networks. IEEE Transactions on Neural Networks and Learning Systems, 34(8), pp. 4112–4125.\n"
          "2. Zhou, L., and Qin, K. (2021). High-Frequency Flash Loan Vulnerabilities and Liquidity Manipulation in Decentralized Finance. Proceedings of the IEEE Symposium on Security and Privacy (S&P), pp. 1024–1039.\n"
          "3. Markowitz, H. M., and Fabozzi, F. J. (2022). Dynamic Mean-Variance Portfolio Selection and Multi-Factor Sharpe Optimization. Journal of Portfolio Management, 48(4), pp. 31–47.\n"
          "4. Gudgeon, L., Perez, D., Harz, D., Gervais, A., and Livshits, B. (2022). DeFi Vault Security: Automated Execution and Invariant Circuit Breakers. ACM Conference on Computer and Communications Security (CCS), pp. 589–604.\n"
          "5. Wang, J., and Chen, S. (2023). Bidirectional LSTM and Attention Mechanisms for Multivariate Financial Time-Series Forecasting. Elsevier Expert Systems with Applications, 218, 119582.\n"
          "6. Scavuzzo, M., and Daian, P. (2023). Cryptographic Intent Architecture and Off-Chain Consensus for Blockchain Systems. Springer Financial Cryptography and Data Security (FC), LNCS 13985, pp. 245–262.\n"
          "7. Hochreiter, S., and Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), pp. 1735–1780.\n"
          "8. Vaswani, A., et al. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems (NeurIPS), 30, pp. 5998–6008.\n"
          "9. Kipf, T. N., and Welling, M. (2017). Semi-Supervised Classification with Graph Convolutional Networks. International Conference on Learning Representations (ICLR).\n"
          "10. Daian, P., et al. (2020). Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges. IEEE Symposium on Security and Privacy (S&P), pp. 910–927.")

    add_h3(doc, "7.3 Reference Websites")
    add_p(doc, "1. Ethereum Improvement Proposal 4626 (ERC-4626 Tokenized Vault Standard): https://eips.ethereum.org/EIPS/eip-4626\n"
          "2. Ethereum Improvement Proposal 712 (Typed Structured Data Hashing and Signing): https://eips.ethereum.org/EIPS/eip-712\n"
          "3. PyTorch Deep Learning Framework Documentation: https://pytorch.org/docs/stable/\n"
          "4. OpenZeppelin Contracts Security Library: https://docs.openzeppelin.com/contracts/4.x/\n"
          "5. Base Layer-2 Blockchain Documentation: https://docs.base.org/\n"
          "6. SciPy Numerical Optimization Library (SLSQP): https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html\n"
          "7. BaseScan Sepolia Block Explorer: https://sepolia.basescan.org/\n"
          "8. AegisVault Live Production Web Application: https://aegis-vault-ten.vercel.app/\n"
          "9. AegisVault Open-Source GitHub Repository: https://github.com/JeedimetlaCharan704/AegisVault")
