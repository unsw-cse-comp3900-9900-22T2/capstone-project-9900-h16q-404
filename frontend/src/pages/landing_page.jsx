import React, { useEffect } from 'react';
import { Layout, Card } from 'antd';
import PageHeader from '../components/page_header';
//import request from '../utils/request';

const { Content, Footer } = Layout;

export default function LandingPage () {

  // hook
  useEffect(()=>{
    const init = {
      mode: 'no-cors'
    }
    fetch('http://127.0.0.1:5000/events', init)
      .then(res => {
        console.log(JSON.stringify(res));
        return;
      })
  }, []);

  return (
    <div className='App'>
      <Layout>
        <PageHeader/>
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <Card title="testing_card" style={{
            idth: 300,
          }}>
            <p>Card content</p>
            <p>Card Content</p>
          </Card>
          <Card title="testing_card_2" style={{
            idth: 300,
          }}>
            <p>Card content</p>
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