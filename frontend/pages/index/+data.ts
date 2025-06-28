import { getLawsLawsGet } from "../../client";
import { render } from "vike/abort";

export type Data = Awaited<ReturnType<typeof data>>;

export const data = async () => {
  const res = await getLawsLawsGet();

  if (res.error || !res.data) {
    throw render(500);
  }

  return { laws: res.data };
};
