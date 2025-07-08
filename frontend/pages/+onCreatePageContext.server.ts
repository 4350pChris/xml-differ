import { PageContextServer } from "vike/types";

export const onCreatePageContext = (pageContext: PageContextServer) => {
  pageContext.apiUrl = pageContext.config.apiUrl as string;
};
