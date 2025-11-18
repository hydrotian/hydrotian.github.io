import type { PageLoad } from './$types';

export interface Photo {
	slug: string;
	title: string;
	date: string;
	location: string;
	category: string;
	thumbnail: string;
	image: string;
	description?: string;
	camera?: string;
	lens?: string;
	settings?: string;
}

export const load: PageLoad = async () => {
	// Sample photos - replace with your actual data
	const photos: Photo[] = [
		{
			slug: 'sample-1',
			title: 'Mountain Vista',
			date: '2024-01-15',
			location: 'Pacific Northwest',
			category: 'landscape',
			thumbnail: 'images/sample-1-thumb.jpg',
			image: 'images/sample-1.jpg',
			description: 'A stunning view of mountain peaks at golden hour',
			camera: 'Canon EOS R5',
			lens: '24-70mm f/2.8',
			settings: 'ISO 100, f/8, 1/250s'
		},
		{
			slug: 'sample-2',
			title: 'Urban Reflection',
			date: '2024-02-20',
			location: 'Seattle, WA',
			category: 'street',
			thumbnail: 'images/sample-2-thumb.jpg',
			image: 'images/sample-2.jpg',
			description: 'Reflections in a rain-soaked street',
			camera: 'Fujifilm X-T4',
			lens: '35mm f/1.4',
			settings: 'ISO 800, f/2.8, 1/125s'
		},
		{
			slug: 'sample-3',
			title: 'Forest Light',
			date: '2024-03-10',
			location: 'Olympic National Park',
			category: 'nature',
			thumbnail: 'images/sample-3-thumb.jpg',
			image: 'images/sample-3.jpg',
			description: 'Morning light filtering through ancient trees',
			camera: 'Sony A7IV',
			lens: '70-200mm f/2.8',
			settings: 'ISO 400, f/4, 1/500s'
		}
	];

	return {
		photos
	};
};

export const prerender = true;
