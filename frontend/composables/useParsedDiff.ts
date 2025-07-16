import { computed, MaybeRefOrGetter, toValue } from "vue";
import { DOMParser } from "linkedom";

export type ChangeType = false | "addition" | "deletion" | "mixed";

export type ParsedDiff = {
  doc: HTMLElement;
  id: string;
  change: ChangeType;
};

function getChangeType(docs: HTMLElement[]): ChangeType {
  const lengthOfModifications = (selector: string) =>
    docs.reduce((acc, doc) => acc + (doc.querySelectorAll(selector)?.length ?? 0), 0);
  const deletions = lengthOfModifications(".diff-del");
  const additions = lengthOfModifications(".diff-insert");

  if (!deletions && !additions) return false;
  if (deletions && additions) return "mixed";
  return deletions ? "deletion" : "addition";
}

function getDocument(content: string): HTMLElement {
  const parser = new DOMParser();
  return parser.parseFromString(content, "text/xml").documentElement as unknown as HTMLElement;
}

export function useParsedDiff(diff: MaybeRefOrGetter<string[][] | undefined>) {
  return computed<ParsedDiff[][]>(() => {
    const unreffedDiff = toValue(diff);
    if (!unreffedDiff) return [];
    return unreffedDiff.map((paragraphs) => {
      const docs = paragraphs.map((content) => getDocument(content));
      const change = getChangeType(docs);
      return docs.map((doc, index) => ({
        doc,
        id: "p" + index + (doc.getAttribute("doknr") || ""),
        change,
      }));
    });
  });
}
