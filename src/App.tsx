import { Routes, Route } from 'react-router-dom';
import AppMain from './AppMain'; // 기존 App.tsx 내용을 옮긴 컴포넌트
import Chat from './Chat';

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppMain />} />
      <Route path="/chat" element={<Chat />} />
    </Routes>
  );
}

export default App;
