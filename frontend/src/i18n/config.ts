export type Locale = (typeof locales)[number];

export const locales = [
  "ru",
  "en",
  "zh",
  "pt",
  "es",
  "hi",
  "ar",
  "kk",
  "hy",
  "az",
  "ro",
  "ky",
  "uz",
  "tg",
  "tr",
  "uk"
] as const;
export const defaultLocale: Locale = "ru";
