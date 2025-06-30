import { LawVersionListProjection, PaginatedParagraphCollection } from "../client";
import { computed, MaybeRefOrGetter, toValue } from "vue";
import { getParagraphsVersionsVersionIdParagraphsGetOptions } from "../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";

export function useParagraphs(versionId: MaybeRefOrGetter<LawVersionListProjection["id"]>) {
  const options = computed(() => {
    const id = toValue(versionId);
    const qOptions = getParagraphsVersionsVersionIdParagraphsGetOptions({
      path: {
        version_id: id,
      },
    });

    const enabled = !!id;
    return { ...qOptions, enabled, select: (data: PaginatedParagraphCollection) => data.paragraphs };
  });

  return useQuery(options);
}
