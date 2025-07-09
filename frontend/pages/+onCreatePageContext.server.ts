import { PageContextServer } from "vike/types";

export const onCreatePageContext = (pageContext: PageContextServer) => {
  const { ssr, client } = pageContext.config.apiUrl!;
  pageContext.apiUrl = ssr || client;
};
