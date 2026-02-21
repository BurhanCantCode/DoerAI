"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useEffect, useState } from "react";
import { Command, Mic, Sparkles, TerminalSquare, ShieldCheck, Zap } from "lucide-react";

export default function MaximalistLandingPage() {
  const [mounted, setMounted] = useState(false);
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);

  // Custom cursor element
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <main className="relative min-h-screen bg-liquid-gradient overflow-hidden">
      <div className="custom-cursor hidden md:block" id="cursor"></div>
      <div className="grain"></div>

      {/* Navbar */}
      <nav className="fixed top-6 left-1/2 -translate-x-1/2 w-[90%] max-w-7xl z-50">
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="glass-holographic rounded-full px-8 py-4 flex justify-between items-center"
        >
          <div className="text-xl md:text-2xl font-display font-bold tracking-widest text-white uppercase flex items-center gap-3">
            <div className="w-3 h-3 md:w-4 md:h-4 rounded-full bg-orange-500 animate-[pulse_2s_infinite]"></div>
            Orange
          </div>
          <div className="hidden md:flex gap-8 text-sm uppercase tracking-[0.2em] font-medium text-white/70">
            <a href="#architecture" className="hover:text-white transition-colors hover-target">Architecture</a>
            <a href="#stats" className="hover:text-white transition-colors hover-target">Performance</a>
          </div>
          <button className="btn-magnetic px-6 py-2 rounded-full bg-orange-500/10 border border-orange-500 text-orange-500 hover:text-white uppercase text-xs md:text-sm font-bold tracking-widest hover-target">
            Deploy
          </button>
        </motion.div>
      </nav>

      {/* Hero Section */}
      <section className="relative h-screen flex flex-col items-center justify-center pt-20 px-4">
        <motion.div
          style={{ y }}
          className="absolute inset-0 z-0 flex items-center justify-center opacity-30 pointer-events-none"
        >
          {/* CSS CSS Shader representation */}
          <div className="w-[800px] h-[800px] bg-orange-500/20 rounded-full blur-[120px] mix-blend-screen mix-blend-color-dodge"></div>
          <div className="absolute w-[600px] h-[600px] bg-purple-500/20 rounded-full blur-[100px] mix-blend-screen translate-x-1/4 -translate-y-1/4"></div>
        </motion.div>

        <div className="relative z-10 text-center w-full flex flex-col items-center max-w-7xl mx-auto">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="inline-flex items-center gap-2 rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-1.5 text-xs font-bold tracking-widest uppercase text-orange-400 backdrop-blur mb-8"
          >
            <Sparkles className="w-3 h-3" />
            <span>Native macOS Agent</span>
          </motion.div>

          <motion.h1
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 1, ease: "easeOut", delay: 0.4 }}
            className="text-[12vw] md:text-[8vw] leading-[0.85] font-display font-black uppercase text-transparent bg-clip-text bg-gradient-to-br from-white via-white to-white/30 tracking-tighter hover-target"
          >
            Speak.
          </motion.h1>
          <motion.h1
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 1, ease: "easeOut", delay: 0.6 }}
            className="text-[12vw] md:text-[8vw] leading-[0.85] font-display font-black uppercase text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-yellow-500 tracking-tighter hover-target -mt-2 md:-mt-6"
          >
            Execute.
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 1 }}
            className="mt-10 text-lg md:text-2xl max-w-2xl text-white/50 font-light leading-relaxed tracking-wide"
          >
            The surgical precision of a natively compiled macOS AI agent. Voice-to-action bypasses the GUI. We build the future.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 1.2 }}
            className="mt-12"
          >
            <button className="hover-target group relative flex items-center justify-center gap-3 rounded-full bg-orange-500 px-8 py-4 font-bold text-black transition-all hover:bg-orange-400 btn-magnetic text-lg tracking-widest uppercase">
              <Mic className="w-5 h-5 flex-shrink-0" />
              <span>Initialize Beta</span>
            </button>
          </motion.div>
        </div>
      </section>

      {/* Architecture Bento Grid */}
      <section id="architecture" className="py-32 px-4 md:px-12 max-w-[1600px] mx-auto relative z-10">
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 0.2 }}
          viewport={{ once: true }}
          className="text-6xl md:text-[10vw] font-display font-black uppercase mb-16 tracking-tighter"
        >
          Architecture
        </motion.h2>

        <div className="grid grid-cols-1 md:grid-cols-3 md:grid-rows-2 gap-6 h-auto md:h-[800px]">

          {/* Large Card */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8 }}
            className="glass-holographic rounded-[2.5rem] p-10 md:col-span-2 relative overflow-hidden group hover-target border border-white/10"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-orange-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
            <div className="relative z-10 h-full flex flex-col justify-between">
              <div>
                <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-8 backdrop-blur-md">
                  <Command className="w-8 h-8 text-orange-400" />
                </div>
                <h3 className="text-4xl md:text-5xl font-display font-bold uppercase mb-4 text-white tracking-tight leading-none group-hover:text-orange-400 transition-colors duration-500">Native Swift<br />Runtime</h3>
              </div>
              <p className="text-xl md:text-2xl text-white/50 max-w-lg leading-relaxed font-light">Zero-latency hooks deep into window management and accessibility APIs. Unmatched execution speed.</p>
            </div>
            <div className="absolute -right-20 -bottom-20 text-[20rem] opacity-[0.03] font-display font-black leading-none pointer-events-none group-hover:opacity-[0.08] transition-opacity duration-700">OS</div>
          </motion.div>

          {/* Tall Card */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="glass-holographic rounded-[2.5rem] p-10 md:row-span-2 relative overflow-hidden group hover-target border border-white/10 flex flex-col justify-end"
          >
            <div className="absolute top-0 right-0 w-full h-full bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4IiBoZWlnaHQ9IjgiPgo8cmVjdCB3aWR0aD0iOCIgaGVpZ2h0PSI4IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMDUiPjwvcmVjdD4KPHBhdGggZD0iTTAgMEw4IDhaTTAgOEw4IDBaIiBzdHJva2U9IiMwMDAiIHN0cm9rZS1vcGFjaXR5PSIwLjEiPjwvcGF0aD4KPC9zdmc+')] opacity-20 group-hover:opacity-40 transition-opacity duration-500"></div>
            <div className="absolute top-10 left-10">
              <TerminalSquare className="w-10 h-10 text-white/30 group-hover:text-white/80 transition-colors" />
            </div>
            <div className="relative z-10">
              <h3 className="text-4xl font-display font-bold uppercase mb-4 tracking-tight leading-none group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-white/50 transition-all">Python<br />Sidecar</h3>
              <p className="text-lg text-white/50 font-light leading-relaxed">Abstract AST generation, multimodal reasoning endpoints, deterministic planning.</p>
            </div>
          </motion.div>

          {/* Small Card 1 */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="glass-holographic rounded-[2.5rem] p-8 md:p-10 relative overflow-hidden group hover-target border border-white/10 flex flex-col justify-between"
          >
            <ShieldCheck className="w-8 h-8 text-orange-500 mb-6" />
            <div>
              <h3 className="text-2xl md:text-3xl font-display font-bold uppercase mb-2 text-white">Contract First</h3>
              <p className="text-base text-white/60 font-light blur-[0.5px] group-hover:blur-none transition-all duration-300">Strictly typed schemas cross boundaries flawlessly. Fail-closed safety mechanisms.</p>
            </div>
          </motion.div>

          {/* Small Card 2 */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="glass-holographic rounded-[2.5rem] p-8 md:p-10 relative overflow-hidden group hover-target border border-white/10 flex flex-col justify-between"
          >
            <div className="absolute inset-0 bg-orange-500/5 group-hover:bg-orange-500/20 transition-colors duration-500"></div>
            <Zap className="w-8 h-8 text-white relative z-10 mb-6" />
            <div className="relative z-10">
              <h3 className="text-2xl md:text-3xl font-display font-bold uppercase mb-2">Cross-App Flow</h3>
              <p className="text-base text-white/60 font-light">Mail &#8594; Slack &#8594; Safari &#8594; Finder. Invisible connective tissue.</p>
            </div>
          </motion.div>

        </div>
      </section>

      {/* Big Numbers Section */}
      <section id="stats" className="py-32 relative z-10 bg-[#020202]/80 backdrop-blur-3xl border-y border-white/5 mt-20">
        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-around items-center gap-16 md:gap-12 text-center">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1 }}
          >
            <div className="text-7xl lg:text-[10rem] font-display font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-white/10 leading-none">0</div>
            <div className="uppercase tracking-[0.3em] text-orange-500 font-bold mt-6 text-sm">Latency (ms)</div>
          </motion.div>
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1, delay: 0.2 }}
          >
            <div className="text-7xl lg:text-[10rem] font-display font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-white/10 leading-none">100</div>
            <div className="uppercase tracking-[0.3em] text-orange-500 font-bold mt-6 text-sm">Task Completion %</div>
          </motion.div>
        </div>
      </section>

      {/* Footer Marquee */}
      <footer className="relative z-10 py-32 overflow-hidden border-t border-white/10 flex flex-col justify-center min-h-[60vh]">
        <div className="w-full flex overflow-hidden whitespace-nowrap mb-20 hover-target py-10 rotate-[-2deg] bg-orange-500/5 backdrop-blur-md border-y border-orange-500/20">
          <div className="animate-marquee inline-block">
            <span className="text-[8vw] md:text-[6vw] font-display font-black uppercase text-stroke px-8">Let's build the future //</span>
            <span className="text-[8vw] md:text-[6vw] font-display font-black uppercase text-stroke px-8">Let's build the future //</span>
          </div>
          <div className="animate-marquee inline-block" aria-hidden="true">
            <span className="text-[8vw] md:text-[6vw] font-display font-black uppercase text-stroke px-8">Let's build the future //</span>
            <span className="text-[8vw] md:text-[6vw] font-display font-black uppercase text-stroke px-8">Let's build the future //</span>
          </div>
        </div>

        <div className="max-w-[1600px] w-full mx-auto px-12 flex flex-col md:flex-row justify-between items-end text-white/30 text-xs md:text-sm font-bold uppercase tracking-[0.2em] mt-auto">
          <div className="mb-4 md:mb-0 hover:text-white transition-colors cursor-default hover-target">&copy; 2026 ORANGE</div>
          <div className="flex gap-8">
            <a href="#" className="hover:text-orange-500 transition-colors hover-target">Privacy</a>
            <a href="#" className="hover:text-orange-500 transition-colors hover-target">Terms</a>
            <a href="#" className="hover:text-orange-500 transition-colors hover-target">Contact us</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
