import React from 'react';
import type { Channel } from '@/types/channel';

interface ChannelProps {
  channel: Channel;
  height: string;
}

const ChannelCard: React.FC<ChannelProps> = ({ channel, height }) => {
  const { name, subscribers, imageUrl } = channel;
  return (
    <div
      className={`h-${height} flex items-center justify-between p-2 px-5 gap-2 border bg-background rounded-md shadow-xs truncate`}
    >
      <div className="h-10 w-10 bg-gray-200 grow-0 flex-shrink-0 rounded-md ">
        <img
          src={imageUrl}
          className="w-full h-full object-cover"
          alt="аватар канала"
        />
      </div>
      <div
        className={`h-15 flex flex-col items-start justify-center basis-2/3 min-w-37 md:min-w-30 lg:min-w-31`}
      >
        <a href="#" className={`font-bold text-md truncate w-full block`}>
          {`${name}`}
        </a>
        <p className="text-xs lg:text-sm text-gray-500 truncate w-full">
          {new Intl.NumberFormat('ru-RU').format(subscribers)} подписчиков
        </p>
      </div>
      <a href="#" className=" collapse xl:visible text-xs font-semi bold">
        Открыть
      </a>
    </div>
  );
};

export default ChannelCard;
