"use client";

import { useEffect, useRef, useState } from "react";
import { useChat } from "@/context/ChatContext";
import { MessageBubble } from "./MessageBubble";

interface ChatWindowProps {
  currentUsername: string;
}

const STATUS_LABEL: Record<string, string> = {
  idle: "",
  connecting: "Connecting…",
  reconnecting: "Reconnecting…",
  disconnected: "Disconnected",
  connected: "",
};

export function ChatWindow({ currentUsername }: ChatWindowProps) {
  const { messages, status, sendMessage } = useChat();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    const text = input.trim();
    if (!text || status !== "connected") return;
    sendMessage(text);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <aside className="w-72 flex-none flex flex-col border-l border-stone-200 bg-white">
      {/* Header */}
      <div className="flex-none p-3 border-b border-stone-200">
        <h2 className="text-sm font-semibold text-stone-700 tracking-wide uppercase">
          Chat
        </h2>
        {STATUS_LABEL[status] && (
          <span className="text-xs text-stone-400 animate-pulse">
            {STATUS_LABEL[status]}
          </span>
        )}
        {status === "connected" && (
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-3 py-2 flex flex-col gap-0.5">
        {messages.length === 0 && status === "connected" && (
          <p className="text-xs text-stone-400 text-center mt-8">
            No messages yet. Say hello!
          </p>
        )}
        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            username={msg.username}
            message={msg.message}
            isOwn={msg.username === currentUsername}
          />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="flex-none p-3 border-t border-stone-200">
        <div className="flex items-center gap-2 bg-stone-100 rounded-xl px-3 py-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={status === "connected" ? "Message…" : "Waiting for connection…"}
            disabled={status !== "connected"}
            className="flex-1 bg-transparent text-sm text-stone-800 placeholder:text-stone-400 outline-none disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || status !== "connected"}
            className="text-stone-400 hover:text-stone-700 disabled:opacity-30 transition-colors"
            aria-label="Send message"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path
                d="M14 8L2 2l2.5 6L2 14l12-6z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>
      </div>
    </aside>
  );
}