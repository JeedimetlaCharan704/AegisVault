import React, { useState } from "react";
import { ArrowDownRight, ArrowUpRight, Loader2 } from "lucide-react";
import confetti from "canvas-confetti";
import { formatCurrency } from "../../lib/utils";

interface DepositWithdrawProps {
  userBalance: number;
  vaultTvl: number;
  onDepositSuccess: (amount: number) => void;
}

export function DepositWithdrawCard({
  userBalance,
  vaultTvl,
  onDepositSuccess,
}: DepositWithdrawProps) {
  const [activeTab, setActiveTab] = useState<"DEPOSIT" | "WITHDRAW">("DEPOSIT");
  const [amount, setAmount] = useState<string>("1000");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const parsedAmount = parseFloat(amount) || 0;
  const exchangeRate = 1.0425;
  const sharesCalculated = parsedAmount > 0 ? (parsedAmount / exchangeRate).toFixed(2) : "0.00";
  const projectedYearlyYield = parsedAmount * 0.1045;

  const handleQuickPercent = (pct: number) => {
    const calc = Math.floor(userBalance * pct);
    setAmount(calc.toString());
  };

  const handleExecute = () => {
    if (parsedAmount <= 0) return;
    setIsSubmitting(true);

    setTimeout(() => {
      setIsSubmitting(false);
      onDepositSuccess(parsedAmount);

      confetti({
        particleCount: 50,
        spread: 50,
        origin: { y: 0.7 },
        colors: ["#3b82f6", "#10b981", "#8b5cf6"],
      });
    }, 600);
  };

  return (
    <div className="zinc-card rounded-xl p-4 border border-zinc-800">
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div className="flex bg-zinc-900 p-0.5 rounded-lg border border-zinc-800 text-xs font-mono w-full">
          <button
            onClick={() => setActiveTab("DEPOSIT")}
            className={`flex-1 py-1 rounded transition-all font-semibold ${
              activeTab === "DEPOSIT" ? "bg-zinc-800 text-white shadow-sm" : "text-zinc-400 hover:text-white"
            }`}
          >
            Deposit USDC
          </button>
          <button
            onClick={() => setActiveTab("WITHDRAW")}
            className={`flex-1 py-1 rounded transition-all font-semibold ${
              activeTab === "WITHDRAW" ? "bg-zinc-800 text-white shadow-sm" : "text-zinc-400 hover:text-white"
            }`}
          >
            Redeem Shares
          </button>
        </div>
      </div>

      <div className="space-y-3 pt-3">
        {/* Input box */}
        <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800 focus-within:border-zinc-700">
          <div className="flex items-center justify-between text-[11px] text-zinc-400 mb-1 font-mono">
            <span>{activeTab === "DEPOSIT" ? "Amount to Deposit" : "Redeem agUSDC"}</span>
            <span>
              Wallet: <strong className="text-zinc-200">{formatCurrency(userBalance)}</strong>
            </span>
          </div>

          <div className="flex items-center justify-between gap-2">
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.0"
              className="bg-transparent text-lg font-bold font-mono text-white outline-none w-full"
            />
            <span className="bg-zinc-900 px-2 py-0.5 rounded border border-zinc-800 font-mono text-xs font-semibold text-zinc-200">
              USDC
            </span>
          </div>

          <div className="flex items-center gap-1.5 mt-2 pt-2 border-t border-zinc-900">
            {[0.25, 0.5, 0.75, 1.0].map((pct) => (
              <button
                key={pct}
                onClick={() => handleQuickPercent(pct)}
                className="flex-1 py-0.5 text-[10px] font-mono rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white transition-colors border border-zinc-800/60"
              >
                {pct === 1.0 ? "MAX" : `${pct * 100}%`}
              </button>
            ))}
          </div>
        </div>

        {/* Accounting Breakdown */}
        <div className="p-2.5 rounded-lg bg-zinc-900/40 border border-zinc-800/80 space-y-1 text-[11px] font-mono">
          <div className="flex items-center justify-between text-zinc-400">
            <span>You Receive</span>
            <span className="font-bold text-white">{sharesCalculated} agUSDC</span>
          </div>
          <div className="flex items-center justify-between text-zinc-400">
            <span>Share Conversion Rate</span>
            <span className="text-zinc-300">1 agUSDC = {exchangeRate} USDC</span>
          </div>
          {parsedAmount > 0 && (
            <div className="flex items-center justify-between text-emerald-400 pt-1 border-t border-zinc-800">
              <span>Projected Yield (10.45% APY)</span>
              <span className="font-bold">+{formatCurrency(projectedYearlyYield)} / yr</span>
            </div>
          )}
        </div>

        {/* Submit */}
        <button
          onClick={handleExecute}
          disabled={isSubmitting || parsedAmount <= 0 || parsedAmount > userBalance}
          className="w-full py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white flex items-center justify-center gap-1.5 transition-all shadow-sm"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              Broadcasting Transaction...
            </>
          ) : (
            <>
              {activeTab === "DEPOSIT" ? "Approve & Deposit USDC" : "Confirm Redeem"}
              <ArrowDownRight className="w-3.5 h-3.5" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
