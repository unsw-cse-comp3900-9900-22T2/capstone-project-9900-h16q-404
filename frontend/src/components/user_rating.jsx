import React, { useState, useEffect, Tooltip } from 'react';
import { Collapse, Rate } from 'antd';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';

const { Panel } = Collapse;

export default function UserRating() {
  const [searchParams] = useSearchParams();
  const [overallRate, setOverallRate] = useState(-1.0);
  const [business, setBusiness] = useState(-1.0);
  const [party, setParty] = useState(-1.0);
  const [music, setMusic] = useState(-1.0);
  const [sport, setSport] = useState(-1.0);
  const [foodndrink, setFoodNDrink] = useState(-1.0);
  const [film, setFilm] = useState(-1.0);
  const [festival, setFestival] = useState(-1.0);
  const [funeral, setFuneral] = useState(-1.0);
  const [holiday, setHoliday] = useState(-1.0);
  const [other, setOther] = useState(-1.0);

  useEffect(() => {
    const userId = searchParams.get('userId');
    const URL = 'http://127.0.0.1:5000/userratings?userId=' + userId;
    axios
      .get(URL)
      .then((response) => response.data)
      .then((data) => {
        if (data.resultStatus === 'SUCCESS') {
          setOverallRate(data.message['Overall Rating']);
        }
        const categorised = data.message['Event Type Rating'];
        if ('Business' in categorised) {
          setBusiness(categorised['Business']);
        }
        if ('Party' in categorised) {
          setParty(categorised['Party']);
        }
        if ('Music' in categorised) {
          setMusic(categorised['Music']);
        }
        if ('Sport' in categorised) {
          setSport(categorised['Sport']);
        }
        if ('Food & Drink' in categorised) {
          setFoodNDrink(categorised['Food & Drink']);
        }
        if ('Film' in categorised) {
          setFilm(categorised['Film']);
        }
        if ('Festival' in categorised) {
          setFestival(categorised['Festival']);
        }
        if ('Funeral' in categorised) {
          setFuneral(categorised['Funeral']);
        }
        if ('Holiday' in categorised) {
          setHoliday(categorised['Holiday']);
        }
        if ('Other' in categorised) {
          setOther(categorised['Other']);
        }
      });
  }, [searchParams]);

  const OverallStars = () => (
    <>
      {overallRate >= 0 ? (
        <div>
          Overall Average Rating for all past Events:
          <Rate disabled allowHalf defaultValue={overallRate} />
        </div>
      ) : (
        <div>
          There are not enough events to show overall rating for past events.
        </div>
      )}
    </>
  );

  const CategorisedStars = () => (
    <>
      {business >= 0 ? (
        <div>
          Average Rating for past Business Event:
          <Rate disabled allowHalf defaultValue={business} />
        </div>
      ) : (
        <></>
      )}
      {party >= 0 ? (
        <div>
          Average Rating for past Party Events:
          <Rate disabled allowHalf defaultValue={party} />
        </div>
      ) : (
        <></>
      )}
      {music >= 0 ? (
        <div>
          Average Rating for past Music Events:
          <Rate disabled allowHalf defaultValue={music} />
        </div>
      ) : (
        <></>
      )}
      {sport >= 0 ? (
        <div>
          Average Rating for past Sport Events:
          <Rate disabled allowHalf defaultValue={sport} />
        </div>
      ) : (
        <></>
      )}
      {foodndrink >= 0 ? (
        <div>
          Average Rating for past Food & Drink Events:
          <Rate disabled allowHalf defaultValue={foodndrink} />
        </div>
      ) : (
        <></>
      )}
      {film >= 0 ? (
        <div>
          Average Rating for past Film Events:
          <Rate disabled allowHalf defaultValue={film} />
        </div>
      ) : (
        <></>
      )}
      {festival >= 0 ? (
        <div>
          Average Rating for past Festival Events:
          <Rate disabled allowHalf defaultValue={festival} />
        </div>
      ) : (
        <></>
      )}
      {sport >= 0 ? (
        <div>
          Average Rating for past Sport Events:
          <Rate disabled allowHalf defaultValue={sport} />
        </div>
      ) : (
        <></>
      )}
      {funeral >= 0 ? (
        <div>
          Average Rating for past Funeral Events:
          <Rate disabled allowHalf defaultValue={funeral} />
        </div>
      ) : (
        <></>
      )}
      {holiday >= 0 ? (
        <div>
          Average Rating for past Holiday Events:
          <Rate disabled allowHalf defaultValue={holiday} />
        </div>
      ) : (
        <></>
      )}
      {other >= 0 ? (
        <div>
          Average Rating for past Other Events:
          <Rate disabled allowHalf defaultValue={other} />
        </div>
      ) : (
        <></>
      )}
    </>
  );

  return (
    <>
      <Collapse>
        <Panel header={<OverallStars />} showArrow={false}>
          <CategorisedStars />
        </Panel>
      </Collapse>
    </>
  );
}
