import { defineStore } from "pinia";

export  const useDrawerStore = defineStore('drawer', () => {
  const drawer = ref(true);

  const toogle = () => {
    drawer.value = !drawer.value
  }

  return {
    drawer,
    toogle
  }
})
