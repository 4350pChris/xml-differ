import { OnCreateAppSync } from "vike-vue/types";
import { client } from "../client/client.gen";

export const onCreateApp: OnCreateAppSync = (pageContext) => {
  let apiUrl: string;
  if (import.meta.env.SSR) {
    apiUrl = pageContext.config.apiUrl as string;
    pageContext.apiUrl = apiUrl;
  } else {
    apiUrl = pageContext.apiUrl;
  }
  client.setConfig({
    baseUrl: apiUrl,
  });
};
