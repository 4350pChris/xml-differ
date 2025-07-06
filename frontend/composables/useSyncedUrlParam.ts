import { usePageContext } from "vike-vue/usePageContext";
import { useUrlSearchParams, watchImmediate } from "@vueuse/core";
import { ref } from "vue";

type SyncedUrlParams<T> = {
  serialize: (value: T) => string;
  deserialize: (value: string) => T;
  initialValue: T;
};

export const makeBoolOptions = (initialValue: boolean) =>
  ({
    serialize: (value) => value.toString(),
    deserialize: (value) => value === "true",
    initialValue: initialValue,
  }) satisfies SyncedUrlParams<boolean>;

export const makeStringOptions = <T extends string>(initialValue: T) =>
  ({
    serialize: (value) => value,
    deserialize: (value) => value as T,
    initialValue: initialValue,
  }) satisfies SyncedUrlParams<T>;

export const makeFloatOptions = (initialValue: number) =>
  ({
    serialize: (value) => value.toString(),
    deserialize: (value) => parseFloat(value),
    initialValue: initialValue,
  }) satisfies SyncedUrlParams<number>;

export function useSyncedUrlParam<T extends Record<string, SyncedUrlParams<any>>>(options: T) {
  const ctx = usePageContext();
  const urlParams = useUrlSearchParams();

  const getInitialValue = (key: string, { deserialize, initialValue }: SyncedUrlParams<T>) => {
    const search = ctx.urlParsed.search;
    const exists = key in search;
    if (exists) {
      return deserialize(search[key]);
    }
    return initialValue;
  };

  const val = ref(
    Object.fromEntries(Object.entries(options).map(([key, option]) => [key, getInitialValue(key, option)])) as {
      [K in keyof T]: T[K]["initialValue"];
    },
  );
  watchImmediate(
    val,
    (newValue) => {
      Object.entries(newValue).forEach(([key, value]) => {
        urlParams[key] = options[key].serialize(value);
      });
    },
    { deep: true },
  );

  return val;
}
