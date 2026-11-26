/**
 * Web3 Browser Wallet Connector (EIP-1193 Standard)
 * Supports MetaMask, Coinbase Wallet, Rabby, and other EVM injected providers.
 * Target Network: Base Sepolia (Chain ID: 84532 / 0x14a34)
 */

declare global {
  interface Window {
    ethereum?: any;
  }
}

export const BASE_SEPOLIA_CHAIN_ID = 84532;
export const BASE_SEPOLIA_HEX = "0x14a34";

export interface WalletState {
  isConnected: boolean;
  address: string | null;
  chainId: number | null;
  balanceUsdc: number;
}

export async function connectBrowserWallet(): Promise<{ address: string; chainId: number } | null> {
  if (typeof window === "undefined" || !window.ethereum) {
    alert("No EVM wallet detected. Please install MetaMask, Coinbase Wallet, or Rabby.");
    return null;
  }

  try {
    const accounts = await window.ethereum.request({
      method: "eth_requestAccounts",
    });

    const chainIdHex = await window.ethereum.request({
      method: "eth_chainId",
    });

    const chainId = parseInt(chainIdHex, 16);

    // Prompt network switch if not on Base Sepolia
    if (chainId !== BASE_SEPOLIA_CHAIN_ID) {
      try {
        await window.ethereum.request({
          method: "wallet_switchEthereumChain",
          params: [{ chainId: BASE_SEPOLIA_HEX }],
        });
      } catch (switchError: any) {
        // Chain not added yet -> Add Base Sepolia
        if (switchError.code === 4902) {
          await window.ethereum.request({
            method: "wallet_addEthereumChain",
            params: [
              {
                chainId: BASE_SEPOLIA_HEX,
                chainName: "Base Sepolia Testnet",
                nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
                rpcUrls: ["https://sepolia.base.org"],
                blockExplorerUrls: ["https://sepolia.basescan.org"],
              },
            ],
          });
        }
      }
    }

    return {
      address: accounts[0],
      chainId,
    };
  } catch (error) {
    console.error("Wallet connection rejected or failed:", error);
    return null;
  }
}
