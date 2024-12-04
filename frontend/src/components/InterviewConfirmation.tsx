import React from 'react';
import { Card, Typography } from 'antd';
import { formatDate, isPastDate } from '../utils/date';

interface InterviewConfirmationProps {
  interviewTime: string;
}

const InterviewConfirmation: React.FC<InterviewConfirmationProps> = ({ 
  interviewTime 
}) => {
  const formattedTime = formatDate(interviewTime);
  const isExpired = isPastDate(new Date(interviewTime));

  return (
    <Card title="Interview Confirmation">
      <Typography.Text>
        {isExpired 
          ? 'This interview slot has expired.' 
          : `Your interview is scheduled for ${formattedTime}`
        }
      </Typography.Text>
    </Card>
  );
};

export default InterviewConfirmation; 