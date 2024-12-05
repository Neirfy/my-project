<template>
  <v-row>
    <v-col cols="12">
      <v-autocomplete v-model="selected" variant="outlined" :loading :search="search" :items="buildings"
        item-title="name" item-value="id" label="Выберите объекты" placeholder="Введите адресс"
        @update:search="buildingsStore.handleSearch" no-data-text="Ничего не найдено" solo clearable hide-details />
    </v-col>
  </v-row>

</template>

<script setup lang="ts">
import { useBuildingsStore } from '@/stores/buildings';
import { storeToRefs } from 'pinia';

const buildingsStore = useBuildingsStore();
const { search, buildings, selected, loading } = storeToRefs(buildingsStore)
</script>
