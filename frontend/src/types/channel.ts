interface Channel {
  id: number;
  name: string;
  subscribers: number;
  category: string;
  verified: boolean;
  country: string;
  imageUrl: string;
}

interface ChannelsProps {
  channels: Channel[];
}

export type { Channel, ChannelsProps};