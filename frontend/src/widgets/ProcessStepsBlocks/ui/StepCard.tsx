import React from 'react';
import type { StepCardProps } from '../model/types';

export const StepCard: React.FC<StepCardProps> = ({ title, description, number }) => {
  return (
    <div className="
      bg-white 
      border border-gray-200 
      rounded-xl 
      p-4 md:p-6 
      flex flex-col 
      items-start 
      shadow-sm
    ">
      <div
        className="
          w-10 h-10 md:w-12 md:h-12 
          rounded-full 
          mb-4 
          flex items-center justify-center 
          bg-[#EEF5FE]
        "
      >
        <span className="text-[#426CEB] font-bold text-base md:text-lg">
          {number}
        </span>
      </div>

      <h3 className="text-base md:text-lg font-semibold text-black mb-2">
        {title}
      </h3>

      <p className="text-sm text-black leading-relaxed">
        {description}
      </p>
    </div>
  );
};
