import type { Metadata } from "next";
import { Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";

const mono = Geist_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "Nonogram",
  description: "Japanese crossword puzzles",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full antialiased overflow-hidden bg-white">
        <AuthProvider>
          {/* Main Wrapper */}
          <div className="flex flex-col h-full">
            
            {/* Navbar: flex-none prevents it from shrinking to 0px */}
            <nav className="flex-none h-14 bg-white border-b border-gray-200 z-50">
              <div className="max-w-6xl mx-auto px-6 h-full flex items-center justify-between">
                <Navbar />
              </div>
            </nav>

            {/* Main Area: flex-1 takes up all space under the navbar */}
            <main className="flex-1 flex overflow-hidden">
              {children}
            </main>
            
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
