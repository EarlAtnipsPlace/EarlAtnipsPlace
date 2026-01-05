
import { defineCollection, z } from 'astro:content';

const postsCollection = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    layout: z.string(),
    postDate: z.date(),
    hideFromPostList: z.boolean().default(false),
  }),
});

export const collections = {
  posts: postsCollection,
};
