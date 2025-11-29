import React, { useState } from 'react';
import type { FaqBlockProps } from '../model/types';
import { FaqItem } from './FaqItem';
import { useFaqBlock } from '../model/useFaqBlock';

export const FaqBlock: React.FC<FaqBlockProps> = ({ faqs: propsFaqs }) => {
  const { faqs: faqsFromPage } = useFaqBlock();
  const faqs = propsFaqs ?? faqsFromPage;

  const [openFaqId, setOpenFaqId] = useState<number | null>(null);

  const handleToggle = (id: number) => {
    setOpenFaqId(prev => (prev === id ? null : id));
  };

  return (
    <section className="bg-[#F8F9FB] py-12">
      <div className="container mx-auto px-4 sm:px-6 text-center">
        <h2 className="text-2xl font-bold mb-8">Частые вопросы</h2>

        <div className="max-w-2xl mx-auto bg-white border border-gray-300 rounded-lg overflow-hidden shadow-sm">
          {faqs.map(faq => (
            <FaqItem
              key={faq.id}
              question={faq.question}
              answer={faq.answer}
              isOpen={openFaqId === faq.id}
              onToggle={() => handleToggle(faq.id)}
            />
          ))}
        </div>
      </div>
    </section>
  );
};
