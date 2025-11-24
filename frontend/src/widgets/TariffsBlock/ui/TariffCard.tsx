import React from 'react';
import type { Tariff } from '../model/types';

export const TariffCard: React.FC<Tariff & { onClick?: () => void }> = ({
  name,
  label,
  description,
  price,
  features,
  button,
  isHighlighted,
  onClick,
}) => {
  const isPrimary = isHighlighted;

  return (
    <div
      onClick={onClick}
      className={`
        border rounded-xl p-5 flex flex-col gap-2 cursor-pointer
        bg-white
        transition-shadow transform hover:scale-[1.02] hover:shadow-lg
        ${isPrimary ? '!border-[#155CFA] shadow-md' : 'border-gray-200'}
      `}
    >
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold text-black">{name}</h3>
        {label && (
          <span className="px-2 py-1 text-xs rounded-md bg-[#EEF5FE] text-[#155CFA] font-medium">
            {label}
          </span>
        )}
      </div>

      <p className="text-sm text-[#6D7F96] mt-0.5">{description}</p>

      <div className="mt-1 flex items-end gap-1">
        <span className="text-3xl font-bold text-black leading-none">
          {price.split('/')[0]}
        </span>
        <span className="text-sm font-semibold text-[#6D7F96] leading-none">
          /{price.split('/')[1]}
        </span>
      </div>

      <ul className="flex flex-col gap-1.5 mt-3">
        {features.map((f) => (
          <li key={f.id} className="flex items-center gap-2 text-black text-sm">
            <span className="w-4 h-4 bg-[#47BD71] rounded-full flex items-center justify-center text-white text-xs">
              ✓
            </span>
            {f.text}
          </li>
        ))}
      </ul>

      <button
        className={`
          mt-4 w-full py-2 rounded-lg border text-sm
          ${isPrimary
            ? '!bg-[#155CFA] !text-white !border-[#155CFA]'
            : 'bg-white text-black border-gray-300'}
        `}
      >
        {button.label}
      </button>
    </div>
  );
};
