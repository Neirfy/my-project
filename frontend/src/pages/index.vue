<template>
  <Building />
  <Products />
  <v-row>
    <v-col>
      <v-locale-provider locale="ru">
        <v-date-input v-model="date" color="black" :min="new Date(new Date().setDate(new Date().getDate() - 1))"
          label="Желаемая дата доставки" prepend-icon=""/>
      </v-locale-provider>
    </v-col>
  </v-row>
  <Comment />
  <v-row justify="end">
    <v-col sm="4" md="3" lg="2" cols="5">
      <v-btn :loading class="w-100" color="black" @click="handleClick">
        Отправить
      </v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { VDateInput } from 'vuetify/labs/VDateInput'
import { createSmart } from '@/api/smart';
import { useBuildingsStore } from '@/stores/buildings';
import { useCommentStore } from '@/stores/comment';
import { useProductsStore } from '@/stores/products';
import { useUserStore } from '@/stores/user';
import { SmartRequest } from '@/types/smart';
import moment from 'moment';

const buildingsStore = useBuildingsStore();
const productsStore = useProductsStore();
const commentStore = useCommentStore();
const userStore = useUserStore();
const loading = ref(false);

const date = ref(new Date())

const handleClick = async () => {
  const obj = buildingsStore.buildings[0]
  if (!obj) return
  const data: SmartRequest = {
    name: userStore.user?.fio || '',
    object: obj.id,
    date: moment(date.value).set({ hour: 12, minute: 0, second: 0, millisecond: 0 }).format(),
    address: obj.address,
    products: productsStore.selectedWithQuantity,
    urgency: commentStore.urgency,
    comment: commentStore.comment,
  }
  try {
    loading.value = true
    const response = await createSmart(data)
    if (response.success) {
      buildingsStore.clear()
      productsStore.clear()
      commentStore.clear()
      date.value = new Date()
    }
  } catch (error) {
    console.log(error)
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
/* Дополнительные стили, если необходимо */
</style>
