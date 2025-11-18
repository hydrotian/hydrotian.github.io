<script lang="ts">
	import '../app.css';
	import { base } from '$app/paths';
</script>

<div class="min-h-screen flex flex-col">
	<header class="bg-white shadow-sm">
		<nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
			<div class="flex justify-between items-center">
				<a href="{base}/" class="text-2xl font-light text-gray-900 hover:text-gray-600 transition-colors">
					Photos
				</a>
				<div class="flex gap-6">
					<a href="{base}/" class="text-gray-600 hover:text-gray-900 transition-colors">Gallery</a>
					<a href="{base}/about" class="text-gray-600 hover:text-gray-900 transition-colors">About</a>
					<a href="https://simhydro.com" class="text-gray-600 hover:text-gray-900 transition-colors">Main Site</a>
				</div>
			</div>
		</nav>
	</header>

	<main class="flex-1">
		<slot />
	</main>

	<footer class="bg-white border-t border-gray-200 mt-16">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-gray-600 text-sm">
			<p>© {new Date().getFullYear()} Tian Zhou. All rights reserved.</p>
		</div>
	</footer>
</div>
