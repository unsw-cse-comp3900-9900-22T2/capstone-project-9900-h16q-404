import React from 'react';
import { Button, Form, Input, message, Layout } from 'antd';
import PageHeader from '../components/page_header';
import logo from '../static/picacg.jpeg';
import axios from 'axios';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';

const LoginBox = styled.div`
  display: flex;
  flex-direction: column;
  width: 50%;
  margin-top: 50px;
  margin-bottom: 50px;
  padding-top: 20px;
  border: 1px solid black;
  border-radius: 5px;
  align-items: center;
  justify-content: center;
`;

const { Content, Footer } = Layout;

const LoginForm = () => {
  let navigate = useNavigate();
  const onFinish = (values) => {
    axios
      .post('http://127.0.0.1:5000/login', {
        username: values.username,
        password: values.password,
      })
      .then((res) => {
        let status = res.data.status;
        // changed var name to use message function
        let info = res.data.message;
        if (status === 'Error') {
          // change alert to antd message
          message.error(info);
        } else {
          localStorage.setItem('username', info.email);
          localStorage.setItem('token', info.token);
          localStorage.setItem('userId', info.userId);
          localStorage.setItem('userIcon', info.image);
          message.success('Login Successful!', 2).then(navigate('/'));
        }
      }, []);
  };

  const onFinishFailed = (errorInfo) => {
    message.error(errorInfo);
  };

  return (
    <>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{
            padding: '0 50px',
            marginTop: 64,
            display: 'flex',
            alignItems: 'center',
            flexDirection: 'column',
          }}
        >
          <LoginBox>
            <img
              src={logo}
              alt='logo'
              style={{ width: '100px', height: '100px', marginBottom: '20px' }}
            ></img>
            <Form
              name='basic'
              labelCol={{
                span: 8,
              }}
              wrapperCol={{
                span: 16,
              }}
              initialValues={{
                remember: true,
              }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete='off'
            >
              <Form.Item
                label='E-mail'
                name='username'
                rules={[
                  {
                    required: true,
                    message: 'Please input your username!',
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label='Password'
                name='password'
                rules={[
                  {
                    required: true,
                    message: 'Please input your password!',
                  },
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                wrapperCol={{
                  offset: 8,
                  span: 16,
                }}
              >
                <Button type='primary' htmlType='submit'>
                  Login
                </Button>
                <br />
                Don't have an account? <br />{' '}
                <a href='register'>Click here to Register!</a>
              </Form.Item>
            </Form>
          </LoginBox>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </>
  );
};

export default function LoginPage() {
  return <LoginForm></LoginForm>;
}
