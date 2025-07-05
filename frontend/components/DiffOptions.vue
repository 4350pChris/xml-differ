<script setup lang="ts">
import { GetDiffDiffLeftVersionIdRightVersionIdGetData, LawDetailProjection } from "../client";
import LawVersionSelector from "./LawVersionSelector.vue";
import { ref, useTemplateRef } from "vue";
import DiffViewSwitch from "./DiffViewSwitch.vue";

export type DifferOptions = GetDiffDiffLeftVersionIdRightVersionIdGetData["query"];

const props = defineProps<{
  law: LawDetailProjection;
  initial: {
    oldVersion: string;
    newVersion: string;
    options: DifferOptions;
  };
}>();

defineOptions({
  inheritAttrs: false,
});

const left = ref<string>(props.initial.oldVersion);
const right = ref<string>(props.initial.newVersion);
const options = ref<DifferOptions>({ ...props.initial.options });

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
  <button class="btn btn-circle z-40" v-bind="$attrs" title="Optionen" @click="modalEl?.showModal()">
    <svg xmlns="http://www.w3.org/2000/svg" class="size-6" viewBox="0 0 24 24">
      <!-- Icon from Material Design Icons by Pictogrammers - https://github.com/Templarian/MaterialDesign/blob/master/LICENSE -->
      <path
        fill="currentColor"
        d="M6 0a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6l-6-6zm0 2h7v5h5v11H6zm1 20v2h2v-2zm4 0v2h2v-2zm4 0v2h2v-2z"
      />
    </svg>
  </button>
  <dialog ref="modal" class="modal modal-bottom sm:modal-middle" @submit.stop>
    <div class="modal-box">
      <DiffViewSwitch v-model="options.split" />
      <fieldset class="fieldset bg-base-100">
        <legend class="fieldset-legend text-lg">Versionen</legend>
        <LawVersionSelector v-model="left" legend="Alte Version" :versions="law.versions" />
        <LawVersionSelector v-model="right" legend="Neue Version" :versions="law.versions" />
      </fieldset>
      <fieldset class="fieldset bg-base-100">
        <legend class="fieldset-legend text-lg">XMLdiff</legend>
        <label class="label">
          <input v-model="options.fast_match" type="checkbox" class="checkbox" name="fast_match" />
          Fast Match
        </label>
        <label class="input">
          <input v-model="options.F" type="number" name="F" :min="0" :max="1" :step="0.1" />
          <span class="label">Ähnlichkeit (0.0 - 1.0)</span>
        </label>
        <label class="select">
          <select id="ratio_mode" v-model="options.ratio_mode" name="ratio_mode">
            <option v-for="option in ratioOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <span class="label">Ähnlichkeitsmodus</span>
        </label>
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
