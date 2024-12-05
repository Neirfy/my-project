import { defineStore } from "pinia";

export const useCommentStore = defineStore("comment", () => {
  const comment = ref("");
  const urgency = ref(false);

  const clear = () => {
    comment.value = "";
    urgency.value = false;
  };

  return {
    comment,
    urgency,
    clear,
  };
});
