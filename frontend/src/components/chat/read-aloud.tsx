"use client";

/* =========================================================================
   ReadAloudButton — Synchronized TTS audio player with sentence tracking.

   Features:
     1. Sentence-by-sentence synchronized visual tracking (onSentenceChange).
     2. Voice speed control (০.৭৫x, ১.০x, ১.২৫x) for field accessibility.
     3. Animated mini audio wave equalizer.
     4. Graceful fallback chain: Backend neural voice -> Browser Web Speech API.
     5. Barge-in: stops on new queries or microphone activation.
   ========================================================================= */

import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { Volume2, VolumeX, Gauge, Sparkles, EarOff } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import { cn } from "@/lib/utils";
import { synthesizeSpeech } from "@/lib/api";

interface Player {
  source?: AudioBufferSourceNode;
  synth?: SpeechSynthesisUtterance;
}

/* ---- Sentence splitter helper for Bengali text ---- */
export function splitBengaliSentences(text: string): string[] {
  if (!text) return [];
  // Match sentences ending with ।, ?, !, or newlines
  const matches = text.match(/[^।\n?!]+[।\n?!]*/g);
  if (!matches || matches.length === 0) return [text.trim()];
  return matches.map((s) => s.trim()).filter(Boolean);
}

/* ---- module-level registry + tick (barge-in bus) ---------------------- */

const activePlayers = new Set<Player>();
let stopTick = 0;
const tickListeners = new Set<() => void>();

function stopPlayer(player: Player) {
  if (player.source) {
    try {
      player.source.stop();
    } catch {
      /* already ended */
    }
    player.source.disconnect();
  }
}

/** Cancel every active read-aloud player and notify all buttons to reset. */
export function stopAllSpeech() {
  if (typeof window !== "undefined" && "speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
  for (const player of activePlayers) stopPlayer(player);
  activePlayers.clear();
  stopTick += 1;
  for (const listener of tickListeners) listener();
}

function useStopTick() {
  return useSyncExternalStore(
    (onChange) => {
      tickListeners.add(onChange);
      return () => tickListeners.delete(onChange);
    },
    () => stopTick,
  );
}

/* ---- shared AudioContext (unlocked inside the click gesture) ---------- */

let sharedCtx: AudioContext | null = null;

function ensureAudioContext(): AudioContext | null {
  if (typeof window === "undefined") return null;
  if (!sharedCtx) {
    const Ctor =
      window.AudioContext ??
      (window as unknown as { webkitAudioContext?: typeof AudioContext })
        .webkitAudioContext;
    if (!Ctor) return null;
    sharedCtx = new Ctor();
  }
  void sharedCtx.resume();
  return sharedCtx;
}

/* ---- browser speechSynthesis fallback -------------------------------- */

function getVoicesWhenReady(synth: SpeechSynthesis): Promise<SpeechSynthesisVoice[]> {
  const voices = synth.getVoices();
  if (voices.length > 0) return Promise.resolve(voices);

  return new Promise((resolve) => {
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timeoutId);
      synth.removeEventListener("voiceschanged", finish);
      resolve(synth.getVoices());
    };
    synth.addEventListener("voiceschanged", finish);
    const timeoutId = window.setTimeout(finish, 450);
  });
}

/* ---- Component -------------------------------------------------------- */

