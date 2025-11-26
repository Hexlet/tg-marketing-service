import { usePage } from '@inertiajs/react';
import type { Step } from './types';

export const useProcessSteps = (): { steps: Step[] } => {
  const { steps = [] } = usePage<{ steps: Step[] }>().props;
  return { steps };
};
