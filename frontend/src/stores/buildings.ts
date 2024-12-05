import { getBuildings } from "@/api/building";
import { Building } from "@/types/buildings";
import { defineStore } from "pinia";

export const useBuildingsStore = defineStore('buildings', () => {
  let timerId: number | null = null;
  const search = ref("");
  const buildings = ref<Building[]>([]);
  const selected = ref<Building>();
  const loading = ref(false);

  const searchBuldings = async () => {
    loading.value = true;
    try {
      const response = await getBuildings(search.value);
      if (response.success) {
        buildings.value.slice(0);
        buildings.value = [...response.data.data.items];
      }
      console.log(response);
    } catch (error) {
      console.log(error);
    } finally {
      loading.value = false;
    }
  };

  const handleSearch = (newSearch: string) => {
    clearTimeout(timerId!);
    timerId = setTimeout(() => {
      search.value = newSearch;
    }, 500)
  }

  const clear = () => {
    search.value = "";
    selected.value = undefined;
  }

  watch(search, () => {
    if (search.value) {
      searchBuldings()
    }
  })

  return {
    search,
    buildings,
    selected,
    loading,
    searchBuldings,
    handleSearch,
    clear,
  }
})
