/*TODO:
	DONE--Step1: finish a static page containing all elements
	Step2: make the elements show/hide depend on host id and make query url, send delete msg to backend
	Step3: add link to event card
*/
import React, { useState, useEffect } from 'react';
import { Layout, Descriptions, Rate, Collapse, Modal } from 'antd';
import PageHeader from '../components/page_header';
import { Col, Row, Statistic, Button, Divider } from 'antd';
import axios from 'axios'
import { useSearchParams, Link } from "react-router-dom";
import { UserOutlined } from '@ant-design/icons';

// Content and Footer 
const { Content, Footer } = Layout;

// Component of rating stars
const Rating = () => <Rate allowHalf defaultValue={2.5}/>;

// Component of button buying tickets and remaing statistics
const TicketBar = () => (
  <Row gutter={16}>
    <Col span={12}>
      <Button style={{ marginTop: 16 }} type="primary">
        Buy A Ticket
      </Button>
    </Col>
    <Col span={12}>
      <Statistic title="Unmerged" value={93} suffix="/ 100" />
    </Col>
  </Row>
);

// To save eventId into localstorage, print states in console log.
function saveEventId(){ 
	console.log("Getting page URL...");
	let url = new URL(window.location.href);
	console.log("append eventId to localstorage...");
	localStorage.setItem("eventId", url.searchParams.get("event_id"));
	console.log("eventId: " + 
							localStorage.getItem("eventId") +
							" has been saved.");
}

// To call an alert and redirect to landing page if needed 
function deleteCheck(){
	alert("Are you sure you want to delete the event?")
}

const DeleteButton = () => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <>
      <Button type="primary" onClick={showModal}>
        DELETE EVENT
      </Button>
      <Modal title="Basic Modal" visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
        <p>Are you sure you want to delete the event?</p>
      </Modal>
    </>
  );
};

// To return event page
export default function EventPage () {

	const [searchParams] = useSearchParams();
  const [isSelfProfle, setSelfProfile] = useState(false);
  const [followed, setFollow] = useState(false);
  const [eventInfo, setEventInfo] = useState({});

	saveEventId();
	useEffect(() => {

	const requestURL = 'http://127.0.0.1:5000/event?event_id=' + localStorage.getItem("eventId")
	axios.get(requestURL)
		.then(res => res.data.message)
		.then(data => {
			console.log(data);
			setEventInfo(data[0]);
			console.log(eventInfo.event_name);
			console.log(eventInfo);
		});
	},[searchParams]);
	
	let time = eventInfo.start_date + " " + eventInfo.start_time + " to " + 
						eventInfo.end_date + " " + eventInfo.end_time;

	// Component of event Description
	const EventInfoBlock = () => (
		<Descriptions title="Event Info">
			<Descriptions.Item label="Event Name">{eventInfo.event_name}</Descriptions.Item>
			<Descriptions.Item label="Type">{eventInfo.type}</Descriptions.Item>
			<Descriptions.Item label="Host">
				<Button type="link">{eventInfo.host}</Button>
			</Descriptions.Item>
			<Descriptions.Item label="Rating"><Rating/></Descriptions.Item>
			<Descriptions.Item label="Time">{time}</Descriptions.Item>
		</Descriptions>
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
			console.log(key);
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

	return (
		<div>
			<Layout>
				<PageHeader/>
				<Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
					

					<EventInfoBlock/>

					<Divider />

					<SpecialConsiderationBar/>

					<Divider />

					<TicketBar/>

					<Divider />

					<p>
						{eventInfo.description}
					</p>

					{ eventInfo.host == 2 ? <>
					<Button>Send Message</Button>
					<Button>Edit Event</Button>
					<DeleteButton/>
 					</> : null}

					<Footer style={{textAlign:'center'}}>
        		9900-H16Q-404
        	</Footer>
				
				</Content>
			</Layout>
		</div>
	)
}