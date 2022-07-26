import React, { useState } from "react";
import { Comment, List, Tooltip, Rate, Input, Form, Button, Modal, Avatar } from 'antd';
import moment from 'moment';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import WriteReview from "./write_review";

const { TextArea } = Input;
const { confirm } = Modal;

const showDeleteConfirm = () => {
  confirm({
    title: 'Are you sure delete this reply?',
    icon: <ExclamationCircleOutlined />,
    okText: 'Yes',
    okType: 'danger',
    cancelText: 'No',

    onOk() {
      // TODO: send data to backend when backend completed
      console.log("Trying to delete...")
    },

    onCancel() {
      return;
    },
  });
};

const ReplyTextArea = ({onChange, onSubmit, onClose, value}) => 
  (
    <>
      <Form.Item>
        <TextArea 
          rows={4} onChange={onChange} value={value}
        />
      </Form.Item>
      <Form.Item>
        <Button size="small" type="primary" onClick={onSubmit} style={{margin:"0 5px"}}>Reply</Button>
        <Button size="small" onClick={onClose} style={{margin:"0 5px"}}>Cancel</Button>
      </Form.Item>
    </>
  )


const ReplyButton = () => {
  const [commentArea, setCommentArea] = useState(false);
  const [value, setValue] = useState('');

  const openCommentArea = () => {
    setCommentArea(true);
  }
  
  const closeCommentArea = () => {
    setCommentArea(false);
  }

  const sendComment = () => {
    // TODO: send data to backend when backend is finished!
    console.log(value);
  }

  const onContentChange = (e) => {
    setValue(e.target.value);
  }

  return (
    <>
      {commentArea?
        <>
        <Comment avatar={<Avatar src="https://joeschmoe.io/api/v1/random" alt="Han Solo" />}
          content={
            <ReplyTextArea
              onChange={onContentChange}
              onSubmit={sendComment}
              onClose={closeCommentArea}
              value={value}
            />
          }
        />
        </>
      :
        <>
          <span key="comment-list-reply-to-0" onClick={openCommentArea}>Reply to</span>
        </>
      }
    </>
  )
}

const DeleteReplyButton = () => {
  const deleteAction = () => {
    showDeleteConfirm()
  }
  return (
    <span key="comment-list-reply-to-0" onClick={deleteAction}>Delete Reply</span>
  )
}

export default function ReviewList (props) {
  // MOCK DATA!
  // Remember to replace with real data when backend is completed

  const data = [
    {
      author: 'Mock Customer 1',
      avatar: 'https://joeschmoe.io/api/v1/random',
      content: (
        <p>
          Very nice event! Looking forward for next time!
        </p>
      ),
      rating: 4.5,
      replied: true,
      reply_content: (
        <p>
          Thanks!
        </p>
      )
    },
    {
      author: 'Mock Customer 2',
      avatar: 'https://joeschmoe.io/api/v1/random',
      content: (
        <p>
          Excellent!
        </p>
      ),
      rating: 5.0
    }
  ];

  return (
    <>
    <WriteReview />
    <List
      className="comment-list"
      header={`${data.length} Reviews`}
      itemLayout="horizontal"
      dataSource={data}
      renderItem={(item) => (
        <li>
          <Comment
            actions={props.isEventHost? (item.replied? null : [<ReplyButton />]) : null}
            author={item.author}
            avatar={item.avatar}
            content={
              <div>
                <Rate disabled allowHalf defaultValue={item.rating}/>
                <br />
                {item.content}
              </div>
            }
          >
            {
              item.replied ? 
              <Comment 
                actions={props.isEventHost? [<DeleteReplyButton />] : null}
                author="Mock Host"
                avatar={item.avatar}
                content={item.reply_content}
              ></Comment>
              :
              null
            }
          </Comment>
        </li>
      )}
  />
  </>
  )
}