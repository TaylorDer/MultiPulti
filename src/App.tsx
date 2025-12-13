import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import TOC from './pages/TOC';
import Chapter from './pages/Chapter';
import Playground from './pages/Playground';
import Glossary from './pages/Glossary';
import About from './pages/About';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="toc" element={<TOC />} />
        <Route path="chapter/:chapterId/section/:sectionId" element={<Chapter />} />
        <Route path="playground" element={<Playground />} />
        <Route path="glossary" element={<Glossary />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}

export default App;

