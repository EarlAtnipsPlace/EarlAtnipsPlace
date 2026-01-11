// @ts-check
import { defineConfig } from 'astro/config';

import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  integrations: [mdx()],
  site: 'https://earlatnipsplace.github.io',
  base: '/EarlAtnipsPlace/',
  outDir: './docs',
});

