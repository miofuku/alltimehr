import React, { useEffect, useState } from 'react';
import { Card, Typography, Spin, Result } from 'antd';
import { formatDate } from '../utils/date';
import api from '../utils/api';

const { Text } = Typography;

interface InterviewConfirmationProps {
  token: string;
}

interface ConfirmationResult {
  status: string;
  message: string;
  event_id?: string;
  time?: string;
}

const InterviewConfirmation: React.FC<InterviewConfirmationProps> = ({ token }) => {
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<ConfirmationResult | null>(null);

  useEffect(() => {
    const confirmInterview = async () => {
      try {
        const { data } = await api.post<ConfirmationResult>(
          `/api/interview/confirm/${token}`
        );
        setResult(data);
      } catch (error) {
        setResult({
          status: 'error',
          message: 'Failed to confirm interview. Please contact HR.',
        });
      } finally {
        setLoading(false);
      }
    };

    confirmInterview();
  }, [token]);

  if (loading) {
    return <Spin tip="Confirming your interview..." />;
  }

  if (!result) {
    return <Result status="error" title="Something went wrong" />;
  }

  return (
    <Card title="Interview Confirmation">
      <Result
        status={result.status === 'success' ? 'success' : 'error'}
        title={result.message}
        subTitle={
          result.time && (
            <Text>
              Interview scheduled for: {formatDate(result.time)}
            </Text>
          )
        }
      />
    </Card>
  );
};

export default InterviewConfirmation; 