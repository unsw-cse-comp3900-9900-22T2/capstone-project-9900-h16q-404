import React from 'react';
import { Button, Form, Input, message } from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  let navigate = useNavigate();
  const onFinish = (values) => {
    console.log('Input:', values);
    axios
      .post('http://127.0.0.1:5000/login', {
        username: values.username,
        password: values.password,
      })
      .then((res) => {
        //console.log(res.data);
        let status = res.data.status;
        // changed var name to use message function
        let info = res.data.message;
        if (status==='Error') {
          // change alert to antd message
          message.error(info);
        }
        else{
          localStorage.setItem('username', values.username);
          localStorage.setItem('token', values.username);
          //console.log(localStorage.getItem('username'));
          message.success("Login Successful!",2)
            .then(navigate('/'));
        }
      }, []);
    }


  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  return (
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
        Don't have an account? <a href='register'>Click here to Register!</a>
      </Form.Item>
    </Form>
  );
};

export default function LoginPage() {
  return <LoginForm></LoginForm>;
}
