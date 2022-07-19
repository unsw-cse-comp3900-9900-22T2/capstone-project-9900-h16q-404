import React, { useState, useEffect } from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined } from '@ant-design/icons';
import { Layout, List, Avatar, Space} from 'antd';
import { Link } from 'react-router-dom'
import PageHeader from '../components/page_header';
import axios from 'axios'

const { Content, Footer } = Layout;

export default function MyTicket () {
	
  // hook
  const [ticketsList, setTicketsList] = useState();

  useEffect(()=>{
    axios.get('localhost:5000/mytickets', {
      headers: {
        'Content-Type': 'application/json'
      },
			params: {
				token: localStorage.getItem("token")
			}
    })
      .then(response => response.data)
      .then(data => {
        console.log(JSON.stringify(data));
        if(data.resultStatus === 'SUCCESS'){
          console.log("succeed");
          console.log(data.message);
          setTicketsList(data.message);
        }
      })
  }, []);

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );
	
	return (
		<dive>
			<Layout>
				<PageHeader />
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <List
          itemLayout="vertical"
          size="large"
          dataSource={ticketsList}
          renderItem={(item) => (
            <List.Item
              key={item.id}
              actions={[
                <IconText icon={StarOutlined} text="114" key="list-vertical-star-o" />,
                <IconText icon={LikeOutlined} text="514" key="list-vertical-like-o" />,
                <IconText icon={MessageOutlined} text="1919" key="list-vertical-message" />,
              ]}
              extra={
                <img
                  width={272}
                  alt="logo"
                  src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
                />
              }
            >
              <List.Item.Meta
                avatar={<Avatar src={'https://joeschmoe.io/api/v1/random'}></Avatar>}
                title={item.event_name}
                description={<Link to='/user?userId=2'>Mock User with userId = 2 {item.id}</Link>}
              />
              {"Event date: " + item.event_date}
            </List.Item>
            )}
          >
          </List>
        </Content>
        <Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
			</Layout>
		</dive>
	)
}