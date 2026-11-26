import React, { useState } from "react";
import { Shield, Check, Copy, Wallet } from "lucide-react";

interface NavbarProps {
  userBalance: number;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  connectedAddress?: string;
  isRealWalletConnected?: boolean;
  onConnectWallet?: () => void;
}

export function Navbar({
  userBalance,
  activeTab,
  setActiveTab,
  connectedAddress = "0x71C95911E9a5D330f4D62145069B562089292e",
  isRealWalletConnected = false,
  onConnectWallet,
}: NavbarProps) {
  const [copied, setCopied] = useState(false);

  const displayAddr = connectedAddress
    ? `${connectedAddress.slice(0, 6)}...${connectedAddress.slice(-4)}`
    : "0x71C9...292e";

  const handleCopyWallet = () => {
    navigator.clipboard.writeText(connectedAddress);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const tabs = [
    { id: "vault", label: "Vault Overview" },
    { id: "regimes", label: "Quant Optimizer" },
    { id: "strategies", label: "Yield Markets" },
    { id: "security", label: "Security & Guardrails" },
    { id: "activity", label: "Audit Trail" },
  ];

  const handleTabClick = (tabId: string) => {
    setActiveTab(tabId);
    const element = document.getElementById(tabId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <header className="border-b border-white/[0.06] bg-[#09090b]/80 backdrop-blur-md sticky top-0 z-30 w-full">
      <div className="max-w-[1440px] mx-auto px-6 sm:px-8 lg:px-10 h-14 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-md bg-white text-black flex items-center justify-center font-bold text-xs shadow-sm">
              <Shield className="w-3.5 h-3.5 text-black fill-current" />
            </div>
            <span className="font-semibold text-sm tracking-tight text-white">
              AegisVault
            </span>
            <span className="text-[10px] font-mono text-zinc-400 bg-zinc-900 px-1.5 py-0.5 rounded border border-white/[0.06] ml-1">
              ERC-4626
            </span>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => handleTabClick(tab.id)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                  activeTab === tab.id
                    ? "text-white bg-white/[0.08]"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Right Info */}
        <div className="flex items-center gap-3 text-xs font-mono">
          {/* Multi-agent Consensus Status */}
          <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-md border border-white/[0.06] bg-zinc-900/60 text-zinc-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-[11px] text-zinc-300">3/3 Agents Online</span>
          </div>

          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-md border border-white/[0.06] bg-zinc-900/60 text-zinc-300">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400" />
            <span className="text-[11px]">Base Sepolia (84532)</span>
          </div>

          {/* Wallet Button */}
          {isRealWalletConnected ? (
            <button
              onClick={handleCopyWallet}
              className="flex items-center gap-2 px-3 py-1 rounded-md border border-emerald-500/30 bg-emerald-950/20 hover:bg-emerald-950/40 text-emerald-300 transition-colors"
              title="Click to copy connected wallet address"
            >
              {copied ? (
                <Check className="w-3 h-3 text-emerald-400" />
              ) : (
                <Copy className="w-3 h-3 text-emerald-500" />
              )}
              <span className="text-[11px] font-mono">{displayAddr}</span>
              <span className="text-zinc-600">·</span>
              <span className="font-medium text-white text-[11px] font-sans">
                ${userBalance.toLocaleString()} USDC
              </span>
            </button>
          ) : (
            <button
              onClick={onConnectWallet}
              className="flex items-center gap-2 px-3 py-1 rounded-md border border-white/[0.1] bg-zinc-800 hover:bg-zinc-700 text-white transition-all shadow-sm font-sans text-xs"
            >
              <Wallet className="w-3.5 h-3.5 text-zinc-400" />
              <span>Connect Wallet</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
