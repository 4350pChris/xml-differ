import type { PageContext } from "vike/types";

export function getTitle(pageContext: PageContext) {
  // The value exported by /pages/**/+title.js is available at pageContext.config.title
  const val = pageContext.config.title;
  if (!val) throw new Error("No title found in pageContext.config.title");
  if (typeof val === "string") return val;
  if (typeof val === "function") return val(pageContext);
}
