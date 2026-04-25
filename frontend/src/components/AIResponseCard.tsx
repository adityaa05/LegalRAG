'use client'

import React from 'react';
import styled from 'styled-components';

const AIResponseCard = () => {
  return (
    <StyledWrapper>
      <div className="card">
        <div className="card_title__container">
          <div className="ai_badge">
            <span className="ai_text">AI</span>
          </div>
          <span className="card_title">AI Response</span>
        </div>
        <div className="response_content">
          <p className="query_text">
            Based on your query about <strong>murder cases in Indian law</strong>, here's what I found:
          </p>
          <p className="response_text">
            Murder is defined under Section 302 of the Indian Penal Code (IPC). It is one of the most serious 
            offenses under Indian criminal law, punishable by death or life imprisonment.
          </p>
          <div className="confidence_container">
            <span className="confidence_badge">Confidence: 95%</span>
            <span className="sources_text">Sources: 3 sections found</span>
          </div>
        </div>
      </div>
    </StyledWrapper>
  );
}

const StyledWrapper = styled.div`
  .card {
    --white: hsl(0, 0%, 100%);
    --black: hsl(240, 15%, 9%);
    --paragraph: hsl(0, 0%, 83%);
    --line: hsl(240, 9%, 17%);
    --primary: hsl(142, 76%, 36%);
    --ai-green: hsl(142, 76%, 36%);
    --bg-light: hsl(120, 60%, 97%);

    position: relative;

    display: flex;
    flex-direction: column;
    gap: 1rem;

    padding: 1.5rem;
    width: 100%;
    max-width: 100%;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    border-radius: 1rem;
    box-shadow: 0px -16px 24px 0px rgba(34, 197, 94, 0.15) inset;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }


  .card .card_title__container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
  }

  .card .ai_badge {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    background-color: var(--ai-green);
    border-radius: 50%;
  }

  .card .ai_text {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--white);
    font-family: "Duru Sans", sans-serif;
  }

  .card .card_title {
    font-size: 1.25rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    font-family: "Duru Sans", sans-serif;
  }

  .card .response_content {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 1rem;
    border-radius: 0.75rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .card .query_text {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    font-family: "Almarai", sans-serif;
  }

  .card .response_text {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
    line-height: 1.5;
    font-family: "Almarai", sans-serif;
  }

  .card .confidence_container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }

  .card .confidence_badge {
    background-color: hsla(142, 76%, 36%, 0.1);
    color: var(--ai-green);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    font-family: "Almarai", sans-serif;
  }

  .card .sources_text {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
    font-family: "Almarai", sans-serif;
  }
`;

export default AIResponseCard;
