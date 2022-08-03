import { Form, Input, Button, message, Layout } from 'antd';
import axios from 'axios';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import PageHeader from '../components/page_header';
import logo from '../static/picacg.jpeg';

const { Content, Footer } = Layout;

const RegisterBox = styled.div`
  display: flex;
  flex-direction: column;
  width: 75%;
  margin-top: 50px;
  margin-bottom: 50px;
  padding-top: 20px;
  border: 1px solid black;
  border-radius: 5px;
  align-items: center;
  justify-content: center;
`;

const formItemLayout = {
  labelCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 8,
    },
  },
  wrapperCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 16,
    },
  },
};

const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 16,
      offset: 8,
    },
  },
};

const RegisterForm = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = (values) => {
    axios
      .post('http://127.0.0.1:5000/register', values)
      .then((response) => response.data)
      .then((data) => {
        if (data.status === 'Success') {
          message.success(
            'Register successful! Redirecting to login page...',
            2
          );
          navigate('/login');
        } else {
          message.error(data.message, 2);
        }
      })
      .catch(function (error) {
        message.error('Something wrong when registering...', 2);
      });
  };

  return (
    <div>
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
          <RegisterBox>
            <img
              src={logo}
              alt='logo'
              style={{ width: '100px', height: '100px', marginBottom: '20px' }}
            ></img>
            <Form
              {...formItemLayout}
              form={form}
              name='register'
              onFinish={onFinish}
            >
              <Form.Item
                name='email'
                label='E-mail'
                rules={[
                  {
                    type: 'email',
                    message: 'The input is not valid E-mail!',
                  },
                  {
                    required: true,
                    message: 'Please input your E-mail!',
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                name='password'
                label='Password'
                rules={[
                  {
                    required: true,
                    message: 'Please input your password!',
                  },
                ]}
                hasFeedback
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                name='confirm'
                label='Confirm Password'
                dependencies={['password']}
                hasFeedback
                rules={[
                  {
                    required: true,
                    message: 'Please confirm your password!',
                  },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                      }

                      return Promise.reject(
                        new Error(
                          'The two passwords that you entered do not match!'
                        )
                      );
                    },
                  }),
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item {...tailFormItemLayout}>
                <Button type='primary' htmlType='submit'>
                  Register
                </Button>
                <br />
                Already have an account? <br />{' '}
                <a href='login'>Click here to Log In!</a>
              </Form.Item>
            </Form>
          </RegisterBox>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </div>
  );
};

export default function RegisterPage() {
  return <RegisterForm />;
}
