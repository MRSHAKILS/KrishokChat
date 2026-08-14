"use client";

/* =========================================================================
   ReadAloudButton — the P5 read-aloud control for completed answers.

   Chain (in order, each step degrading gracefully, never breaking chat):
     1. Backend /api/tts (edge-tts, real Bengali bn-BD neural voice) played
        through a shared Web Audio context. The context is resumed inside the
        click gesture so browser autoplay policies never block playback.
     2. Browser speechSynthesis (fallback when the backend is unreachable —
        the demo machine has no Bengali system voice, so this is degraded
        but non-crashing).
     3. Nothing — the answer text remains visible; an inline error appears.

   Barge-in: stopAllSpeech() cancels every active player (backend + browser)
   and bumps a module-level tick. The chat panel calls it when the farmer
   sends a new query or starts the mic, so stale audio never overlaps the
   next turn. Each button subscribes to the tick to reset its own UI state.
   ========================================================================= */

import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { Volume2, VolumeX } from "lucide-react";
import { cn } from "@/lib/utils";
import { synthesizeSpeech } from "@/lib/api";

interface Player {
  source?: AudioBufferSourceNode;
  synth?: SpeechSynthesisUtterance;
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

/* ---- browser speechSynthesis fallback (pre-existing behavior) --------- */

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
    // Some browsers do not emit voiceschanged until a second synthesis call.
    // A short timeout still lets the system default voice work.
    const timeoutId = window.setTimeout(finish, 450);
  });
}

/* ---- component -------------------------------------------------------- */

export function ReadAloudButton({
  text,
  className,
}: {
  text: string;
  className?: string;
}) {
  const [speaking, setSpeaking] = useState(false);
  const [error, setError] = useState(false);
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
  };

  // Reset this button's UI when any other action barges in (new query, mic).
  const mounted = useRef(false);
  useEffect(() => {
    if (!mounted.current) {
      mounted.current = true;
      return;
    }
    if (stopTickValue > 0) stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stopTickValue]);

  // Stop playback if the message unmounts (chat cleared, new conversation).
  useEffect(() => stop, []);

  const playBackend = async (
    cleanText: string,
    requestId: number,
    ctx: AudioContext | null,
  ): Promise<boolean> => {
    try {
      const blob = await synthesizeSpeech(cleanText, { timeoutMs: 12_000 });
      if (requestRef.current !== requestId) return true; // superseded
      if (!ctx) return false; // no Web Audio → browser fallback

      const arrayBuffer = await blob.arrayBuffer();
      const buffer = await ctx.decodeAudioData(arrayBuffer);
      if (requestRef.current !== requestId) return true; // superseded

      const source = ctx.createBufferSource();
      source.buffer = buffer;
      source.connect(ctx.destination);
      const player: Player = { source };
      playerRef.current = player;
      activePlayers.add(player);
      source.start();
      setSpeaking(true);
      source.onended = () => {
        activePlayers.delete(player);
        if (playerRef.current === player) playerRef.current = null;
        if (requestRef.current === requestId) setSpeaking(false);
      };
      return true;
    } catch {
      return false; // backend unreachable/failed → browser fallback
    }
  };

  const playBrowser = (cleanText: string, requestId: number) => {
    const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
    if (!synth) {
      if (requestRef.current === requestId) {
        setError(true);
        setSpeaking(false);
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
      const selectedVoice = bnVoice ?? voices.find((voice) => voice.default) ?? voices[0];
      const utterance = new SpeechSynthesisUtterance(cleanText.slice(0, 1000));
      // Prefer a Bengali system voice. If the device has none, use its default
      // voice rather than silently failing with language-unavailable.
      utterance.lang = selectedVoice?.lang ?? "bn-BD";
      utterance.rate = 0.88;
      if (selectedVoice) utterance.voice = selectedVoice;

      const player: Player = { synth: utterance };
      playerRef.current = player;
      activePlayers.add(player);
      utterance.onstart = () => {
        if (requestRef.current === requestId) setSpeaking(true);
      };
      utterance.onend = () => {
        activePlayers.delete(player);
        if (playerRef.current === player) playerRef.current = null;
        if (requestRef.current === requestId) setSpeaking(false);
      };
      utterance.onerror = (event) => {
        activePlayers.delete(player);
        if (playerRef.current === player) playerRef.current = null;
        if (
          event.error !== "canceled" &&
          event.error !== "interrupted" &&
          requestRef.current === requestId
        ) {
          setError(true);
        }
        setSpeaking(false);
      };

      // A brief yield after cancel prevents Chrome from dropping the new
      // utterance when a previous answer was just stopped.
      window.setTimeout(() => {
        if (requestRef.current !== requestId) return;
        synth.resume();
        synth.speak(utterance);
      }, 40);
    });
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

    const requestId = ++requestRef.current;
    setError(false);
    setSpeaking(true); // immediate feedback while synthesizing

    // Resume inside the click gesture so autoplay policies never block us.
    const ctx = ensureAudioContext();
    void playBackend(cleanText, requestId, ctx).then((played) => {
      if (!played && requestRef.current === requestId) {
        playBrowser(cleanText, requestId);
      }
    });
  };

  return (
    <>
      <button
        onClick={toggle}
        type="button"
        aria-label={speaking ? "আবৃত্তি বন্ধ করুন" : "পরামর্শটি শুনুন"}
        className={cn(
          "control-press flex min-h-9 items-center gap-1.5 rounded-lg border px-3 text-xs font-medium",
          speaking
            ? "border-leaf bg-leaf text-paper"
            : "border-leaf/25 bg-leaf/8 text-leaf hover:bg-leaf/15",
          className,
        )}
      >
        {speaking ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
        <span>{speaking ? "থামুন" : "শুনুন"}</span>
      </button>
      {error && (
        <p className="text-[11px] text-clay" role="status">
          এই ব্রাউজারে শব্দ চালু করা যায়নি। ব্রাউজারের শব্দ ও স্পিকারের অনুমতি পরীক্ষা করুন।
        </p>
      )}
    </>
  );
}