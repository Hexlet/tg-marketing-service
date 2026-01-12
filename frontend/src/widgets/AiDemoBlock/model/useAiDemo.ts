import { useState } from 'react';
import { usePage } from '@inertiajs/react';
import type { AiDemoBlockProps, AiDemoButton } from './types';

export const useAiDemo = (): {
  data: AiDemoBlockProps;
  activeButton: string;
  handleButtonClick: (button: AiDemoButton) => void;
} => {
  const { aiDemo = {} } = usePage<{ aiDemo: AiDemoBlockProps }>().props;

  const [activeButton, setActiveButton] = useState<string>(aiDemo.tryButton?.label || '');

  const handleButtonClick = (button: AiDemoButton) => {
    setActiveButton(button.label);
  };

  return {
    data: {
      description: aiDemo.description ?? '',
      features: aiDemo.features ?? [],
      tryButton: aiDemo.tryButton,
      demoButton: aiDemo.demoButton,
      demoTitle: aiDemo.demoTitle ?? '',
    },
    activeButton,
    handleButtonClick,
  };
};
