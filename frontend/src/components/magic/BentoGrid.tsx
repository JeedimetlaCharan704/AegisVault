import React from "react";
import { cn } from "../../lib/utils";

export function BentoGrid({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 max-w-7xl mx-auto",
        className
      )}
    >
      {children}
    </div>
  );
}

export function BentoCard({
  className,
  children,
  colSpan = 1,
}: {
  className?: string;
  children: React.ReactNode;
  colSpan?: 1 | 2 | 3;
}) {
  const colSpanClasses = {
    1: "col-span-1",
    2: "col-span-1 lg:col-span-2",
    3: "col-span-1 md:col-span-2 lg:col-span-3",
  };

  return (
    <div
      className={cn(
        "glass-panel rounded-2xl p-6 transition-all duration-300 relative group overflow-hidden border border-white/5 hover:border-white/10 hover:shadow-2xl hover:shadow-blue-500/5",
        colSpanClasses[colSpan],
        className
      )}
    >
      {children}
    </div>
  );
}
