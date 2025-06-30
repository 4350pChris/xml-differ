import { XMLParser } from "fast-xml-parser";
import { computed, MaybeRefOrGetter, toValue } from "vue";

export function useParseParagraphXML(content: MaybeRefOrGetter<string>) {
  const parser = new XMLParser({
    preserveOrder: true,
  });

  const parsed = computed(() => {
    try {
      return parser.parse(toValue(content));
    } catch (error) {
      console.error("Error parsing XML content:", error);
      return null;
    }
  });

  return { parsed };
}
