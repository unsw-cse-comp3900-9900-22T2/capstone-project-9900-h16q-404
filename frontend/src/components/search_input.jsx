import React from 'react';
import { Input, Space } from 'antd';

const { Search } = Input;

// to be changed when search function is ready to develop
const onSearch = (value) => {
  const keyWordList = value.split(" ");
  const keyWordDict = {
    keyWordList: keyWordList.map(word => {
      return word.toLowerCase();
    })
  }
  // when backend ready, change this to axios function
  console.log(JSON.stringify(keyWordDict));
}

export default function SearchInput () {
  return(
  <Space direction='vertical'>
    <Search placeholder="input search text" onSearch={onSearch} enterButton />
  </Space>
  )
}