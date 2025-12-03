import type { FaqAccordionItemProps } from '../model/types';

export const FaqItem: React.FC<FaqAccordionItemProps> = ({
  question,
  answer,
  isOpen,
  onToggle,
}) => {
  return (
    <div className="last:border-none w-full">
      {/* Линия между вопросами полностью по ширине */}
      <div className="border-b border-gray-200 w-full">
        <button
          onClick={onToggle}
          className="w-full flex items-center justify-between text-left px-4 py-3 !bg-white"
        >
          <span className="font-semibold text-base">{question}</span>

          {isOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-4 h-4 text-gray-700 transition-transform duration-300"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m19.5 8.25-7.5 7.5-7.5-7.5"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-4 h-4 text-gray-700 transition-transform duration-300"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m8.25 4.5 7.5 7.5-7.5 7.5"
              />
            </svg>
          )}
        </button>
      </div>

      {isOpen && (
        <p className="px-4 py-3 text-[15px] text-[#6D7F96] text-left">
          {answer}
        </p>
      )}
    </div>
  );
};
