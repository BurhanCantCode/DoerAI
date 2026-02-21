"use client";

import { FormEvent, useState } from "react";
import { ArrowRight, Loader2 } from "lucide-react";

type WaitlistResponse = {
  status: string;
  beta_access: boolean;
  beta_token?: string | null;
};

export default function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [statusText, setStatusText] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setStatusText("Submitting...");
    try {
      const response = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          email,
          full_name: name || undefined,
          source: "website"
        })
      });
      const body = (await response.json()) as WaitlistResponse & { detail?: string };
      if (!response.ok) {
        setStatusText(body.detail ?? "Unable to submit. Try again.");
        return;
      }

      if (body.beta_access && body.beta_token) {
        setStatusText(`Accepted. Your beta token: ${body.beta_token}`);
      } else {
        setStatusText("Added to waitlist. We’ll email you when your invite is ready.");
      }
      setEmail("");
      setName("");
    } catch {
      setStatusText("Network error. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full max-w-md mx-auto mt-8">
      <form onSubmit={onSubmit} className="flex flex-col gap-3">
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="First name"
            className="flex-1 rounded-2xl border border-white/10 bg-white/5 px-4 py-3.5 text-sm text-white outline-none transition-all focus:border-orange-500/50 focus:bg-white/10 placeholder:text-white/30 backdrop-blur-md"
          />
          <input
            type="email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Email address"
            className="flex-[2] rounded-2xl border border-white/10 bg-white/5 px-4 py-3.5 text-sm text-white outline-none transition-all focus:border-orange-500/50 focus:bg-white/10 placeholder:text-white/30 backdrop-blur-md"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="group relative flex w-full items-center justify-center gap-2 rounded-2xl bg-orange-500 px-6 py-3.5 font-semibold text-black transition-all hover:bg-orange-400 hover:scale-[1.01] active:scale-95 disabled:opacity-70 disabled:hover:scale-100 disabled:cursor-not-allowed shadow-[0_0_20px_-5px_rgba(255,120,0,0.5)]"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <>
              <span>Join the Private Beta</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </>
          )}
        </button>
      </form>
      {statusText && (
        <p className="mt-4 text-center text-sm font-medium text-orange-400 animate-[fadeIn_0.3s_ease-out]">{statusText}</p>
      )}
    </div>
  );
}
