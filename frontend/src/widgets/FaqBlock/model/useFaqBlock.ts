import { usePage } from '@inertiajs/react';
import type { FaqItem } from './types';

export const useFaqBlock = (): { faqs: FaqItem[] } => {
  const { faqs = [] } = usePage<{ faqs: FaqItem[] }>().props;

  return { faqs };
};
