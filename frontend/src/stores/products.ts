import { getProductsWithQuantity } from "@/api/products";
import { PaginationLinks } from "@/types/pagination";
import { Product, ProductRequest } from "@/types/products";
import { defineStore } from "pinia";

export const useProductsStore = defineStore("products", () => {
  let timerId: number | null = null;
  const search = ref("");
  const products = ref<Product[]>([]);
  const selected = ref<Product[]>([]);
  const selectedWithQuantity = ref<ProductRequest[]>([]);
  const page = ref(0);
  const pagination = ref<PaginationLinks>();
  const loading = ref(false);

  const searchProducts = async () => {
    loading.value = true;
    try {
      const response = await getProductsWithQuantity(search.value, page.value + 1);
      if (response.success) {
        page.value = response.data.data.page;
        if (response.data.data.page === 1) {
          products.value.slice(0);
          products.value = [...response.data.data.items];
        } else {
          products.value = [...products.value, ...response.data.data.items];
        }
        pagination.value = response.data.data.links;
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

  const getQuantity = (id: number) => {
    return selected.value.find((item) => item.id === id)?.quantity || 0;
  };

  const updateQuantity = (id: number, quantity: number) => {
    selectedWithQuantity.value.map((item) => {
      if (item.id === id) {
        item.quantity = quantity;
      }
      return item;
    })
  }

  const selectItem = (id: number) => {
    if (!id) return;
    if (selectedWithQuantity.value.find((item) => item.id === id)) return;

    const item = products.value.find((item) => item.id === id);
    if (item) {
      selected.value.push(item);
      selectedWithQuantity.value.push({
        id: item.id,
        name: item.name,
        quantity: 1,
      });
    }
  };

  const deleteItem = (id: number) => {
    selected.value = selected.value.filter((item) => item.id !== id);
    selectedWithQuantity.value = selectedWithQuantity.value.filter(
      (item) => item.id !== id
    );
  }

  const clear = () => {
    search.value = "";
    selected.value = [];
    selectedWithQuantity.value = [];
    page.value = 0;
    pagination.value = undefined;
    products.value = [];
  }

  watch(search, () => {
    if (search.value) {
      page.value = 0;
      searchProducts()
    }
  })

  return {
    search,
    products,
    selected,
    selectedWithQuantity,
    page,
    pagination,
    loading,
    searchProducts,
    updateQuantity,
    handleSearch,
    getQuantity,
    selectItem,
    deleteItem,
    clear,
  }
});
