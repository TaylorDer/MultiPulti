import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import ImageModal from './ImageModal';
import { storage } from '../utils/storage';
import './Layout.css';

const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [fontSize, setFontSize] = useState(1);
  const [modalImage, setModalImage] = useState<{ src: string; alt: string } | null>(null);

  useEffect(() => {
    const settings = storage.getSettings();
    setFontSize(settings.fontSize);
    document.documentElement.style.fontSize = `${16 * settings.fontSize}px`;
  }, []);

  useEffect(() => {
    const handleImageClick = (e: Event) => {
      const customEvent = e as CustomEvent;
      setModalImage({ src: customEvent.detail.src, alt: customEvent.detail.alt });
    };

    window.addEventListener('imageClick', handleImageClick);
    return () => window.removeEventListener('imageClick', handleImageClick);
  }, []);

  const handleFontSizeChange = (delta: number) => {
    const newSize = Math.max(0.75, Math.min(1.5, fontSize + delta));
    setFontSize(newSize);
    document.documentElement.style.fontSize = `${16 * newSize}px`;
    storage.saveSettings({ ...storage.getSettings(), fontSize: newSize });
  };

  return (
    <div className="layout">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      <div className="layout-body">
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          fontSize={fontSize}
          onFontSizeChange={handleFontSizeChange}
        />
        <main className="layout-content">
          <Outlet />
        </main>
      </div>
      {modalImage && (
        <ImageModal
          src={modalImage.src}
          alt={modalImage.alt}
          onClose={() => setModalImage(null)}
        />
      )}
    </div>
  );
};

export default Layout;

