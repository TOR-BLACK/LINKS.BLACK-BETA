import type { Metadata } from "next";
import localFont from "next/font/local";
import "./style/index.scss";
import Header from "@/components/Header/Header";
import { ThemeProvider } from "@/components/Theme/theme-provider";
import Footer from "@/components/Footer/Footer";
import { getLocale, getMessages } from "next-intl/server";
import { NextIntlClientProvider } from "next-intl";
import ChatButton from "@/components/ChatButton/ChatButton";

const montserrat = localFont({
  src: [
    {
      path: "./fonts/Montserrat-Light.woff2",
      weight: "300",
      style: "normal",
    },
    {
      path: "./fonts/Montserrat-Regular.woff2",
      weight: "400",
      style: "normal",
    },
    {
      path: "./fonts/Montserrat-Medium.woff2",
      weight: "500",
      style: "normal",
    },
    {
      path: "./fonts/Montserrat-SemiBold.woff2",
      weight: "600",
      style: "normal",
    },
    {
      path: "./fonts/Montserrat-Bold.woff2",
      weight: "700",
      style: "normal",
    },
    {
      path: "./fonts/Montserrat-Black.woff2",
      weight: "900",
      style: "normal",
    },
  ],
  variable: "--font-montserrat",
});

const futuraPt = localFont({
  src: [
    {
      path: "./fonts/FuturaPT-Heavy.woff2",
      weight: "900",
      style: "normal",
    },
  ],
  variable: "--font-futura-pt",
});

export const metadata: Metadata = {
  title: "localhost Webgram market",
  description: "Webgram market",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await getLocale();

  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body className={`${montserrat.variable} ${futuraPt.variable}`}>
        <NextIntlClientProvider messages={messages}>
          <ThemeProvider
            attribute="class"
            defaultTheme="dark"
            enableSystem
            disableTransitionOnChange
          >
            <Header />
            <main>{children}</main>
            <Footer />
            <ChatButton />
          </ThemeProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
