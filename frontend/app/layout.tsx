import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Meta-Analysis Audit",
  description: "Audit published meta-analyses against their source evidence",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="topbar">
          <a href="/" className="brand">
            Meta-Analysis Audit
          </a>
        </header>
        <main className="main">{children}</main>
      </body>
    </html>
  );
}
