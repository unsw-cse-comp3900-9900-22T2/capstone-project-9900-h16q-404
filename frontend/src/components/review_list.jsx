import React, { useState } from "react";
import { Comment, List, Tooltip, Rate, Input, Form, Button, Modal, Avatar, Divider } from 'antd';
import moment from 'moment';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import WriteReview from "./write_review";
import axios from 'axios';
import { useEffect } from "react";

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

  const [reviewList, setReviewList] = useState({});

  useEffect(()=>{
    const requestURL = "http://127.0.0.1:5000/reviews?token="
      +localStorage.getItem("token")
      +"&eventId="+props.eventId;
    axios.get(requestURL)
      .then(response => response.data.message)
      .then(data => {
        setReviewList(data)
      })
  },[props])

  const WriteReviewSection = () => {
    if (!reviewList.has_ticket){
      return(
        <h2>Sorry you can't post a review on this event, since you have not attended it.</h2>
      )
    }
    else {
      if( !reviewList.has_commeent){
        return(
          <h2>You have already left your comment.</h2>
        )
      }
      else {
        return(
          <WriteReview />
        )
      }
    }
  }


  return (
    <>
    <Divider />
    <WriteReviewSection />
    <Divider />
    <h2>Review List</h2>
    <List
      className="comment-list"
      itemLayout="horizontal"
      dataSource={reviewList.reviews}
      renderItem={(item) => (
        <li>
          <Comment
            actions={reviewList.isHost? (item.reply? null : [<ReplyButton />]) : null}
            author={item.reviewedBy}
            avatar='https://joeschmoe.io/api/v1/random'
            content={
              <div>
                <Rate disabled allowHalf defaultValue={item.rating}/>
                <br />
                {item.review}
              </div>
            }
            datetime={
              <Tooltip title={moment(item.reviewedOn).format('YYYY-MM-DD HH:mm:ss')}>
                <span>{moment(item.reviewedOn).fromNow()}</span>
              </Tooltip>
            }
          >
            {
              item.reply ? 
              <Comment 
                actions={props.isEventHost? [<DeleteReplyButton />] : null}
                author={reviewList.hostedBy}
                avatar='https://joeschmoe.io/api/v1/random'
                content={item.reply}
                datetime={
                  <Tooltip title={moment(item.repliedOn).format('YYYY-MM-DD HH:mm:ss')}>
                    <span>{moment(item.repliedOn).fromNow()}</span>
                  </Tooltip>
                }
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