"use client";
import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { getPuzzle, getAttempts, createAttempt, updateAttempt } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { ChatProvider } from "@/context/ChatContext";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { useMemo } from "react";

interface Puzzle {
  id: number;
  title: string;
  author_username: string;
  hor_size: number;
  ver_size: number;
  difficulty: string;
  row_clues: number[][];
  col_clues: number[][];
}

interface Attempt {
  id: number;
  puzzle_id: number;
  status: string;
  current_grid: number[][];
}

export default function PuzzlePage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [puzzle, setPuzzle] = useState<Puzzle | null>(null);
  const [attempt, setAttempt] = useState<Attempt | null>(null);
  const [grid, setGrid] = useState<number[][]>([]);
  const [solved, setSolved] = useState(false);
  const [loading, setLoading] = useState(true);
  const [completedRowClues, setCompletedRowClues] = useState<Set<string>>(new Set());
  const [completedColClues, setCompletedColClues] = useState<Set<string>>(new Set());
  const [painting, setPainting] = useState<number | null>(null);
  const chatSidebar = useMemo(() => (
    <ChatProvider roomId={String(id)}>
      <ChatWindow currentUsername={user?.name ?? "Anonymous"} />
    </ChatProvider>
  ), [id, user?.name]);

  useEffect(() => {
    const load = async () => {
      const p = await getPuzzle(Number(id));
      setPuzzle(p);
      if (user) {
        const attempts = await getAttempts();
        const existing = attempts.find((a: Attempt) => a.puzzle_id === Number(id));
        if (existing) {
          setAttempt(existing);
          setGrid(existing.current_grid);
          setSolved(existing.status === "completed");
        } else {
          const newAttempt = await createAttempt(Number(id));
          setAttempt(newAttempt);
          setGrid(newAttempt.current_grid);
        }
      } else {
        // If no user, initialize a blank grid based on puzzle dimensions
        setGrid(Array.from({ length: p.ver_size }, () => Array(p.hor_size).fill(0)));
      }
      setLoading(false);
    };
    load();
  }, [id, user]);

  const handleMouseDown = (r: number, c: number, e: React.MouseEvent) => {
    if (!puzzle || solved) return;
    let newVal: number;
    if (e.button === 0) {
      newVal = grid[r][c] === 1 ? 0 : 1;
    } else if (e.button === 2) {
      newVal = grid[r][c] === 2 ? 0 : 2;
    } else {
      return;
    }
    setPainting(newVal);
    const newGrid = grid.map((row, ri) =>
      row.map((cell, ci) => (ri === r && ci === c ? newVal : cell))
    );
    setGrid(newGrid);
  };

  const handleMouseEnter = (r: number, c: number) => {
    if (painting === null || !puzzle || solved) return;
    const newGrid = grid.map((row, ri) =>
      row.map((cell, ci) => (ri === r && ci === c ? painting : cell))
    );
    setGrid(newGrid);
  };

  const stopPainting = useCallback(async () => {
    if (painting === null || !puzzle || solved) return;
    setPainting(null);
    if (user && attempt) {
      const updated = await updateAttempt(attempt.id, grid);
      if (updated.status === "completed") {
        setSolved(true);
        setGrid(updated.current_grid);
      }
    }
  }, [grid, attempt, solved, painting, user, puzzle]);

  if (loading) return <div className="text-center py-20 text-gray-500">Loading...</div>;
  if (!puzzle) return <div className="text-center py-20 text-gray-500">Puzzle not found</div>;

  const maxRowClue = Math.max(...puzzle.row_clues.map((r) => r.length));
  const maxColClue = Math.max(...puzzle.col_clues.map((c) => c.length));

  

  return (
    <div className="flex h-full w-full">
      {/* Puzzle area */}
      <section className="flex-1 overflow-auto px-8">
        <div className="py-10">
          <div className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight mb-1">{puzzle.title}</h1>
            <p className="text-gray-600 text-sm">
              {puzzle.hor_size}×{puzzle.ver_size} · {puzzle.difficulty} · by {puzzle.author_username}
            </p>
          </div>

          {solved && (
            <div className="mb-6 bg-green-900/30 border border-green-800 rounded-xl px-5 py-4 text-black font-semibold">
              ✓ Puzzle solved!
            </div>
          )}

          {!user && (
            <div className="mb-6 bg-gray-100 border border-gray-300 rounded-xl px-5 py-4 text-gray-700 text-sm">
              Sign in to save your progress
            </div>
          )}

          <div
            className="overflow-auto select-none"
            onMouseLeave={stopPainting}
            onMouseUp={stopPainting}
            onContextMenu={(e) => e.preventDefault()}
          >
            <table className="border-collapse" style={{ fontFamily: "var(--font-mono)" }}>
              <thead>
                {Array.from({ length: maxColClue }).map((_, ci) => (
                  <tr key={ci}>
                    <td colSpan={maxRowClue} />
                    {puzzle.col_clues.map((clue, col) => {
                      const clueIndex = ci - (maxColClue - clue.length);
                      const clueKey = `col-${col}-${clueIndex}`;
                      const isCompleted = completedColClues.has(clueKey);
                      return (
                        <td
                          key={col}
                          onClick={() => {
                            const newSet = new Set(completedColClues);
                            if (newSet.has(clueKey)) newSet.delete(clueKey);
                            else newSet.add(clueKey);
                            setCompletedColClues(newSet);
                          }}
                          className={`w-8 h-8 text-xs cursor-pointer select-none transition-colors hover:bg-gray-100 ${
                            isCompleted ? "line-through text-gray-300" : "text-gray-600 font-bold"
                          } ${clue[clueIndex] !== undefined ? "border border-gray-300" : ""}`}
                        >
                          <div className="flex items-center justify-center w-full h-full">
                            {clue[clueIndex] ?? ""}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </thead>
              <tbody>
                {grid.map((row, ri) => (
                  <tr key={ri}>
                    {Array.from({ length: maxRowClue - puzzle.row_clues[ri].length }).map((_, i) => (
                      <td key={`empty-${ri}-${i}`} className="w-8 h-8" />
                    ))}
                    {puzzle.row_clues[ri].map((n, i) => {
                      const clueKey = `row-${ri}-${i}`;
                      const isCompleted = completedRowClues.has(clueKey);
                      return (
                        <td
                          key={i}
                          onClick={() => {
                            const newSet = new Set(completedRowClues);
                            if (newSet.has(clueKey)) newSet.delete(clueKey);
                            else newSet.add(clueKey);
                            setCompletedRowClues(newSet);
                          }}
                          className={`w-8 h-8 text-xs cursor-pointer select-none transition-colors hover:bg-gray-100 ${
                            isCompleted ? "line-through text-gray-300" : "text-gray-600 font-bold"
                          } ${n ? "border border-gray-300" : ""}`}
                        >
                          <div className="flex items-center justify-center w-full h-full">
                            {n}
                          </div>
                        </td>
                      );
                    })}
                    {row.map((cell, ci) => (
                      <td
                        key={ci}
                        onMouseDown={(e) => handleMouseDown(ri, ci, e)}
                        onMouseEnter={() => handleMouseEnter(ri, ci)}
                        className={`
                          w-8 h-8 border border-gray-500
                          cursor-pointer transition-colors select-none relative
                          ${cell === 1 ? "bg-black" : "bg-white hover:bg-gray-50"}
                          ${ci % 5 === 0 ? "border-l-2 border-l-zinc-500" : ""}
                          ${ri % 5 === 0 ? "border-t-2 border-t-zinc-500" : ""}
                        `}
                      >
                        {cell === 2 && (
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-1.5 h-1.5 bg-gray-400 rounded-full" />
                          </div>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Chat sidebar */}
      {/* <ChatProvider roomId={String(id)}>
        <ChatWindow currentUsername={user?.name ?? "Anonymous"} />
      </ChatProvider> */}
      {chatSidebar}
    </div>
  );
}