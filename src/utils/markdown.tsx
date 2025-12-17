import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';
import rehypeHighlight from 'rehype-highlight';

interface MarkdownContentProps {
  content: string;
}

export const MarkdownContent: React.FC<MarkdownContentProps> = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkMath, remarkGfm]}
      rehypePlugins={[rehypeKatex, rehypeHighlight]}
      components={{
        img: ({ node, ...props }) => (
          <img
            {...props}
            style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px', margin: '1rem auto', display: 'block', cursor: 'pointer' }}
            onClick={() => {
              // Open image in modal (will be handled by parent)
              const event = new CustomEvent('imageClick', { detail: { src: props.src, alt: props.alt } });
              window.dispatchEvent(event);
            }}
          />
        ),
        code: ({ className, children, ...props }: any) => {
          return (
            <code className={className} {...props}>
              {children}
            </code>
          );
        },
        table: ({ children, ...props }: any) => (
          <div style={{ overflowX: 'auto', margin: '1rem 0' }}>
            <table style={{ borderCollapse: 'collapse', width: '100%', border: '1px solid #ddd' }} {...props}>
              {children}
            </table>
          </div>
        ),
        th: ({ children, ...props }: any) => (
          <th style={{ border: '1px solid #ddd', padding: '8px', backgroundColor: '#f2f2f2', textAlign: 'left' }} {...props}>
            {children}
          </th>
        ),
        td: ({ children, ...props }: any) => (
          <td style={{ border: '1px solid #ddd', padding: '8px' }} {...props}>
            {children}
          </td>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

