import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Celestial Atlas - Tower 6",
  description: "Prime Calendar & Star Mapping System - Stored. Retrievable. Kind.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased starfield-bg">
        {children}
      </body>
    </html>
  );
}
