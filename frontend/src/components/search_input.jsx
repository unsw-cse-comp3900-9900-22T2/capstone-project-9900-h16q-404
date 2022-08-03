import React from 'react';
import { Input, Space } from 'antd';
import { useNavigate } from 'react-router-dom';

const { Search } = Input;

export default function SearchInput() {
  const navigate = useNavigate();

  // to be changed when search function is ready to develop
  const onSearch = (value) => {
    const keyWordAsURIComponent =
      '/search?keyword=' + encodeURIComponent(value);
    navigate(keyWordAsURIComponent);
    // plan to move the axios action in search result page.
  };

  return (
    <Space direction='vertical'>
      <Search placeholder='input search text' onSearch={onSearch} enterButton />
    </Space>
  );
}
