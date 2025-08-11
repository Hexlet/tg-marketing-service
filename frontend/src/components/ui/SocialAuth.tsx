import React from "react";
import { SocialIcon } from "react-social-icons";

interface SocialAuthProps {
  network: string;
}

const SocialAuth: React.FC<SocialAuthProps> = ({ network }) => {
  return (
    <>
      <a href='#' className='!p-0 cursor-pointer'>
        <SocialIcon network={network} style={{ height: 40, width: 40 }} ></SocialIcon>
      </a>
    </>
  )
}

export default SocialAuth;
