import React from "react";

interface DividerProps {
	text: string;
}

const Divider: React.FC<DividerProps> = ({ text }) => {
	return (
		<div className='flex items-center justify-between gap-2'>
			<span className='w-full h-px bg-gray-300 block' ></span >
			<span className='text-lg text-gray-400'>
				{text}
			</span>
			<span className='w-full h-px bg-gray-300 block'></span>
		</div >
	)
}

export default Divider;
