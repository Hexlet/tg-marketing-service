import { useState } from 'react';
import { usePage } from '@inertiajs/react';
import type { Tariff } from './types';

export const useTariffsBlock = (): {
  tariffs: Tariff[];
  activeTariffId: number | null;
  setActiveTariffId: (id: number) => void;
} => {
  const { tariffs = [] } = usePage<{ tariffs: Tariff[] }>().props;

  const [activeTariffId, setActiveTariffId] = useState<number | null>(
    tariffs.find(t => t.isHighlighted)?.id ?? null
  );

  return { tariffs, activeTariffId, setActiveTariffId };
};
