import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

export async function getSortedPosts(): Promise<CollectionEntry<'posts'>[]> {
    const allPosts = await getCollection('posts');
    const filteredPosts = allPosts.filter(post => !post.data.hideFromPostList);
    filteredPosts.sort((a, b) => b.data.postDate.getTime() - a.data.postDate.getTime());
    return filteredPosts;
}
