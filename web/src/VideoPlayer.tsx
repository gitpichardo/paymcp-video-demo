import React from 'react';
import { createRoot } from 'react-dom/client';

interface VideoPlayerProps {
  videoUrl: string;
  prompt: string;
}

function VideoPlayer() {
  // Read data from window.openai (injected by ChatGPT)
  const toolOutput = (window as any).openai?.toolOutput;
  
  if (!toolOutput || !toolOutput.video_url) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>No video data available</p>
      </div>
    );
  }

  const { video_url, prompt } = toolOutput;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '16px',
      padding: '20px',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div>
        <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: 600 }}>
          ✅ Video Generated Successfully
        </h3>
        <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
          📹 {prompt}
        </p>
      </div>
      
      <video
        controls
        autoPlay
        loop
        style={{
          width: '100%',
          maxHeight: '400px',
          borderRadius: '8px',
          backgroundColor: '#000'
        }}
        src={video_url}
      >
        Your browser doesn't support video playback.
      </video>
      
      <div style={{ fontSize: '12px', color: '#888' }}>
        <p style={{ margin: '4px 0' }}>
          💾 <a href={video_url} download style={{ color: '#0066cc' }}>
            Download video
          </a>
        </p>
        <p style={{ margin: '4px 0' }}>
          ⏰ Link valid for 24 hours
        </p>
      </div>
    </div>
  );
}

// Mount the component
const root = document.getElementById('video-player-root');
if (root) {
  createRoot(root).render(<VideoPlayer />);
}

