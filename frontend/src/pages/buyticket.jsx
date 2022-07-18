import React, { useEffect, useState } from 'react';
import { Layout, Select, Button, Form, Input, Space, Cascader } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import PageHeader from '../components/page_header';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';
const { Option } = Select;
const { Content } = Layout;

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
  const dict = { gold: [1, 2, 3, 5, 6, 10], silver: [1, 3, 5, 7], bronze: [0] };

  const onFinish = (values) => {
    console.log(values);
    const stringlist = [];
    const tickets = [];
    for (const value of values.tickets) {
      if (value !== undefined) {
        if (!stringlist.includes(value.join())) {
          stringlist.push(value.join());
          tickets.push({
            event_id: eventid,
            seat_num: value[1],
            tix_class: value[0],
          });
        }
      }
    }
    console.log(tickets);
  };
  const [options, setOptions] = useState();

  const filter = (inputValue, path) => {
    path.some(
      (option) =>
        option.label.toLowerCase().indexOf(inputValue.toLowerCase()) > -1
    );
  };

  useEffect(() => {
    const newoptions = [];
    for (const [key, value] of Object.entries(dict)) {
      if (!value.includes(0)) {
        console.log(value);
        const option = {
          value: key,
          label: key.toString(),
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
  }, [setOptions]);
  return (
    <div>
      <h3>Hallo\</h3>
      <Form name='buyticket' onFinish={onFinish}>
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
                  <Form.Item {...field} noStyle>
                    <Cascader
                      style={{
                        width: '40%',
                      }}
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
                </Form.Item>
              ))}
              <Form.Item>
                <Button
                  type='dashed'
                  onClick={() => add()}
                  style={{
                    width: '60%',
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
        <Form.Item>
          <Button type='primary' htmlType='submit'>
            Submit
          </Button>
        </Form.Item>
      </Form>

      <Cascader
        options={options}
        showSearch={{
          filter,
        }}
        onChange={(value, selectedOptions) => {
          console.log(value);
        }}
      />
    </div>
  );
}
