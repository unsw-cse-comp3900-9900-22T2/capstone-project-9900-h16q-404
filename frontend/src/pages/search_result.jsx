import React, { useEffect, useState } from 'react';
import { Layout, message, List, Avatar, Space } from 'antd';
import PageHeader from '../components/page_header';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { LikeOutlined, MessageOutlined, StarOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';

const { Content, Footer } = Layout;

export default function SearchResult() {
  const [searchParams] = useSearchParams();
  const [searchResult, setSearchResult] = useState([]);

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );

  useEffect(() => {
    const value = decodeURIComponent(searchParams.get('keyword'));
    const keyWordList = value.split(' ');
    const keyWordDict = {
      keyWordList: keyWordList.map((word) => {
        return word.toLowerCase();
      }),
    };
    //console.log(JSON.stringify(keyWordDict));
    axios
      .post('http://127.0.0.1:5000/event/search', keyWordDict)
      .then((response) => response.data)
      .then((data) => {
        if (data.resultStatus === 'SUCCESS') {
          setSearchResult(data.message);
        } else {
          message.error(data.message);
        }
      });
  }, [searchParams]);
  return (
    <>
      <Layout>
        <PageHeader />
        <Content
          className='site-layout'
          style={{ padding: '0 50px', marginTop: 64 }}
        >
          <div
            style={{
              fontSize: '300%',
              fontWeight: 'bold',
              fontFamily: 'Arial, Helvetica, sans-serif',
            }}
          >
            Results of searching{' '}
            {decodeURIComponent(searchParams.get('keyword'))}:{' '}
          </div>
          <List
            itemLayout='vertical'
            size='large'
            dataSource={searchResult}
            renderItem={(item) => (
              <List.Item
                key={item.id}
                actions={[
                  <IconText
                    icon={StarOutlined}
                    text='114'
                    key='list-vertical-star-o'
                  />,
                  <IconText
                    icon={LikeOutlined}
                    text='514'
                    key='list-vertical-like-o'
                  />,
                  <IconText
                    icon={MessageOutlined}
                    text='1919'
                    key='list-vertical-message'
                  />,
                ]}
                extra={
                  <img
                    width={272}
                    alt='logo'
                    src='https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png'
                  />
                }
              >
                <List.Item.Meta
                  avatar={
                    <Avatar src={'https://joeschmoe.io/api/v1/random'}></Avatar>
                  }
                  title={
                    <Link to={'/event?event_id=' + item.id}>
                      {item.event_name}
                    </Link>
                  }
                  description={
                    <Link to={'/user?userId=' + item.host}>
                      {item.host_username}
                    </Link>
                  }
                />
                {'Event date: ' + item.start_date}
              </List.Item>
            )}
          ></List>
        </Content>
        <Footer style={{ textAlign: 'center' }}>9900-H16Q-404</Footer>
      </Layout>
    </>
  );
}
