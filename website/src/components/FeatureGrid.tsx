"use client";

import { Mic, ShieldCheck, MonitorSmartphone, BrainCircuit } from "lucide-react";
import { motion } from "framer-motion";

const features = [
  {
    title: "Voice -> Action",
    body: "Fast hold-to-talk workflow with real-time transcript and interactive action timeline.",
    icon: <Mic className="w-6 h-6 text-orange-400" />
  },
  {
    title: "Safety Guard",
    body: "Every critical action requires confirmation before sending, deleting, or purchasing.",
    icon: <ShieldCheck className="w-6 h-6 text-green-400" />
  },
  {
    title: "Cross-App Execution",
    body: "Deep integrations with Mail, Slack, browser, Finder, and Calendar for focused quality.",
    icon: <MonitorSmartphone className="w-6 h-6 text-blue-400" />
  },
  {
    title: "Local-First Privacy",
    body: "On-device defaults keep your data safe, with optional managed cloud reasoning endpoints.",
    icon: <BrainCircuit className="w-6 h-6 text-purple-400" />
  }
];

export default function FeatureGrid() {
  return (
    <section className="container py-24 relative">
      <div className="text-center mb-16">
        <h2 className="text-3xl font-bold sm:text-4xl text-white mb-4">Powerful, by design.</h2>
        <p className="text-white/50 max-w-2xl mx-auto">Built from the ground up for macOS using native Swift and Python planning sidecar, delivering an incredibly fast and fluid experience.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {features.map((feature, i) => (
          <motion.article
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
            key={feature.title}
            className="group relative rounded-3xl border border-white/5 bg-white/[0.02] p-8 hover:bg-white/[0.04] transition-colors overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative z-10">
              <div className="mb-5 inline-flex items-center justify-center rounded-2xl bg-white/10 p-4 border border-white/10 shadow-inner">
                {feature.icon}
              </div>
              <h3 className="mb-3 text-2xl font-semibold text-white tracking-tight">{feature.title}</h3>
              <p className="text-white/60 leading-relaxed text-lg">{feature.body}</p>
            </div>
            <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-white/5 rounded-full blur-[40px] group-hover:bg-white/10 transition-colors"></div>
          </motion.article>
        ))}
      </div>
    </section>
  );
}
