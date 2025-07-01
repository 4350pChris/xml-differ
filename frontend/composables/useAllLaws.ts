import { useQuery } from "@tanstack/vue-query";
import { getLawsLawsGetOptions } from "../client/@tanstack/vue-query.gen";

export function useAllLaws() {
  return useQuery(getLawsLawsGetOptions());
}