export function ReadAloudButton({
  text,
  className,
  onSentenceChange,
}: {
  text: string;
  className?: string;
  onSentenceChange?: (index: number | null) => void;
}) {
  const [speaking, setSpeaking] = useState(false);
  // null = no error; "voice" = no Bengali voice found; "offline" = backend unreachable while offline
  const [error, setError] = useState<null | "voice" | "offline">(null);
  const [speed, setSpeed] = useState<0.75 | 1.0 | 1.25>(1.0);
  const requestRef = useRef(0);
  const playerRef = useRef<Player | null>(null);
  const stopTickValue = useStopTick();

  const stop = () => {
    requestRef.current += 1;
    if (playerRef.current) {
      activePlayers.delete(playerRef.current);
      stopPlayer(playerRef.current);
      playerRef.current = null;
    }
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setSpeaking(false);
    onSentenceChange?.(null);
  };

  // Reset when any other action barges in
  const mounted = useRef(false);
  useEffect(() => {
    if (!mounted.current) {
      mounted.current = true;
      return;
    }
    if (stopTickValue > 0) stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stopTickValue]);

  // Stop playback on unmount
  useEffect(() => stop, []);

  const cycleSpeed = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSpeed((prev) => (prev === 1.0 ? 1.25 : prev === 1.25 ? 0.75 : 1.0));
  };

  const playBrowserSequential = (sentences: string[], requestId: number) => {
    const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
    if (!synth || sentences.length === 0) {
      if (requestRef.current === requestId) {
        setError(typeof navigator !== "undefined" && !navigator.onLine ? "offline" : "voice");
        setSpeaking(false);
        onSentenceChange?.(null);
      }
      return;
    }

    synth.cancel();
    void getVoicesWhenReady(synth).then((voices) => {
      if (requestRef.current !== requestId) return;

      const bnVoice = voices.find(
        (voice) =>
          voice.lang.toLowerCase().startsWith("bn") ||
          voice.name.toLowerCase().includes("bengali"),
      );

      if (!bnVoice) {
        setError(typeof navigator !== "undefined" && !navigator.onLine ? "offline" : "voice");
        setSpeaking(false);
        onSentenceChange?.(null);
        return;
      }

      let currentIndex = 0;

      const speakNextSentence = () => {
        if (requestRef.current !== requestId || currentIndex >= sentences.length) {
          if (requestRef.current === requestId) {
            setSpeaking(false);
            onSentenceChange?.(null);
          }
          return;
        }

        const sentenceText = sentences[currentIndex]
          .replace(/\[[^\]]+\]/g, "")
          .replace(/\s+/g, " ")
          .trim();

        if (!sentenceText) {
          currentIndex++;
          speakNextSentence();
          return;
        }

        const utterance = new SpeechSynthesisUtterance(sentenceText);
        utterance.lang = bnVoice.lang;
        utterance.voice = bnVoice;
        utterance.rate = speed * 0.9;

        const player: Player = { synth: utterance };
        playerRef.current = player;
        activePlayers.add(player);

        utterance.onstart = () => {
          if (requestRef.current === requestId) {
            setSpeaking(true);
            onSentenceChange?.(currentIndex);
          }
        };

        utterance.onend = () => {
          activePlayers.delete(player);
          if (playerRef.current === player) playerRef.current = null;
          if (requestRef.current === requestId) {
            currentIndex++;
            speakNextSentence();
          }
        };

        utterance.onerror = (event) => {
          activePlayers.delete(player);
          if (playerRef.current === player) playerRef.current = null;
          if (
            event.error !== "canceled" &&
            event.error !== "interrupted" &&
            requestRef.current === requestId
          ) {
            setError(typeof navigator !== "undefined" && !navigator.onLine ? "offline" : "voice");
          }
          setSpeaking(false);
          onSentenceChange?.(null);
        };

        synth.speak(utterance);
      };

      // Brief delay after cancel
      window.setTimeout(() => {
        if (requestRef.current !== requestId) return;
        synth.resume();
        speakNextSentence();
      }, 40);
    });
  };

  const playBackend = async (
    cleanText: string,
    requestId: number,
    ctx: AudioContext | null,
    sentences: string[],
  ): Promise<boolean> => {
    try {
      const blob = await synthesizeSpeech(cleanText, { timeoutMs: 12_000 });
      if (requestRef.current !== requestId) return true;
      if (!ctx) return false;

      const arrayBuffer = await blob.arrayBuffer();
      const buffer = await ctx.decodeAudioData(arrayBuffer);
      if (requestRef.current !== requestId) return true;

      const source = ctx.createBufferSource();
      source.buffer = buffer;
      source.playbackRate.value = speed;
      source.connect(ctx.destination);
      const player: Player = { source };
      playerRef.current = player;
      activePlayers.add(player);
      source.start();
      setSpeaking(true);

      // Interpolate sentence highlights across total audio duration
      const totalDuration = buffer.duration / speed;
      const sentenceDurations = sentences.map((s) => Math.max(s.length, 1));
      const totalChars = sentenceDurations.reduce((a, b) => a + b, 0);

      let accumulatedTime = 0;
      sentences.forEach((_, idx) => {
        const sentenceFraction = sentenceDurations[idx] / totalChars;
        const sentenceDurationMs = sentenceFraction * totalDuration * 1000;
        const startTimeMs = (accumulatedTime / totalChars) * totalDuration * 1000;
        accumulatedTime += sentenceDurations[idx];

        window.setTimeout(() => {
          if (requestRef.current === requestId && playerRef.current === player) {
            onSentenceChange?.(idx);
          }
        }, startTimeMs);
      });

      source.onended = () => {
        activePlayers.delete(player);
        if (playerRef.current === player) playerRef.current = null;
        if (requestRef.current === requestId) {
          setSpeaking(false);
          onSentenceChange?.(null);
        }
      };
      return true;
    } catch {
      return false;
    }
  };

  const toggle = () => {
    if (speaking) {
      stop();
      return;
    }

    const cleanText = text
      .replace(/\[[^\]]+\]/g, "")
      .replace(/\s+/g, " ")
      .trim();
    if (!cleanText) return;

    const sentences = splitBengaliSentences(text);
    const requestId = ++requestRef.current;
    setError(null);
    setSpeaking(true);

    const ctx = ensureAudioContext();
    void playBackend(cleanText, requestId, ctx, sentences).then((played) => {
      if (!played && requestRef.current === requestId) {
        playBrowserSequential(sentences, requestId);
      }
    });
  };

  const speedLabelBn = speed === 0.75 ? "০.৭৫x" : speed === 1.25 ? "১.২৫x" : "১.০x";

  return (
    <div className="flex items-center gap-1.5">
      <button
        onClick={toggle}
        type="button"
        aria-label={speaking ? "আবৃত্তি বন্ধ করুন" : "পরামর্শটি শুনুন"}
        className={cn(
          "control-press flex min-h-9 items-center gap-1.5 rounded-lg border px-3 text-xs font-semibold transition-all cursor-pointer",
          speaking
            ? "border-leaf bg-leaf text-paper shadow-xs"
            : "border-leaf/25 bg-leaf/8 text-leaf hover:bg-leaf/15",
          className,
        )}
      >
        {speaking ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
        <span>{speaking ? "থামুন" : "শুনুন"}</span>
        {speaking && (
          <span className="flex items-center gap-0.5 ml-0.5">
            <EqualizerBar height={10} delay={0} />
            <EqualizerBar height={14} delay={0.2} />
            <EqualizerBar height={8} delay={0.4} />
          </span>
        )}
      </button>

      {/* Voice Speed Toggle Chip */}
      <button
        onClick={cycleSpeed}
        type="button"
        title="পড়ার গতি পরিবর্তন করুন (০.৭৫x / ১.০x / ১.২৫x)"
        className="flex min-h-9 items-center gap-1 rounded-lg border border-bone bg-paper px-2 py-1 text-xs font-mono font-medium text-ink-soft hover:border-leaf/40 hover:text-leaf transition-colors cursor-pointer"
      >
        <span>{speedLabelBn}</span>
      </button>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          role="status"
          className="flex min-h-10 items-center gap-2 rounded-lg border border-clay/30 bg-clay/10 px-3 py-2 text-xs font-medium leading-relaxed text-ink-soft"
        >
          <EarOff className="h-4 w-4 shrink-0 text-clay" aria-hidden />
          <span>
            {error === "offline"
              ? "ইন্টারনেট সংযোগ ছাড়া এখন কণ্ঠস্বর দেওয়া যাচ্ছে না — লেখাটি পড়ে নিন।"
              : "এই ফোনে বাংলা কণ্ঠস্বর পাওয়া যায়নি — লেখাটি পড়ে নিন।"}
          </span>
        </motion.div>
      )}
    </div>
  );
}

function EqualizerBar({ height, delay }: { height: number; delay: number }) {
  return (
    <motion.span
      animate={{ height: [4, height, 4] }}
      transition={{ duration: 0.6, repeat: Infinity, delay, ease: "easeInOut" }}
      className="w-0.5 rounded-full bg-paper block"
    />
  );
}