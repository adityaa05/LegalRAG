'use client'

import React from 'react';
import styled from 'styled-components';

interface PillButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
}

const PillButton: React.FC<PillButtonProps> = ({ children, onClick }) => {
  return (
    <StyledWrapper>
      <button className="small-button" onClick={onClick}>
        {children}
      </button>
    </StyledWrapper>
  );
}

const StyledWrapper = styled.div`
  /* <reset-style> ============================ */
  button {
    border: none;
    background: none;
    padding: 0;
    margin: 0;
    cursor: pointer;
    font-family: inherit;
  }
  /* <main-style> ============================ */
  .small-button {
    min-width: 104px;
    height: 40px;
    border-radius: 40px;
    background: #000;
    padding: 12px 28px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    font-size: 13px;
    font-weight: 400;
    line-height: 1;
    transition: background .2s ease-in-out, color .2s ease-in-out;
    position: relative;
  }

  .small-button::before {
    content: '';
    width: 100%;
    height: 100%;
    border-radius: 40px;
    background: linear-gradient(69deg, #c3aab2 -4.77%, #9ec 46.72%, #80c0c8 90.23%, #4B8bfa 134.46%);
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
    z-index: -1;
    transition: opacity .2s ease-in-out;
  }

  .small-button:hover {
    background: transparent;
    color: #000;
  }

  .small-button:hover::before {
    opacity: 1;
  }
`;

export default PillButton;
