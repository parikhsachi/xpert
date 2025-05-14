// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        'nu-purple': '#4e2a84',
        'nu-purple-80': '#684c96',
        'nu-purple-60': '#836eaa',
        'soft-bg': '#f9f9f9',
        'text-muted': '#666666',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        'content': '1280px',
      },
    },
  },
  plugins: [],
}
