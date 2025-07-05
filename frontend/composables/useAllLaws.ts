import { useQuery } from "@tanstack/vue-query";
import { getLawsLawsGetOptions } from "../client/@tanstack/vue-query.gen";
import { computed, MaybeRefOrGetter, toValue } from "vue";

export function useAllLaws(all: MaybeRefOrGetter<boolean> = false) {
  const options = computed(() =>
    getLawsLawsGetOptions({
      query: {
        all: toValue(all),
      },
    }),
  );
  return useQuery(options);
}
