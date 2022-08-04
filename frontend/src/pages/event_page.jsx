import React, { useState, useEffect } from 'react';
import { Layout, Descriptions, Rate, Collapse, Modal } from 'antd';
import PageHeader from '../components/page_header';
import { Col, Row, Button, Divider, message } from 'antd';
import axios from 'axios'
import { useSearchParams, useNavigate } from "react-router-dom";
import { ExclamationCircleOutlined } from '@ant-design/icons';
import BroadCast from '../components/broadcast_button';
import ReviewList from '../components/review_list';
import PastEventBuyTicketMask from '../components/past_event_buy_ticket_mask';
import moment from 'moment';
import FollowButton from '../components/follow_button';

const { confirm } = Modal;

// Content and Footer
const { Content, Footer } = Layout;

// To return event page
export default function EventPage() {
  const [searchParams] = useSearchParams();
  const [eventInfo, setEventInfo] = useState({});
  const [usrInfo, setUsrInfo] = useState({});
  // a switch to distinguish past event and upcoming event
  const [eventFinished, setEventFinished] = useState(false);
  const [rating, setRating] = useState(0.0);

  useEffect(() => {
    var requestURL =
      'http://127.0.0.1:5000/event?event_id=' + searchParams.get('event_id');
    axios
      .get(requestURL)
      .then((res) => res.data.event_details)
      .then((data) => {
        setEventInfo(data[0]);
        // set eventFinished based on event start date
        const today = moment();
        const endDate = moment(data[0].end_date + ' ' + data[0].end_time);
        if (endDate.isBefore(today)) {
          setEventFinished(true);
        } else {
          setEventFinished(false);
        }
        return;
      })
      .catch((error) => {
        message.error('This event does not exist...', 5);
      });

    const getRatingURL =
      'http://127.0.0.1:5000/eventratings?eventId=' +
      searchParams.get('event_id');
    axios
      .get(getRatingURL)
      .then((response) => response.data)
      .then((data) => {
        if (data.resultStatus === 'SUCCESS') {
          let rate = parseFloat(data.message['Average Rating']);
          rate = Math.round(rate * 2) / 2;
          setRating(rate);
        }
      });

    if (localStorage.getItem('userId') != null) {
      requestURL =
        'http://127.0.0.1:5000/user?userId=' + localStorage.getItem('userId');
      axios
        .get(requestURL, {
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then((res) => res.data.message)
        .then((data) => {
          setUsrInfo(data);
        })
        .catch((error) => {});
    }
  }, [searchParams]);

  let navigate = useNavigate();

  const deleteConfirm = () => {
    confirm({
      title: 'Warning',
      icon: <ExclamationCircleOutlined />,
      content: 'Are you sure you want to delete this event?',

      onOk() {
        axios
          .delete(
            'http://127.0.0.1:5000/event?event_id=' +
              searchParams.get('event_id')
          )
          .then(() => {
            // console.log('successfully delete this event.');
            message.success('This event has been deleted.', 2);
            navigate('/');
          })
          .catch(() => {
            message.error('Something goes wrong.', 5);
          });
      },

      onCancel() {},
    });
  };

  let time =
    eventInfo.start_date +
    ' ' +
    eventInfo.start_time +
    ' to ' +
    eventInfo.end_date +
    ' ' +
    eventInfo.end_time;

  function usrIsNotAdult() {
    let date = new Date(usrInfo.dateOfBirth);
    var diff_ms = Date.now() - date.getTime();
    var age_dt = new Date(diff_ms);
    var year = Math.abs(age_dt.getUTCFullYear() - 1970);
    if (year < 18) {
      return true;
    } else {
      return false;
    }
  }

  // Component of event Description
  const EventInfoBlock = () => (
    <>
      <Divider orientation='left'>Event Information</Divider>
      <Descriptions>
        <Descriptions.Item label='Event Name'>
          {eventInfo.event_name}
        </Descriptions.Item>
        <Descriptions.Item label='Type'>{eventInfo.type}</Descriptions.Item>
        <Descriptions.Item label='Host'>
          <Button type='link' href={'user?userId=' + eventInfo.host}>
            {eventInfo.host_username}
          </Button>
          {FollowButton(eventInfo.host)}
        </Descriptions.Item>
        <Descriptions.Item label='location'>
          {eventInfo.location}
        </Descriptions.Item>
        <Descriptions.Item label='Rating'>
          <Rate disabled allowHalf defaultValue={rating} />
        </Descriptions.Item>
        <Descriptions.Item label='Time'>{time}</Descriptions.Item>
      </Descriptions>
    </>
  );

  // Component of special Consideration Collapse
  const { Panel } = Collapse;

  const VacReq = `
		A Vaccination requirement is needed for this
		Event.
	`;

  const AdultReq = `
		This Event required guest to be at least 18
		years old.
	`;

	const SpecialConsiderationBar = () => {
		const onChange = (key) => {

		};

		return (
			<Collapse onChange={onChange}>
				{ eventInfo.vax_only ? <Panel header="Vaccination Required" key="1">
					<p>{VacReq}</p>
				</Panel> : null}
				{ eventInfo.adult_only ? <Panel header="Age 18 Required" key="2">
					<p>{AdultReq}</p>
				</Panel> : null}
			</Collapse>
		);
	};

	// Component of button buying tickets and remaing statistics
	const TicketBar = () => (
		<Row gutter={16}>
			<Col span={12}>
				<Button 
				style={{ marginTop: 16 }} 
				type="primary"
				disabled={
					(usrInfo.vac !== true && eventInfo.vax_only) ||
					(usrIsNotAdult() && eventInfo.adult_only) ||
					(localStorage.getItem("token") === null)
				}
				href={'/buyticket/' + eventInfo.id}>
					Buy A Ticket
				</Button>
			</Col>
		</Row>
	);

	return (
		<div>
			<Layout>
				<PageHeader/>
				<Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>

					<EventInfoBlock/>

					<Divider orientation='left'>Attendance Condition</Divider>

					<SpecialConsiderationBar/>

					<Divider orientation='left' >Event Description</Divider>

					<div>
            <p>{eventInfo.description}</p>
            {eventInfo.image !== 'default' && eventInfo.image !== null ? (
              <p>
                <img
                  src={eventInfo.image}
                  alt={eventInfo.image}
                  style={{ maxWidth: '100%' }}
                />
              </p>
            ) : (
              <></>
            )}
          </div>

					<Divider orientation='left'>Buy Ticket</Divider>

					{eventFinished ? <PastEventBuyTicketMask/> :<TicketBar/>}
					
					{ 
					eventInfo.host === parseInt(localStorage.getItem("userId")) ? 
						<>
							<Divider orientation='left'>Actions</Divider>
							<BroadCast />
							<Button href={'/editevent/'+ searchParams.get("event_id")}>Edit Event</Button>
							<Button onClick={deleteConfirm}>
								Delete
							</Button>
						</> 
					: null
					}

				{
					eventFinished ? <ReviewList eventId={eventInfo.id} isEventHost={(eventInfo.host === parseInt(localStorage.getItem("userId")) ? true : false)} /> : null 
				}
				</Content>
				<Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
			</Layout>
		</div>
	)
}
