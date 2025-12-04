export interface AiDemoFeature {
  id: number;
  text: string;
}

export interface AiDemoButton {
  label: string;
  variant: 'default' | 'primary';
}

export interface AiDemoWindowProps {
demoTitle?: string;
}

export interface AiDemoBlockProps {
  description?: string;
  features?: AiDemoFeature[];
  tryButton?: AiDemoButton;
  demoButton?: AiDemoButton;
  demoTitle?: string;
}

export interface AiDemoTextProps extends AiDemoBlockProps {
activeButton: string;
onButtonClick: (button: AiDemoButton) => void;
}
