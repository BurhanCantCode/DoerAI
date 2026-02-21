"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

const tiers = [
  { name: "Free", price: "$0", details: "10 commands/day", features: ["Bring Your Own Key", "Basic Support", "Native macOS Runtime"] },
  { name: "Pro", price: "$12", period: "/mo", details: "Unlimited commands", features: ["Managed Cloud Models", "Priority Support", "Advanced Context", "Automated Planning"], popular: true },
  { name: "Team", price: "$20", period: "/seat", details: "Shared settings", features: ["Centralized Billing", "Team Prompts", "Admin Controls", "SLA Support"] }
];

export default function Pricing() {
  return (
    <section className="container py-24 relative z-10">
      <div className="text-center mb-16">
        <h2 className="text-3xl font-bold sm:text-4xl text-white mb-4">Simple, transparent pricing</h2>
        <p className="text-white/50 max-w-xl mx-auto">Choose the plan that fits your execution needs.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-3 max-w-6xl mx-auto">
        {tiers.map((tier, i) => (
          <motion.article
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: i * 0.15 }}
            key={tier.name}
            className={`relative rounded-3xl border p-8 flex flex-col ${tier.popular ? "border-orange-500/50 bg-orange-500/[0.03] shadow-[0_0_40px_-15px_rgba(255,100,0,0.2)]" : "border-white/10 bg-white/[0.02]"}`}
          >
            {tier.popular && (
              <span className="absolute -top-3 inset-x-0 mx-auto w-fit rounded-full bg-orange-500 px-3 py-1 text-xs font-bold uppercase tracking-wider text-black">
                Most Popular
              </span>
            )}
            <h3 className="text-2xl font-semibold text-white mb-2">{tier.name}</h3>
            <p className="text-white/60 mb-6 min-h-[48px]">{tier.details}</p>
            <div className="mb-6 flex items-baseline gap-1">
              <span className="text-5xl font-bold text-white">{tier.price}</span>
              {tier.period && <span className="text-xl text-white/50">{tier.period}</span>}
            </div>

            <ul className="mb-8 flex-1 space-y-4">
              {tier.features.map(feature => (
                <li key={feature} className="flex items-center gap-3">
                  <Check className={`w-5 h-5 ${tier.popular ? "text-orange-400" : "text-white/30"}`} />
                  <span className="text-white/80">{feature}</span>
                </li>
              ))}
            </ul>

            <button className={`w-full rounded-2xl py-3.5 font-semibold text-sm transition-all ${tier.popular ? "bg-orange-500 text-black hover:bg-orange-400 hover:scale-[1.02] shadow-[0_0_20px_-5px_rgba(255,120,0,0.5)]" : "bg-white/10 text-white hover:bg-white/20"}`}>
              {tier.name === 'Team' ? 'Contact Sales' : 'Get Started'}
            </button>
          </motion.article>
        ))}
      </div>
    </section>
  );
}
