import React, { useEffect, useState } from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined } from '@ant-design/icons';
import { Layout, List, Space, Avatar, Radio } from 'antd';
import { Link } from 'react-router-dom'
import PageHeader from '../components/page_header';
import axios from 'axios'

const { Content, Footer } = Layout;

export default function LandingPage () {

  // hook
  const [eventList, setEventList] = useState();

  const onFilterButtonChange = (e) => {
    console.log(e.target.value);
  }

  const FilterButtonGroup = () => {
    // check login status
    if (localStorage.getItem("token")){
      return (
        <Radio.Group size="large" defaultValue="" buttonStyle='solid' onChange={onFilterButtonChange}>
          <Radio.Button value="">All</Radio.Button>
          <Radio.Button value="festival">Festival</Radio.Button>
          <Radio.Button value="party">Party</Radio.Button>
          <Radio.Button value="music">Music</Radio.Button>
          <Radio.Button value="sport">Sport</Radio.Button>
          <Radio.Button value="film">Film</Radio.Button>
          <Radio.Button value="foodndrink">Food & Drink</Radio.Button>
          <Radio.Button value="business">Business</Radio.Button>
          <Radio.Button value="funeral">Funeral</Radio.Button>
          <Radio.Button value="others">Others</Radio.Button>
          <Radio.Button value="follower">Only from my follower</Radio.Button>
        </Radio.Group>
      )
    }
    else {
      return (
        <Radio.Group size="large" defaultValue="" buttonStyle='solid' onChange={onFilterButtonChange}>
          <Radio.Button value="">All</Radio.Button>
          <Radio.Button value="festival">Festival</Radio.Button>
          <Radio.Button value="party">Party</Radio.Button>
          <Radio.Button value="music">Music</Radio.Button>
          <Radio.Button value="sport">Sport</Radio.Button>
          <Radio.Button value="film">Film</Radio.Button>
          <Radio.Button value="foodndrink">Food & Drink</Radio.Button>
          <Radio.Button value="business">Business</Radio.Button>
          <Radio.Button value="funeral">Funeral</Radio.Button>
          <Radio.Button value="others">Others</Radio.Button>
        </Radio.Group>
      )
    }
  }

  useEffect(()=>{
    axios.get('http://127.0.0.1:5000/events', {
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then(response => response.data)
      .then(data => {
        //console.log(JSON.stringify(data));
        if(data.resultStatus === 'SUCCESS'){
          //console.log("succeed");
          //console.log(data.message);
          setEventList(data.message);
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
    <div>
      <Layout>
        <PageHeader/>
        <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
          <div className='filter-area' style={{marginTop:'5px'}}>
            <div style={{
              fontSize:'300%', 
              fontWeight:'bold',
              fontFamily:'Arial, Helvetica, sans-serif'
            }}>Ready for your next event ride?</div>
          </div>
          <h1>Please select to filter the type of events you want to see: </h1>
          <FilterButtonGroup />
          <List
          itemLayout="vertical"
          size="large"
          dataSource={eventList}
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
    </div>
  )
}