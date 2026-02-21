"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Mic, Command, ArrowRight, Sparkles } from "lucide-react";
import WaitlistForm from "@/components/WaitlistForm";

export default function Hero() {
  return (
    <section className="container relative pt-32 pb-24 overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-orange-600/10 rounded-full blur-[120px] -z-10"></div>

      <div className="flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 rounded-full border border-orange-500/30 bg-orange-500/10 px-4 py-1.5 text-sm font-medium text-orange-400 backdrop-blur"
        >
          <Sparkles className="w-4 h-4" />
          <span>Private Beta | Native macOS agent</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mt-8 max-w-4xl text-5xl font-bold tracking-tight sm:text-7xl"
        >
          Speak once. <br className="hidden sm:block" />
          <span className="text-gradient">Orange executes</span> <span className="text-gradient-orange">across your Mac.</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-6 max-w-2xl text-lg text-white/60 leading-relaxed"
        >
          Hold a hotkey, say what you want, and Orange plans, confirms, and executes actions in Mail, Slack, browser, Finder, and Calendar automatically.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10 flex flex-col items-center justify-center w-full"
        >
          <WaitlistForm />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mt-20 w-full max-w-4xl"
        >
          <div className="glass-panel rounded-3xl p-2 sm:p-4 overflow-hidden shadow-2xl relative border border-white/10">
            {/* Top Bar for mock terminal / window */}
            <div className="flex items-center gap-2 px-4 py-3 border-b border-white/5 bg-white/5">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
              </div>
              <div className="mx-auto flex items-center gap-2 text-xs font-mono text-white/40">
                <Command className="w-3 h-3" /> native_swift_runtime
              </div>
            </div>
            {/* Mock UX content */}
            <div className="bg-[#0A0A12] p-6 lg:p-10 rounded-b-[20px] font-mono text-sm sm:text-base text-left min-h-[300px] flex flex-col justify-center relative">
              <div className="animate-pulse-slow absolute right-10 top-10 w-32 h-32 bg-orange-500/20 rounded-full blur-[60px]"></div>
              <div className="space-y-4 relative z-10 text-white/80">
                <p className="flex items-center gap-3"><span className="text-orange-400">&gt;</span> <span className="text-white">"Check my unread emails and draft a reply to Sarah about the meeting being moved to 3 PM."</span></p>
                <div className="pl-5 border-l-2 border-white/10 space-y-2 py-2">
                  <p className="text-white/50 opacity-0 animate-[fadeIn_0.5s_0.5s_forwards]">[Agent] Analysing request via /v1/plan...</p>
                  <p className="text-white/50 opacity-0 animate-[fadeIn_0.5s_1s_forwards]">[Agent] Executing step 1: Open Mail app</p>
                  <p className="text-white/50 opacity-0 animate-[fadeIn_0.5s_1.5s_forwards]">[Agent] Executing step 2: Find unread mail from Sarah</p>
                  <p className="text-white/50 opacity-0 animate-[fadeIn_0.5s_2s_forwards]">[Agent] Executing step 3: Draft reply "Sure, see you at 3 PM."</p>
                </div>
                <p className="flex items-center gap-2 text-green-400 opacity-0 animate-[fadeIn_0.5s_2.5s_forwards]"><Sparkles className="w-4 h-4" /> <span>Action chain completed. Waiting for confirmation.</span></p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
