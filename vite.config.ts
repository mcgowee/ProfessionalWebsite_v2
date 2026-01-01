import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			// Proxy /socket.io for WebSocket connections
			'/socket.io': {
				target: 'http://127.0.0.1:5000',
				changeOrigin: true,
				ws: true
			},
			// Proxy /api requests to Flask, BUT exclude /api/wordle (handled by SvelteKit)
			'^/api/(?!wordle)': {
				target: 'http://127.0.0.1:5000',
				changeOrigin: true
			}
		}
	}
});
