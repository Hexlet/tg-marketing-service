import type { Channel } from '@/types/channel';

const reduceChannelsByCategory = (
  acc: { [category: string]: Channel[] },
  channel: Channel
) => {
  if (!acc[channel.category]) {
    acc[channel.category] = [];
  }
  acc[channel.category].push(channel);
  return acc;
};

type CategoriesCount = Record<string, number>;
type CategoryCountEntry = [string, number];

const countChannelsByCategory = (
  acc: CategoriesCount,
  channel: Channel
): CategoriesCount => {
  acc[channel.category] = (acc[channel.category] || 0) + 1;
  return acc;
};

const mapCategoryCountEntry = ([category, count]: CategoryCountEntry) => ({
  category,
  count,
});
export {
  reduceChannelsByCategory,
  countChannelsByCategory,
  mapCategoryCountEntry,
};
