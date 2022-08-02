import React, { useEffect, useState } from 'react';
import {
  Layout,
  Select,
  Button,
  Form,
  Input,
  Space,
  Cascader,
  message,
} from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import PageHeader from '../components/page_header';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const { Content, Footer } = Layout;

const formItemLayout = {
  labelCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 4,
    },
  },
  wrapperCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 20,
    },
  },
};

const formItemLayoutWithOutLabel = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 20,
      offset: 4,
    },
  },
};

export default function BuyTicket() {
  const params = useParams();
  const eventid = params.eventid;
  const navigate = useNavigate();
  const [token, setToken] = useState();
  const [total, setTotal] = useState(0);
  // const dict = { gold: [1, 2, 3, 5, 6, 10], silver: [1, 3, 5, 7], bronze: [0] };

  const [options, setOptions] = useState();

  const filter = (inputValue, path) => {
    path.some(
      (option) =>
        option.label.toLowerCase().indexOf(inputValue.toLowerCase()) > -1
    );
  };

  useEffect(() => {
    if (localStorage.getItem('username')) {
      setToken(localStorage.getItem('username'));
    } else {
      message.error('You must log in to do this!');
      navigate(-1);
    }

    axios
      .get(`http://127.0.0.1:5000/buytickets`, {
        params: {
          event_id: eventid,
        },
      })
      .then((res) => {
        if (res.data.resultStatus === 'SUCCESS') {
          // console.log(res.data.message);
          const newdata = {};
          for (const value of res.data.message.result) {
            const combine = [
              value.tix_class,
              value.ticket_price.toString(),
            ].join();
            if (newdata[combine] === undefined) {
              newdata[combine] = [];
            }
            newdata[combine].push(value.seat_num);
          }
          const newoptions = [];
          for (const [key, value] of Object.entries(newdata)) {
            if (value.length > 0) {
              const labels = key.toString().split(',');
              const label = 'Price: AUD' + labels[1] + ', ' + labels[0];
              const option = {
                value: key,
                label: label,
                children: value.map((item) => {
                  return {
                    value: item,
                    label: item.toString(),
                  };
                }),
              };
              newoptions.push(option);
            }
          }
          setOptions(newoptions);
        } else {
          message.error(res.data.message);
        }
      });
  }, [setOptions]);

  function convertForm(formValues) {
    const stringlist = [];
    const tickets = [];
    if (formValues.tickets === undefined) return [];
    for (const value of formValues.tickets) {
      if (value !== undefined) {
        if (!stringlist.includes(value.join())) {
          stringlist.push(value.join());
          tickets.push({
            event_id: eventid,
            seat_num: value[1],
            tix_class: value[0].split(',')[0],
            card_number: formValues.card_number,
            ticket_price: parseInt(value[0].split(',')[1]),
          });
        }
      }
    }
    // console.log(tickets);
    return tickets;
  }

  const onvalueChange = (changedFields, allFields) => {
    const tickets = convertForm(allFields);
    if (tickets.length === 0) {
      setTotal(0);
    } else {
      let num = 0;
      for (const tix of tickets) {
        num += tix.ticket_price;
      }
      setTotal(num);
    }
  };

  const onFinish = (values) => {
    const tickets = convertForm(values);
    if (tickets.length === 0) {
      message.warning('At least 1 ticket');
      return;
    }
    console.log(tickets);
    axios
      .post(`http://127.0.0.1:5000/buytickets`, {
        token: token,
        tickets: tickets,
      })
      .then((res) => {
        if (res.data.resultStatus === 'SUCCESS') {
          message.success(res.data.message);
          navigate(`/event?event_id=${eventid}`);
        } else {
          message.error(res.data.message);
        }
      });
  };

  return (
    <div>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <Form
            name='buyticket'
            {...formItemLayoutWithOutLabel}
            onFinish={onFinish}
            onValuesChange={onvalueChange}
            style={{ margin: 20 }}
          >
            <Form.Item>
              <h1>Buy tickets</h1>
            </Form.Item>
            <Form.List
              name='tickets'
              rules={[
                {
                  validator: async (_, tickets) => {
                    if (!tickets || tickets.length < 1) {
                      return Promise.reject(new Error('At least 1 ticket'));
                    }
                  },
                },
              ]}
            >
              {(fields, { add, remove }, { errors }) => (
                <>
                  {fields.map((field, index) => (
                    <Form.Item
                      {...(index === 0
                        ? formItemLayout
                        : formItemLayoutWithOutLabel)}
                      label={index === 0 ? 'Ticket' : ''}
                      required={false}
                      key={field.key}
                    >
                      <Space>
                        <Form.Item {...field} noStyle>
                          <Cascader
                            style={{
                              maxWidth: '600px',
                              minWidth: '200px',
                            }}
                            expandTrigger='hover'
                            options={options}
                            showSearch={{
                              filter,
                            }}
                          />
                        </Form.Item>
                        {fields.length > 1 ? (
                          <MinusCircleOutlined
                            className='dynamic-delete-button'
                            onClick={() => remove(field.name)}
                          />
                        ) : null}
                      </Space>
                    </Form.Item>
                  ))}
                  <Form.Item>
                    <Button
                      type='dashed'
                      onClick={() => add()}
                      style={{
                        maxwidth: '600px',
                        minWidth: '200px',
                      }}
                      icon={<PlusOutlined />}
                    >
                      Add ticket
                    </Button>
                    <Form.ErrorList errors={errors} />
                  </Form.Item>
                </>
              )}
            </Form.List>
            <Form.Item>Total price:{total}</Form.Item>
            <Form.Item
              name={'card_number'}
              label={'Card Number:'}
              rules={[
                { required: true, message: 'Please input your card number!' },
                {
                  pattern: '[0-9]{16}',
                  message: 'Invalid card number!',
                },
              ]}
              {...formItemLayout}
            >
              <Input
                style={{
                  maxWidth: '200px',
                  minWidth: '50px',
                }}
                maxLength={16}
              />
            </Form.Item>
            <Form.Item>
              <Button type='primary' htmlType='submit'>
                Confirm
              </Button>
            </Form.Item>
          </Form>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </div>
  );
}
