import { useEffect, useState } from 'react';
import './App.css';

function Chat() {
  const [isBlinking, setIsBlinking] = useState(false);
  const [time, setTime] = useState('');
  const [date, setDate] = useState('');

  // 시간 및 날짜 설정
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

  // 깜빡임 애니메이션
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setIsBlinking(true);
      setTimeout(() => setIsBlinking(false), 100); // 0.1초 후 원상복귀
    }, 5000); // 5초마다 실행

    return () => clearInterval(blinkInterval);
  }, []);

  return (
    <div className='main-viewport'>
      <div className={`daybird-background ${isBlinking ? 'blink' : ''}`} />
      <div className='day-time'>
        <div className='time'>{time}</div>
        <div className='day'>{date}</div>
      </div>
    </div>
  );
}

export default Chat;
