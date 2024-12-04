import React, { useState } from 'react';
import { Upload, Form, Input, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

interface ApplicationFormProps {
  onSubmit: (values: any) => void;
}

const ApplicationForm: React.FC<ApplicationFormProps> = ({ onSubmit }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('resume', values.resume[0].originFileObj);
      if (values.coverLetter) {
        formData.append('cover_letter', values.coverLetter[0].originFileObj);
      }
      
      const response = await fetch('/api/applications', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      message.success('申请提交成功！');
      onSubmit(result);
    } catch (error) {
      message.error('提交失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form form={form} onFinish={handleSubmit}>
      <Form.Item
        name="resume"
        label="简历"
        rules={[{ required: true, message: '请上传简历' }]}
      >
        <Upload accept=".pdf,.doc,.docx">
          <Button icon={<UploadOutlined />}>上传简历</Button>
        </Upload>
      </Form.Item>

      <Form.Item name="coverLetter" label="求职信">
        <Upload accept=".pdf,.doc,.docx">
          <Button icon={<UploadOutlined />}>上传求职信（可选）</Button>
        </Upload>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          提交申请
        </Button>
      </Form.Item>
    </Form>
  );
};

export default ApplicationForm; 