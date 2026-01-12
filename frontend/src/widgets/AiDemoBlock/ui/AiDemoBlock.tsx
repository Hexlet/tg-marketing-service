import React from 'react';
import { AiDemoText } from './AiDemoText';
import { AiDemoWindow } from './AiDemoWindow';
import { useAiDemo } from '../model/useAiDemo';

export const AiDemoBlock: React.FC = () => {
  const { data, activeButton, handleButtonClick } = useAiDemo();

  return (
    <section className="w-full py-10">
      <div
        className="
          max-w-7xl
          mx-auto
          px-6
          flex
          flex-col
          lg:flex-row
          gap-8
          items-stretch
        "
      >
        <div className="flex-1 flex flex-col w-full">
          <h2 className="text-2xl font-bold text-black mb-4">
            ИИ-помощник редактора
          </h2>

          <AiDemoText
            {...data}
            activeButton={activeButton}
            onButtonClick={handleButtonClick}
          />
        </div>

        <div className="flex-1 w-full flex">
          <AiDemoWindow demoTitle={data.demoTitle} />
        </div>
      </div>
    </section>
  );
};

