import { Input, message, Modal, Button } from 'antd';
import React from 'react';
import axios from 'axios';

const { TextArea } = Input;
const { confirm } = Modal;

var word = "";

const onChange = (e) => {
  word = e.target.value;  
  //console.log('Change:', e.target.value);
};

const InputModal = () => {
  const params = new URLSearchParams(window.location.search);

    confirm({
      title: 'Broadcast to users',
      content: <TextArea showCount onChange={onChange}/>,
      okText: 'Submit',

      onOk() {
        console.log("send msg to back end:\neventId: " + params.get("event_id") + "; msg: " + word);
        axios.post(
          'http://127.0.0.1:5000/broadcast',
          { eventId: params.get("event_id"), 
            msg : word }
        )
        .then((response) => {
          console.log(response.data);
          if (response.data.status != 'Error') {
            message.success("Broadcast sent.")
          } else {
            message.error("Email sending failed from server...")   
          }
        })
        .catch((error) => {
          console.log(error);
          message.error("Broadcast failed.")
        })
      },

      onCancel() {},
    });
  };

const BroadCast = () => (
  <Button onClick={InputModal}>Send Message</Button>
);

export default BroadCast;