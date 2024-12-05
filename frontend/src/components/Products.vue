<template>
  <v-row>
    <v-col cols="12">
      <v-autocomplete variant="outlined" :loading :search="search" :items="products" item-title="name" item-value="id"
        label="Поиск товаров" placeholder="Введите наименование..." @update:search="productsStore.handleSearch"
        @update:model-value="productsStore.selectItem" no-data-text="Ничего не найдено" solo clearable hide-details>
        <template #item="{ props, item }">
          <v-list-item class="d-flex align-center" v-bind="props">
            <v-img v-if="item.raw.image" :src="item.raw.image" max-width="40" class="mr-2" />
          </v-list-item>
        </template>
        <template v-if="products.length && pagination?.next" #append-item>
          <v-list-item>
            <v-list-item-content class="d-flex justify-center">
              <v-btn :loading @click="productsStore.searchProducts" color="black"> Еще </v-btn>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-autocomplete>
    </v-col>
  </v-row>

  <!-- Список выбранных элементов -->
  <v-row>
    <v-col cols="12">
      <v-data-table v-if="selectedWithQuantity.length" :headers="headers" :items="selectedWithQuantity"
        hide-default-footer disable-sort items-per-page="-1">
        <template #item.quantity="{ item }">
          <v-text-field v-model.number="item.quantity"
            @update:model-value="(quantity) => handleUpdateQuantity(Number(quantity), item.id)" variant="outlined"
            density="compact" type="number" hide-details />
        </template>
        <template #item.rest="{ item }">
          {{ productsStore.getQuantity(item.id) - item.quantity }}
        </template>
        <template #item.actions="{ item }">
          <v-icon size="small" @click="productsStore.deleteItem(item.id)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { useProductsStore } from '@/stores/products';
import { storeToRefs } from 'pinia';

type Headers = {
  title: string;
  align?: 'start' | 'end' | 'center' | undefined;
  key: string;
}

const headers = ref<Headers[]>([
  { title: 'Наименование', align: 'start', key: 'name' },
  { title: 'Колличество', align: 'end', key: 'quantity' },
  { title: 'Остаток', align: 'end', key: 'rest' },
  { title: 'Действия', key: 'actions', }
])


const productsStore = useProductsStore();
const { search, loading, products, selectedWithQuantity, pagination } = storeToRefs(productsStore)

const handleUpdateQuantity = (quantity: number, id: number) => {
  // проверка на максимальное колличество (не понадобилась)
  // const maxQuantity = productsStore.getQuantity(id);
  // if (maxQuantity < Number(quantity)) {
  //   productsStore.updateQuantity(id, maxQuantity);
  // }
  if (quantity === 0) {
    productsStore.updateQuantity(id, 1);
  }
}

</script>
