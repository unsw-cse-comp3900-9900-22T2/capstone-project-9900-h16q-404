import React from 'react';
import { Input, Space } from 'antd';

const { Search } = Input;

// to be changed when search function is ready to develop
const onSearch = (value) => console.log(value);

export default function SearchInput () {
  return(
  <Space direction='vertical'>
    <Search placeholder="input search text" onSearch={onSearch} enterButton />
  </Space>
  )
}