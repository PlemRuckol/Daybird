import { useEffect, useState } from 'react';
import './App.css';

type ChatItem = {
  content: string;
  direction: 'L' | 'R';
};

function Chat() {
  const [time, setTime] = useState('');
  const [date, setDate] = useState('');
  const [chatData, setChatData] = useState<ChatItem[]>([]);

  // 시간 / 날짜 설정
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      setTime(`${hours}:${minutes}`);

      const dayNames = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];
      const month = now.getMonth() + 1;
      const day = now.getDate();
      const weekday = dayNames[now.getDay()];
      setDate(`${month}월 ${day}일 ${weekday}`);
    };

    updateTime();
    const timeInterval = setInterval(updateTime, 1000);
    return () => clearInterval(timeInterval);
  }, []);

  // 1초마다 JSON 데이터를 동기화
  useEffect(() => {
    const interval = setInterval(() => {
      fetch('./data/data.json')
        .then((res) => res.json())
        .then((data) => {
          setChatData(data); // 최신 상태로 반영
        })
        .catch((err) => console.error('❌ JSON fetch error:', err));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className='chat-viewport'>
      <div className='chat-day-time'>
        <div className='chat-time'>{time}</div>
        <div className='chat-day'>{date}</div>
      </div>
      <div className='chat-container scroll-hidden'>
        {chatData.map((item, i) => (
          <div
            key={i}
            className={item.direction === 'L' ? 'chat-item-left' : 'chat-item-right'}
          >
            {item.content}
          </div>
        ))}
      </div>
      <div className='chat-footer'>3분 이상 대화가 없으면 대기 화면으로 전환됩니다.</div>
    </div>
  );
}

export default Chat;
