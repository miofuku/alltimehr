import React from 'react';
import { Layout, Typography } from 'antd';
import ApplicationForm from './components/ApplicationForm';

const { Header, Content } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const handleSubmit = (result: any) => {
    console.log('Application result:', result);
  };

  return (
    <Layout>
      <Header style={{ background: '#fff', padding: '0 20px' }}>
        <Title level={3} style={{ margin: '16px 0' }}>AI HR Agent</Title>
      </Header>
      <Content style={{ padding: '24px', minHeight: 'calc(100vh - 64px)' }}>
        <ApplicationForm onSubmit={handleSubmit} />
      </Content>
    </Layout>
  );
};

export default App; 