import React from 'react';
import type { AiDemoTextProps } from '../model/types';

import {
  PlayCircleIcon,
  SparklesIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';

export const AiDemoText: React.FC<AiDemoTextProps> = ({
  description,
  features = [],
  tryButton,
  demoButton,
  activeButton,
  onButtonClick,
}) => {
  return (
    <div className="flex flex-col gap-4">
      {description && (
        <p className="text-[#6D7F96] text-base">{description}</p>
      )}

      <ul className="flex flex-col gap-2">
        {features.map((f) => (
          <li
            key={f.id}
            className="flex items-center gap-2 text-[#6D7F96] text-sm"
          >
            <CheckCircleIcon className="w-5 h-5 text-[#47BD71]" />
            {f.text}
          </li>
        ))}
      </ul>

      <div className="flex gap-3 mt-4">
        {tryButton && (
          <button
            onClick={() => onButtonClick(tryButton)}
            className={`
              px-5 py-2 rounded-lg border text-sm flex items-center gap-2 transition
              ${
                activeButton === tryButton.label
                  ? '!bg-[#155CFA] !text-white !border-[#155CFA]'
                  : 'bg-white text-black border-gray-300'
              }
            `}
          >
            <SparklesIcon className="w-5 h-5" />
            {tryButton.label}
          </button>
        )}

        {demoButton && (
          <button
            onClick={() => onButtonClick(demoButton)}
            className={`
              px-5 py-2 rounded-lg border text-sm flex items-center gap-2 transition
              ${
                activeButton === demoButton.label
                  ? '!bg-[#155CFA] !text-white !border-[#155CFA]'
                  : 'bg-white text-black border-gray-300'
              }
            `}
          >
            <PlayCircleIcon className="w-5 h-5" />
            {demoButton.label}
          </button>
        )}
      </div>
    </div>
  );
};
