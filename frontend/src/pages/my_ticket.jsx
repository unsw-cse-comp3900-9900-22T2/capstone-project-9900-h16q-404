import React, { useState, useEffect } from 'react';
import { Layout, List, Descriptions, Card, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/page_header';
import axios from 'axios';
import {
  ExclamationCircleOutlined,
  MoreOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import { Modal } from 'antd';
import DescriptionsItem from 'antd/lib/descriptions/Item';

const { Content, Footer } = Layout;
const { confirm } = Modal;

export default function MyTicket() {
  let navigate = useNavigate();

  // hook
  const [ticketsList, setTicketsList] = useState();

  useEffect(() => {
    axios
      .get('http://127.0.0.1:5000/mytickets', {
        headers: {
          'Content-Type': 'application/json',
          token: localStorage.getItem('token'),
        },
      })
      .then((response) => response.data)
      .then((data) => {
        if (data.resultStatus === 'SUCCESS') {
          setTicketsList(data.result.result);
        }
      });
  }, []);

  let today = new Date();
  let sevenDaysBefore = new Date();
  sevenDaysBefore.setDate(today.getDate() + 7);

  const refundConfirm = (item) => {
    confirm({
      title: 'Warning',
      icon: <ExclamationCircleOutlined />,
      content: 'Are you sure you want to refund?',
      onOk() {
        let eventStartDate = new Date(item.start_date);
        if (eventStartDate.getTime() > sevenDaysBefore.getTime()) {
          // axios
          axios
            .put('http://127.0.0.1:5000/buytickets', {
              token: localStorage.getItem('token'),
              tickets: [
                {
                  event_id: item.event_id,
                  seat_num: item.seat_num,
                  tix_class: item.tix_class,
                },
              ],
            })
            .then((response) => response.data)
            .then((data) => {
              console.log(JSON.stringify(data));
              if (data.resultStatus === 'SUCCESS') {
                //console.log("Refund succeed");
                message.info('Refund seccessed.');
                window.location.reload();
              }
            });
        } else {
          //console.log("cannot refund because it is a past event or less than 7 days.")
          message.warning(
            'cannot refund because it is a past event or less than 7 days.'
          );
        }
      },

      onCancel() {},
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
          <h1>Your tickets are shown below:</h1>
          <List
            grid={{
              gutter: 16,
              column: 4,
            }}
            dataSource={ticketsList}
            renderItem={(item) =>
              item.purchased ? (
                <List.Item>
                  <Card
                    title={item.event_name}
                    style={{ width: 230 }}
                    hoverable
                    actions={[
                      <DeleteOutlined
                        title='Refund your ticket'
                        onClick={refundConfirm.bind(this, item)}
                      ></DeleteOutlined>,
                      <MoreOutlined
                        title='Go to this event'
                        onClick={() => {
                          navigate('/event?event_id=' + item.event_id);
                        }}
                      ></MoreOutlined>,
                    ]}
                  >
                    <Descriptions column={1}>
                      <DescriptionsItem label='Ticket ID'>
                        {' '}
                        {item.id}
                      </DescriptionsItem>
                      <DescriptionsItem label='Seat Class'>
                        {' '}
                        {item.tix_class}
                      </DescriptionsItem>
                      <DescriptionsItem label='Seat Num'>
                        {' '}
                        {item.seat_num}
                      </DescriptionsItem>
                      <DescriptionsItem label='Start From'>
                        {' '}
                        {item.start_date + '\n' + item.start_time}
                      </DescriptionsItem>
                      <DescriptionsItem label='Price'>
                        {' '}
                        {'$' + item.ticket_price}
                      </DescriptionsItem>
                    </Descriptions>
                  </Card>
                </List.Item>
              ) : null
            }
          ></List>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </div>
  );
}
