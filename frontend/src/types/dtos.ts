/**
 * Файл: dtos.ts
 * Описание: Определяет структуры данных (DTO) для передачи информации между клиентом и сервером.
 * Используется для типизации API-ответов и обеспечения строгой типизации в TypeScript.
 */

export interface Contact {
  id: number;
  person: string;
  person_avatar?: string;
  department: "opt" | "employment";
  element: string;
  telegram: string; 
  is_telegram_active: boolean;
  session: string;
}

export interface DVInstruction {
  id: number;
  title: string;
  rows: DVInstructionRows[];
}

export interface DVInstructionRows {
  id: number;
  column1_text: string | null; 
  column1_image: string | null; 
  column2_text: string | null;
  column2_image: string | null;
  column3_text: string | null;
  column3_image: string | null;
}

export interface FAQ {
  id: number;
  position: number;
  question: string;
  answer: string;
  image?: string;
}

export interface MainPageButtonBlock {
  id: number;
  title: string;
  description: string;
  background_image?: string;
  link: string;
}

export interface MainPageReputationLink {
  id: number;
  title: string;
  image?: string;
  link: string;
}

export interface MainPageSlider {
  id: number;
  title: string;
  description: string;
  image?: string;
}

export interface City {
  id: number;
  name: string;
}

export interface Country {
  id: number;
  name: string;
  cities?: City[];
  code: string;
}

export interface ProductImage {
  id: number;
  image?: string;
}

export interface ProductItem {
  id: number;
  title: string;
  price: number;
  count: number;
  availability_status: "in_stock" | "preorder";
  updated_at: string;
}

export interface ProductItemAggregate {
  city: City;
  items?: ProductItem[];
}

export interface ProductList {
  id: number;
  title: string;
  description?: string;
  buy_url: string;
  images?: ProductImage[];
  items?: ProductItemAggregate[];
}

export interface Partnership {
  id: number;
  title: string;
  description?: string;
  image?: string;
  form_template?: number;
  short_description?: string; 
}

export interface ProjectLink {
  link: string;
  is_active: boolean;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  links?: ProjectLink[];
}

export interface Retail {
  id: number;
  name: string;
  link_type: string;
  link: string;
}

export interface Vacancy {
  id: number;
  image?: string;
  title: string;
  salary: number;
  short_description: string;
  description: string;
  salary_calc: boolean;
}

export interface Vacancy1 {
  id: number;
  name: string;
  image_url: string;
  work_format: string;
  description: string;
  salary: number;
  order_num: number;
  created_at: string;
  calc_showed: number;
}

export interface ResourcePolicy {
  id: number;
  heading: string;
  content: string;
  position: number;
}

export interface APIResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ResourcePolicy[];
}
