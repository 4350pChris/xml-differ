export default {
  ssr: process.env.API_URL_SSR || process.env.API_URL,
  client: process.env.API_URL,
};
