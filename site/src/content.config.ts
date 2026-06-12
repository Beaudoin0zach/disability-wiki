import { defineCollection, z } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

// Content is the existing wiki markdown, symlinked into src/content/docs/.
// The extra fields are Wiki.js frontmatter we tolerate rather than migrate.
export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			extend: z.object({
				published: z.boolean().optional(),
				date: z.coerce.date().optional(),
				dateCreated: z.coerce.date().optional(),
				editor: z.string().optional(),
				tags: z.union([z.string(), z.array(z.string()), z.null()]).optional(),
			}),
		}),
	}),
};
