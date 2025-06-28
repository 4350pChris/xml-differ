import { useData } from "vike-vue/useData";
import { Data } from "../pages/+data";

export function useLawList() {
  const data = useData<Data>();

  const laws = data.laws.map((law) => ({
    ...law,
    url: `/law/${law.id}`,
  }));

  return { laws };
}
