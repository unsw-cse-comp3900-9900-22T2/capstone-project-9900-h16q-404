import React from 'react';
import { Layout, Card } from 'antd';
import PageHeader from '../components/page_header';

const { Content, Footer } = Layout;

export default function LandingPage () {
  return (
    <div className='App'>
      <Layout>
        <PageHeader/>
        <Content style={{marginTop: '100px'}}>
          <Card title="testing_card" style={{
            idth: 300,
          }}>
            <p>Card content</p>
            <p>Card Content</p>
            <p>Card Content</p>
            <p>Card content</p>
            <p>Card Content</p>
            <p>Card Content</p>
          </Card>
          <Card title="testing_card_2" style={{
            idth: 300,
          }}>
            <p>Card content</p>
            <p>Card Content</p>
            <p>Card Content</p>
            <p>Card content</p>
            <p>Card Content</p>
            <p>Card Content</p>
          </Card>
        </Content>
        <Footer>
          9900-H16Q-404
        </Footer>
      </Layout>
    </div>
  )
}