export interface FaqItem {
  id: number;
  question: string;
  answer: string;
}

export interface FaqBlockProps {
  faqs?: FaqItem[];
}

export interface FaqAccordionItemProps
  extends Omit<FaqItem, 'id'> {
  isOpen: boolean;
  onToggle: () => void;
}
