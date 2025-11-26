import React from 'react';
import { StepCard } from './StepCard';
import type { ProcessStepsBlocksProps } from '../model/types';
import { useProcessSteps } from '../model/useProcessSteps';

export const ProcessStepsBlocks: React.FC<ProcessStepsBlocksProps> = ({ steps: propsSteps }) => {
  const { steps: stepsFromPage } = useProcessSteps();
  const steps = propsSteps ?? stepsFromPage;

  return (
    <section className="w-full bg-[#F8F9FB] py-12">
      <div className="
        max-w-6xl 
        mx-auto 
        px-4
        sm:px-6
        lg:px-0
      ">

        <h2 className="text-3xl font-bold mb-10 text-black text-left">
          Как это работает
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {steps.map((step, index) => (
            <StepCard
              key={step.id}
              title={step.title}
              description={step.description}
              number={index + 1}
            />
          ))}
        </div>

      </div>
    </section>
  );
};