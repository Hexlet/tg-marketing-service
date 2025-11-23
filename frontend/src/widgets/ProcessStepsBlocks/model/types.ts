export interface Step {
  id: number;
  title: string;
  description: string;
}

export interface ProcessStepsBlocksProps {
  steps?: Step[];
}

export interface StepCardProps extends Omit<Step, 'id'> {
  number?: number;
}
