import { deleteUserByUsername, getUsers } from "@/api/users";
import { User } from "@/types/auth";
import { defineStore } from "pinia";

export const useUsersStore = defineStore("users", () => {
  const users = ref<User[]>([]);
  const loading = ref(false);

  const get = async () => {
    try {
      loading.value = true;
      const response = await getUsers();
      if (response.success) {
        users.value.slice(0);
        users.value = [...response.data.data.items];
      }
    } catch (error) {
      console.log(error);
    } finally {
      loading.value = false;
    }
  };

  const deleteUser = async (username: string, closeModal: () => void) => {
    try {
      const response = await deleteUserByUsername(username);
      console.log(response);
      if (response.success) {
        users.value = users.value.filter((item) => item.username !== username);
      }
    } catch (error) {
      console.log(error);
    } finally {
      closeModal();
    }
  };

  return {
    users,
    loading,
    get,
    deleteUser,
  };
});
