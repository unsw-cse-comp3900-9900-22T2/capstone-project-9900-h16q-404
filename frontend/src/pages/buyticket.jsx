import React, { useEffect, useState } from 'react';
import { Select } from 'antd';
const { Option } = Select;

export default function BuyTicket() {
  const list = [1, 2, 3, 5, 6, 10];
  return (
    <div>
      <h3>Hallo\</h3>
      <Select>
        {
          list.map((item) => {
            return(
              <Option key={item.toString()}>
                {item}
              </Option>
            )
          })
        }
      </Select>
    </div>
  );
}
