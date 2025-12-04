import React from 'react';
import type { AiDemoBlockProps } from '../model/types';

export const AiDemoWindow: React.FC<AiDemoBlockProps> = ({ demoTitle }) => {
  return (
    <div
      className="flex-1 w-full rounded-xl border p-4 bg-white flex min-h-[15rem] lg:min-h-0"
    >
      <div
        className="w-full h-full rounded-lg flex items-center justify-center p-4"
        style={{ backgroundColor: '#F8F9FB' }}
      >
        <span className="text-5xl" style={{ color: '#94A2B8' }}>
          {demoTitle || 'AI Assistant Chat'}
        </span>
      </div>
    </div>
  );
};
