import React, { useState } from 'react';
import type { TariffsBlockProps } from '../model/types';
import { useTariffsBlock } from '../model/useTariffsBlock';
import { TariffCard } from './TariffCard';

export const TariffsBlock: React.FC<TariffsBlockProps> = ({ tariffs: propsTariffs }) => {
  const { tariffs: tariffFromPage } = useTariffsBlock();

  const tariffs = propsTariffs ?? tariffFromPage;

  const [activeTariffId, setActiveTariffId] = useState<number>(
    tariffs?.find((t) => t.isHighlighted)?.id || tariffs?.[0]?.id || 0
  );

  if (!tariffs || tariffs.length === 0) return null;

  return (
    <section className="w-full bg-[#FEFEFE] py-16">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-black text-center mb-4">Тарифы</h2>
        <p className="text-center text-[#6D7F96] text-base mb-12 max-w-2xl mx-auto">
          Начните бесплатно. Обновляйтесь по мере роста команды и запросов.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {tariffs.map((tariff) => (
            <TariffCard
              key={tariff.id}
              {...tariff}
              isHighlighted={tariff.id === activeTariffId}
              onClick={() => setActiveTariffId(tariff.id)}
            />
          ))}
        </div>
      </div>
    </section>
  );
};
