import React, { useState } from "react";
import { Loader2, Calculator, Check, Zap, TrendingUp, Clock } from "lucide-react";
import { formatCurrency } from "../../lib/utils";
import { SpotlightCard } from "../magic/SpotlightCard";

interface DepositPanelProps {
  userBalance: number;
  netApy?: number;
  onDepositSuccess: (amount: number) => void;
}

export function DepositPanel({ userBalance, netApy = 10.45, onDepositSuccess }: DepositPanelProps) {
  const [tab, setTab] = useState<"DEPOSIT" | "WITHDRAW">("DEPOSIT");
  const [amount, setAmount] = useState<string>("1000");
  const [compoundFreq, setCompoundFreq] = useState<"HOURLY" | "DAILY" | "CONTINUOUS">("HOURLY");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [showCalculator, setShowCalculator] = useState<boolean>(true);

  const parsed = parseFloat(amount) || 0;
  const exchangeRate = 1.0425;
  const shares = parsed > 0 ? (parsed / exchangeRate).toFixed(2) : "0.00";
  const apyRate = (netApy || 10.45) / 100;

  // Compound return calculations
  const dailyReturn = parsed * (apyRate / 365);
  const weeklyReturn = dailyReturn * 7;
  const monthlyReturn = parsed * (apyRate / 12);
  const yearlyReturn = parsed * apyRate;
  
  // 3-year compound interest: A = P(1 + r/n)^(nt)
  const n = compoundFreq === "HOURLY" ? 8760 : compoundFreq === "DAILY" ? 365 : 10000;
  const threeYearCompound = parsed * (Math.pow(1 + apyRate / n, n * 3) - 1);

  const handleMax = () => {
    setAmount(userBalance.toString());
  };

  const handleAction = () => {
    if (parsed <= 0 || parsed > userBalance) return;
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      onDepositSuccess(parsed);
    }, 600);
  };

  return (
    <SpotlightCard className="p-6 sm:p-7 w-full flex flex-col justify-between border border-white/[0.08]" spotlightColor="rgba(255, 255, 255, 0.08)">
      <div>
        {/* Toggle Bar */}
        <div className="flex bg-zinc-900 p-1 rounded-xl border border-white/[0.08] text-xs font-medium w-full mb-5">
          <button
            onClick={() => setTab("DEPOSIT")}
            className={`flex-1 py-2 rounded-lg transition-all ${
              tab === "DEPOSIT" ? "bg-zinc-800 text-white font-semibold shadow-sm" : "text-zinc-400 hover:text-white"
            }`}
          >
            Deposit USDC
          </button>
          <button
            onClick={() => setTab("WITHDRAW")}
            className={`flex-1 py-2 rounded-lg transition-all ${
              tab === "WITHDRAW" ? "bg-zinc-800 text-white font-semibold shadow-sm" : "text-zinc-400 hover:text-white"
            }`}
          >
            Withdraw Shares
          </button>
        </div>

        {/* Input Block */}
        <div className="p-4 rounded-xl bg-zinc-900/70 border border-white/[0.08] focus-within:border-blue-500/50 transition-all">
          <div className="flex items-center justify-between text-xs text-zinc-400 mb-2 font-mono">
            <span>{tab === "DEPOSIT" ? "Deposit Amount" : "Shares to Redeem"}</span>
            <button
              onClick={handleMax}
              className="hover:text-white transition-colors"
            >
              Balance: <span className="text-zinc-200 font-bold">{formatCurrency(userBalance)}</span> (Max)
            </button>
          </div>

          <div className="flex items-center justify-between gap-3 my-1">
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="0.00"
              className="bg-transparent text-2xl font-bold font-mono text-white outline-none w-full"
            />
            <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-zinc-800 border border-white/[0.08] text-zinc-200 font-mono">
              USDC
            </span>
          </div>

          {/* Quick preset pills */}
          <div className="flex items-center gap-1.5 mt-3 pt-3 border-t border-white/[0.06]">
            {[500, 1000, 5000].map((val) => (
              <button
                key={val}
                onClick={() => setAmount(val.toString())}
                className="flex-1 py-1 text-[11px] font-mono rounded-md bg-zinc-800/80 hover:bg-zinc-700/80 text-zinc-300 hover:text-white transition-colors"
              >
                +${val.toLocaleString()}
              </button>
            ))}
            <button
              onClick={handleMax}
              className="flex-1 py-1 text-[11px] font-mono font-bold rounded-md bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 hover:text-blue-200 transition-colors border border-blue-500/20"
            >
              MAX
            </button>
          </div>
        </div>

        {/* Share Conversion & Fee Summary */}
        <div className="mt-3.5 p-3.5 rounded-xl bg-zinc-900/40 border border-white/[0.06] space-y-1.5 text-xs font-mono">
          <div className="flex items-center justify-between text-zinc-400">
            <span>You Receive</span>
            <span className="text-white font-bold">{shares} agUSDC</span>
          </div>
          <div className="flex items-center justify-between text-zinc-400">
            <span>Share Conversion Rate</span>
            <span className="text-zinc-300">1 agUSDC = {exchangeRate} USDC</span>
          </div>
          <div className="flex items-center justify-between text-zinc-400">
            <span>Network Gas Fee</span>
            <span className="text-emerald-400 font-medium">{"<"} $0.005 (Base Sepolia)</span>
          </div>
        </div>

        {/* Live Compound Earnings Calculator (Productivity Power Tool) */}
        {tab === "DEPOSIT" && (
          <div className="mt-4 p-4 rounded-xl bg-zinc-900/60 border border-white/[0.08]">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-xs font-semibold text-white font-mono uppercase tracking-wider">
                  Compound Returns
                </span>
              </div>

              {/* Compounding frequency picker */}
              <div className="flex bg-zinc-800/80 p-0.5 rounded-md text-[10px] font-mono">
                {(["HOURLY", "DAILY", "CONTINUOUS"] as const).map((freq) => (
                  <button
                    key={freq}
                    onClick={() => setCompoundFreq(freq)}
                    className={`px-2 py-0.5 rounded transition-all ${
                      compoundFreq === freq
                        ? "bg-zinc-700 text-white font-bold"
                        : "text-zinc-400 hover:text-zinc-200"
                    }`}
                  >
                    {freq === "HOURLY" ? "1h" : freq === "DAILY" ? "1d" : "Euler"}
                  </button>
                ))}
              </div>
            </div>

            {/* Projection Grid */}
            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div className="p-2.5 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                <span className="text-[10px] text-zinc-400 block mb-0.5">1 Day</span>
                <span className="text-emerald-400 font-bold block">
                  +{formatCurrency(dailyReturn)}
                </span>
                <span className="text-[9px] text-zinc-400 font-sans">Linear yield</span>
              </div>

              <div className="p-2.5 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                <span className="text-[10px] text-zinc-400 block mb-0.5">1 Month (30d)</span>
                <span className="text-emerald-400 font-bold block">
                  +{formatCurrency(monthlyReturn)}
                </span>
                <span className="text-[9px] text-zinc-400 font-sans">Compounded</span>
              </div>

              <div className="p-2.5 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                <span className="text-[10px] text-zinc-400 block mb-0.5">1 Year</span>
                <span className="text-emerald-400 font-bold block">
                  +{formatCurrency(yearlyReturn)}
                </span>
                <span className="text-[9px] text-zinc-400 font-sans">{(apyRate * 100).toFixed(2)}% APY</span>
              </div>

              <div className="p-2.5 rounded-lg bg-zinc-900/70 border border-white/[0.04]">
                <span className="text-[10px] text-zinc-400 block mb-0.5">3 Years</span>
                <span className="text-emerald-400 font-bold block">
                  +{formatCurrency(threeYearCompound)}
                </span>
                <span className="text-[9px] text-zinc-400 font-sans">Re-invested</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Action Button */}
      <div className="mt-5">
        <button
          onClick={handleAction}
          disabled={isLoading || parsed <= 0 || parsed > userBalance}
          className="group relative w-full py-3.5 rounded-xl text-xs font-bold bg-white hover:bg-zinc-200 text-black disabled:opacity-40 disabled:cursor-not-allowed transition-all font-sans flex items-center justify-center gap-2 shadow-lg tracking-wide uppercase font-mono overflow-hidden"
        >
          <span className="relative z-10 flex items-center gap-2">
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Processing Transaction...
              </>
            ) : tab === "DEPOSIT" ? (
              "Approve & Deposit USDC"
            ) : (
              "Withdraw Funds"
            )}
          </span>
          {/* Subtle Shimmer Hover Effect */}
          <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/40 to-transparent pointer-events-none" />
        </button>
      </div>
    </SpotlightCard>
  );
}
