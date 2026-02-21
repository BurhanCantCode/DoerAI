"use client";

import { motion } from "framer-motion";
import { CheckCircle2 } from "lucide-react";

const rows = [
  { app: "Mail / Gmail", workflows: "Draft, reply, send (with confirmation)", beta: "High" },
  { app: "Slack", workflows: "Reply in active thread, channel-safe prompts", beta: "High" },
  { app: "Safari / Chrome", workflows: "Open URL, search, fill simple inputs", beta: "High" },
  { app: "Finder", workflows: "Create folder, rename, navigation", beta: "Medium" },
  { app: "Calendar", workflows: "Create event from natural language", beta: "Medium" }
];

export default function SupportedApps() {
  return (
    <section className="container py-24 relative">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="relative mx-auto max-w-5xl rounded-3xl border border-white/10 bg-white/[0.03] backdrop-blur-xl p-8 md:p-12 overflow-hidden shadow-2xl"
      >
        <div className="absolute top-0 right-0 w-64 h-64 bg-orange-500/10 rounded-full blur-[80px]"></div>
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle2 className="w-6 h-6 text-green-400" />
            <h2 className="text-3xl font-bold text-white">Private Beta Supported Apps</h2>
          </div>
          <p className="mt-2 text-lg text-white/60 max-w-2xl mb-10">
            v1 beta is intentionally narrow. We prioritize reliability in this core set before long-tail app support.
          </p>
          <div className="overflow-x-auto rounded-2xl border border-white/10 bg-black/20 backdrop-blur-md">
            <table className="w-full min-w-[620px] border-collapse text-left text-sm md:text-base text-white">
              <thead className="bg-white/5 uppercase tracking-wider text-white/50 text-xs">
                <tr>
                  <th className="py-4 px-6 font-semibold">App</th>
                  <th className="py-4 px-6 font-semibold">Beta Workflows</th>
                  <th className="py-4 px-6 font-semibold text-center">Readiness</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {rows.map((row) => (
                  <tr key={row.app} className="hover:bg-white/5 transition-colors">
                    <td className="py-4 px-6 font-medium text-white">{row.app}</td>
                    <td className="py-4 px-6 text-white/70">{row.workflows}</td>
                    <td className="py-4 px-6 text-center">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${row.beta === 'High' ? 'bg-green-400/10 text-green-400 border-green-400/20' : 'bg-yellow-400/10 text-yellow-400 border-yellow-400/20'}`}>
                        {row.beta}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
