/*TODO:
	DONE--Step1: finish a static page containing all elements
	Step2: make the elements show/hide depend on host id and make query url, send delete msg to backend
	Step3: add link to event card
*/
import React, { useState, useEffect } from 'react';
import { Layout, Descriptions, Rate, Collapse, Modal } from 'antd';
import PageHeader from '../components/page_header';
import { Col, Row, Statistic, Button, Divider, message } from 'antd';
import axios from 'axios'
import { useSearchParams, Link, useNavigate } from "react-router-dom";
import { ExclamationCircleOutlined } from '@ant-design/icons';

const { confirm } = Modal;

// Content and Footer 
const { Content, Footer } = Layout;

// Component of rating stars
const Rating = () => <Rate allowHalf defaultValue={2.5}/>;

// To return event page
export default function EventPage () {

	const [searchParams] = useSearchParams();
  const [eventInfo, setEventInfo] = useState({});
  const [usrInfo, setUsrInfo] = useState({});

	useEffect(() => {
		var requestURL = 
				'http://127.0.0.1:5000/event?event_id=' + searchParams.get("event_id");
		console.log("Sending request with event_id=" + searchParams.get("event_id"));
		axios.get(requestURL)
			.then(res => res.data.event_details)
			.then(data => {
				console.log(data);
				setEventInfo(data[0]);
				console.log("get event: " + eventInfo.event_name);
				console.log(eventInfo);
			})
			.catch(error => {
				console.log(error);
				message.error("This event does not exist...", 5);
				//navigate('/');
			});
			
		if(localStorage.getItem('userId') != null)
		{requestURL =
			'http://127.0.0.1:5000/user?userId=' + localStorage.getItem('userId');
		axios
			.get(requestURL, {
				headers: {
					'Content-Type': 'application/json',
				},
			})
			.then((res) => res.data.message)
			.then((data) => {
				console.log("getting user info...")
				console.log(data);
				setUsrInfo(data);
			})
			.catch((error) => {
				console.log(error);
			});}
		}, [searchParams]);

	let navigate = useNavigate();

	const deleteConfirm = () => {
		confirm({
			title: 'Warning',
			icon: <ExclamationCircleOutlined />,
			content: 'Are you sure you want to delete this event?',

			onOk() {
				axios.delete('http://127.0.0.1:5000/event?event_id=' + searchParams.get("event_id"))
    			.then(() => {
						console.log("successfully delete this event.");
						message.success("This event has been deleted.",2)
            navigate('/');
					})
					.catch(() =>{
						message.error("Something goes wrong.",5);
					});
				},

			onCancel() {},
		});
	};
	
	let time = eventInfo.start_date + " " + eventInfo.start_time + " to " + 
						eventInfo.end_date + " " + eventInfo.end_time;

	// Component of event Description
	const EventInfoBlock = () => (
		<Descriptions title="Event Info">
			<Descriptions.Item label="Event Name">{eventInfo.event_name}</Descriptions.Item>
			<Descriptions.Item label="Type">{eventInfo.type}</Descriptions.Item>
			<Descriptions.Item label="Host">
				<Button 
				type="link"
				href={"user?userId=" + eventInfo.host}>{eventInfo.host_username}</Button>
			</Descriptions.Item>
			<Descriptions.Item label="location">{eventInfo.location}</Descriptions.Item>
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

	// Component of button buying tickets and remaing statistics
	const TicketBar = () => (
		<Row gutter={16}>
			<Col span={12}>
				<Button 
				style={{ marginTop: 16 }} 
				type="primary"
				disabled={
					usrInfo.vac == null 
				}>
					Buy A Ticket
				</Button>
			</Col>
			<Col span={12}>
				<Statistic title="Unmerged" value={93} suffix="/ 100" />
			</Col>
		</Row>
	);

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

					{ eventInfo.host == localStorage.getItem("userId") ? <>
					<Button>Send Message</Button>
					<Button href={'/editevent/'+ searchParams.get("event_id")}>Edit Event</Button>
					<Button onClick={deleteConfirm}>
						Delete
					</Button>
 					</> : null}
				</Content>
				<Footer style={{textAlign:'center'}}>
          9900-H16Q-404
        </Footer>
			</Layout>
		</div>
	)
}