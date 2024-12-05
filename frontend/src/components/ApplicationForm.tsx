import React, { useState } from 'react';
import { Upload, Form, Button, message, Card, Typography } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';
import api from '../utils/api';

const { Text } = Typography;

interface ApplicationFormProps {
  onSubmit: (result: ApplicationResult) => void;
}

interface ApplicationResult {
  status: string;
  analysis?: {
    education: any;
    experience: any;
    skills: string[];
    overall_assessment: string;
    recommendation: string;
  };
  message: string;
}

const ApplicationForm: React.FC<ApplicationFormProps> = ({ onSubmit }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApplicationResult | null>(null);

  const handleSubmit = async (values: { resume: UploadFile[]; coverLetter?: UploadFile[] }) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('resume', values.resume[0].originFileObj as Blob);
      if (values.coverLetter?.[0]) {
        formData.append('cover_letter', values.coverLetter[0].originFileObj as Blob);
      }
      
      const { data } = await api.post<ApplicationResult>('/api/applications', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setResult(data);
      message.success('Application processed successfully!');
      onSubmit(data);
    } catch (error) {
      message.error('Failed to process application. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Form form={form} onFinish={handleSubmit}>
        <Form.Item
          name="resume"
          label="Resume"
          rules={[{ required: true, message: 'Please upload your resume' }]}
        >
          <Upload accept=".pdf,.doc,.docx" maxCount={1}>
            <Button icon={<UploadOutlined />}>Upload Resume</Button>
          </Upload>
        </Form.Item>

        <Form.Item name="coverLetter" label="Cover Letter">
          <Upload accept=".pdf,.doc,.docx" maxCount={1}>
            <Button icon={<UploadOutlined />}>Upload Cover Letter (Optional)</Button>
          </Upload>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Submit Application
          </Button>
        </Form.Item>
      </Form>

      {result && (
        <Card title="Application Analysis" style={{ marginTop: 20 }}>
          <Text strong>Status: </Text>
          <Text>{result.status}</Text>
          
          {result.analysis && (
            <>
              <div style={{ marginTop: 16 }}>
                <Text strong>Skills Assessment:</Text>
                <ul>
                  {result.analysis.skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              </div>
              
              <div style={{ marginTop: 16 }}>
                <Text strong>Overall Assessment:</Text>
                <p>{result.analysis.overall_assessment}</p>
              </div>
              
              <div style={{ marginTop: 16 }}>
                <Text strong>Recommendation:</Text>
                <p>{result.analysis.recommendation}</p>
              </div>
            </>
          )}
          
          <div style={{ marginTop: 16 }}>
            <Text strong>Message: </Text>
            <Text>{result.message}</Text>
          </div>
        </Card>
      )}
    </>
  );
};

export default ApplicationForm; 