<template>
  <v-container fluid>
    <v-card>
      <v-card-title>Список сотрудников</v-card-title>
      <v-data-table :items="usersStore.users" :headers="headers" class="elevation-1" hide-default-footer>
        <template v-slot:item.actions="{ item }">
          <div class="actions">
            <v-btn append-icon="mdi-pencil" @click="() => openDialogChange(item)">
              ред.
            </v-btn>
            <v-btn append-icon="mdi-delete" color="red" @click="() => openDialogDelete(item)">
              Удалить
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог подтверждения -->
    <v-dialog v-model="isConfirmDialogOpen" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить сотрудника {{ selectedUser?.fio }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green" @click="closeDialog">Отмена</v-btn>
          <v-btn color="red" @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="isChange" max-width="400">
      <v-card title="Регистрация">
        <v-card-text>
          <v-form ref="form" autocomplete="off" v-model="isFormValid" lazy-validation>
            <v-text-field v-model="formData.fio" label="ФИО" :rules="[rules.required]" required />
            <v-text-field v-model="formData.email" :rules="[rules.required, rules.email]" label="Email" type="email"
              required />
            <v-text-field v-model="formData.username" label="Логин" :rules="[rules.required]" required />
            <v-text-field v-model="formData.phone" label="Телефон" :rules="[rules.required]" required />
            <!-- <v-text-field v-model="formData.phone" :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'" @click:append-inner="togglePasswordVisibility" label="Пароль"
              :rules="[rules.required, rules.min(6)]" required /> -->
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-btn text="Закрыть" @click="isChange = false" />
          <v-spacer></v-spacer>
          <v-btn color="black darken-1" @click="submitForm(() => isChange = false)"
            :disabled="!isFormValid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts" setup>
import { updateUser } from '@/api/users';
import { useUsersStore } from '@/stores/users';
import { User } from '@/types/auth';

const usersStore = useUsersStore()
const headers = [
  { title: 'Имя', key: 'fio' },
  { title: 'E-mail', key: 'email' },
  { title: 'Логин', key: 'username' },
  { title: 'Действия', value: 'actions', sortable: false },
];
const isConfirmDialogOpen = ref(false)
const isChange = ref(false)
const selectedUser = ref<User>()

const isFormValid = ref(false);
const formData = ref({
  username: '',
  nickname: '',
  fio: '',
  email: '',
  phone: '',
});

const rules = {
  required: (value: string) => !!value || 'Это поле обязательно',
  min: (minLength: number) => (value: string) =>
    value.length >= minLength || `Минимальная длина ${minLength} символов`,
  email: (v: string) =>
    /.+@.+\..+/.test(v) || 'Введите корректный email'
};


const submitForm = async (closeDialog: () => void) => {
  console.log(isFormValid.value)
  if (isFormValid.value && selectedUser.value) {
    console.log('Submitted data:', formData.value);
    try {
      const response = await updateUser({
        dept_id: selectedUser.value?.dept_id,
        ...formData.value
      })
      if (response.success) {
        usersStore.get()
        closeDialog()
      }
    } catch (error) {
      console.log(error)
    }
    console.log('Submitted data:', formData.value);
  }
};

const openDialogDelete = (user: User) => {
  isConfirmDialogOpen.value = true
  selectedUser.value = user
}

const openDialogChange = (user: User) => {
  isChange.value = true
  selectedUser.value = user
  formData.value = {
    username: user.username,
    nickname: user.nickname,
    fio: user.fio,
    email: user.email,
    phone: user.phone
  }
}
const confirmDelete = () => {
  usersStore.deleteUser(selectedUser.value!.username, closeDialog)
}

const closeDialog = () => {
  isConfirmDialogOpen.value = false
  selectedUser.value = undefined
}

onMounted(() => {
  usersStore.get()
})

</script>

<style scoped>
.actions {
  display: flex;
  gap: 10px;
  justify-content: end;
}
</style>
