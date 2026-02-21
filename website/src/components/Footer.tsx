import Link from "next/link";
import { Command } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-white/10 py-12 text-sm text-white/50 relative z-10 mt-10">
      <div className="container flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center">
            <Command className="w-4 h-4 text-white" />
          </div>
          <p>© {new Date().getFullYear()} Orange. Built for macOS.</p>
        </div>
        <nav className="flex gap-6">
          <Link href="/download" className="hover:text-white transition-colors">
            Download
          </Link>
          <Link href="/privacy" className="hover:text-white transition-colors">
            Privacy
          </Link>
          <Link href="/terms" className="hover:text-white transition-colors">
            Terms
          </Link>
        </nav>
      </div>
    </footer>
  );
}
