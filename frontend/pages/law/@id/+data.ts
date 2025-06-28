import { render } from "vike/abort";
import { getLawLawsLawIdGet } from "../../../client";
import { PageContextServer } from "vike/types";

export type Data = Awaited<ReturnType<typeof data>>;

export const data = async (pageContext: PageContextServer) => {
  const res = await getLawLawsLawIdGet({
    path: {
      law_id: pageContext.routeParams.id,
    },
  });

  if (res.error || !res.data) {
    throw render(500);
  }

  return { law: res.data };
};
