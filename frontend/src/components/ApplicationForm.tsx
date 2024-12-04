import React, { useState } from 'react';
import { Upload, Form, Input, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';

interface ApplicationFormProps {
  onSubmit: (values: ApplicationData) => void;
}

interface ApplicationData {
  resume: UploadFile[];
  coverLetter?: UploadFile[];
}

const ApplicationForm: React.FC<ApplicationFormProps> = ({ onSubmit }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: ApplicationData) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('resume', values.resume[0].originFileObj as Blob);
      if (values.coverLetter?.[0]) {
        formData.append('cover_letter', values.coverLetter[0].originFileObj as Blob);
      }
      
      const response = await fetch('/api/applications', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      message.success('Application submitted successfully!');
      onSubmit(result);
    } catch (error) {
      message.error('Submission failed, please try again');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} onFinish={handleSubmit}>
      <Form.Item
        name="resume"
        label="Resume"
        rules={[{ required: true, message: 'Please upload your resume' }]}
      >
        <Upload accept=".pdf,.doc,.docx">
          <Button icon={<UploadOutlined />}>Upload Resume</Button>
        </Upload>
      </Form.Item>

      <Form.Item name="coverLetter" label="Cover Letter">
        <Upload accept=".pdf,.doc,.docx">
          <Button icon={<UploadOutlined />}>Upload Cover Letter (Optional)</Button>
        </Upload>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Submit Application
        </Button>
      </Form.Item>
    </Form>
  );
};

export default ApplicationForm; 