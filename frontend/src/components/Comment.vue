<template>
  <v-row>
    <v-col cols="12">
      <v-switch v-model="urgency" color="black" label="Срочно" />
    </v-col>
    <v-col cols="12">
      <v-textarea v-model="comment" label="Комментарии" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { useCommentStore } from '@/stores/comment';
import { storeToRefs } from 'pinia';


const commentStore = useCommentStore();
const { urgency, comment } = storeToRefs(commentStore)
</script>
