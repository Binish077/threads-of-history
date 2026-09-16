import type { Metadata } from "next";

import "./styles/globals.css";

export const metadata: Metadata = {
  title: "Threads of History",
  description: "A temporal history simulator for Westeros.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
