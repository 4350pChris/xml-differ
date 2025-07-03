<script setup lang="ts">
import { GetDiffDiffLeftVersionIdRightVersionIdGetData, LawDetailProjection } from "../client";
import LawVersionSelector from "./LawVersionSelector.vue";
import { ref, useTemplateRef } from "vue";

export type DifferOptions = GetDiffDiffLeftVersionIdRightVersionIdGetData["query"];

const props = defineProps<{
  law: LawDetailProjection;
  initial: {
    left: string;
    right: string;
    options: DifferOptions;
  };
}>();

const left = ref<string>(props.initial.left);
const right = ref<string>(props.initial.right);
const options = ref<DifferOptions>(props.initial.options);

const emits = defineEmits<{
  submit: [versions: [string, string], options: DifferOptions];
}>();

const acceptChanges = () => {
  emits("submit", [left.value, right.value], { ...options.value });
};

const modalEl = useTemplateRef<HTMLDialogElement>("modal");

const ratioOptions: { value: DifferOptions["ratio_mode"]; label: string }[] = [
  {
    value: "fast",
    label: "Schnell",
  },
  {
    value: "faster",
    label: "Schneller",
  },
  {
    value: "accurate",
    label: "Genau",
  },
];
</script>

<template>
  <button class="btn fixed bottom-4 left-24" @click="modalEl?.showModal()">open modal</button>
  <dialog ref="modal" class="modal modal-bottom sm:modal-middle" @submit.stop>
    <div class="modal-box">
      <h3 class="text-lg font-bold">Optionen</h3>
      <LawVersionSelector v-model="left" legend="Alte Version" :versions="law.versions" />
      <LawVersionSelector v-model="right" legend="Neue Version" :versions="law.versions" />
      <fieldset class="fieldset bg-base-100 border-base-300 rounded-box w-64 border p-4">
        <legend class="fieldset-legend">XMLdiff Optionen</legend>
        <label class="label">
          <input v-model="options.fast_match" type="checkbox" class="checkbox" name="fast_match" />
          Fast Match
        </label>
        <label class="label">
          <input v-model="options.F" type="number" class="input" name="F" :min="0" :max="1" :step="0.1" />
          F (0.0 - 1.0)
        </label>
        <select v-model="options.ratio_mode" name="ratio_mode" class="select">
          <option v-for="option in ratioOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </fieldset>
      <div class="modal-action">
        <form method="dialog" @submit="acceptChanges">
          <button class="btn">Speichern</button>
        </form>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>
