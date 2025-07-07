import { OnCreateAppSync } from "vike-vue/types";
import { client } from "../client/client.gen";

export const onCreateApp: OnCreateAppSync = (pageContext) => {
  let apiUrl: string;
  if (import.meta.env.SSR) {
    const { ssr, client } = pageContext.config.apiUrl!;
    console.log(`Using API URL: SSR=${ssr}, Client=${client}`);
    apiUrl = ssr;
    pageContext.apiUrl = client;
  } else {
    apiUrl = pageContext.apiUrl;
  }
  client.setConfig({
    baseUrl: apiUrl,
  });
};
