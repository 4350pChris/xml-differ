export default {
  ssr: process.env.API_URL_SSR || process.env.API_URL_CLIENT,
  client: process.env.API_URL_CLIENT,
};
