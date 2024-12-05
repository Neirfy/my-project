<template>
  <v-app>
    <!-- Боковая панель -->
    <v-navigation-drawer app v-model="drawer" temporary>
      <v-list-item>
        <v-list-item-title>
          {{ userStore.user?.fio }}
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ userStore.user?.is_superuser ? 'Администратор' : 'Монтажник' }}
        </v-list-item-subtitle>
      </v-list-item>
      <v-divider />
      <v-list-item v-for="item in items" :key="item.title" :prepend-icon="item.icon" @click="navigateTo(item.route)">
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
      <v-list-item v-if="userStore.user?.is_superuser" v-for="item in adminItems" :key="item.title"
        :prepend-icon="item.icon" @click="navigateTo(item.route)">
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
      <template #append>
        <div class="pa-2">
          <v-btn variant='flat' color="black" prepend-icon="mdi-logout" block title="Выйти" @click="handleLogout">
            Выйти
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title><img class="logo" src="/black.png" alt=""></v-toolbar-title>
      <v-spacer />
      <v-dialog v-model="dialog" max-width="500">
        <template #activator="{ props }">
          <v-btn v-if="route.path == '/employees'" base-color="indigo-lighten-2" class="mr-4"
            prepend-icon="mdi-account-plus" variant="tonal" v-bind="props"> Добавить </v-btn>
        </template>
        <template v-slot:default="{ isActive }">
          <v-card title="Регистрация">
            <v-card-text>
              <v-form ref="form" autocomplete="off" v-model="isFormValid" lazy-validation>
                <v-text-field v-model="formData.fullName" label="ФИО" :rules="[rules.required]" required></v-text-field>
                <v-text-field v-model="formData.email" :rules="[rules.required, rules.email]" label="Email" type="email"
                  required></v-text-field>
                <v-text-field v-model="formData.username" label="Логин" :rules="[rules.required]"
                  required></v-text-field>
                <v-text-field v-model="formData.password" :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'" @click:append-inner="togglePasswordVisibility"
                  label="Пароль" :rules="[rules.required, rules.min(6)]" required></v-text-field>
              </v-form>
            </v-card-text>

            <v-card-actions>
              <v-btn text="Закрыть" @click="isActive.value = false" />
              <v-spacer></v-spacer>
              <v-btn color="black darken-1" @click="submitForm(() => isActive.value = false)"
                :disabled="!isFormValid">Регистрация</v-btn>
            </v-card-actions>
          </v-card>
        </template>
      </v-dialog>
    </v-app-bar>



    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { logoutUser } from '@/api/auth';
import { registerUser } from '@/api/users';
import { useUserStore } from '@/stores/user';
import { UserRegister } from '@/types/auth';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore()
const drawer = ref(false);
const dialog = ref(false);
const isFormValid = ref(false);
const showPassword = ref(false);
const formData = ref({
  fullName: '',
  email: '',
  username: '',
  password: '',
});


const items = [
  { title: 'Главная', icon: 'mdi-home', route: '/', isAdmin: false },
];
const adminItems = [
  { title: 'Сотрудники', icon: 'mdi-account-group', route: '/employees', isAdmin: true },
]

const rules = {
  required: (value: string) => !!value || 'Это поле обязательно',
  min: (minLength: number) => (value: string) =>
    value.length >= minLength || `Минимальная длина ${minLength} символов`,
  email: (v: string) =>
    /.+@.+\..+/.test(v) || 'Введите корректный email'
};

const submitForm = async (closeDialog: () => void) => {
  const data: UserRegister = {
    username: formData.value.username,
    password: formData.value.password,
    nickname: formData.value.username,
    fio: formData.value.fullName,
    email: formData.value.email
  }

  if (isFormValid.value) {
    try {
      const response = await registerUser(data)
      if (response.success) {
        closeDialog()
      }
    } catch (error) {
      console.log(error)
    }
    console.log('Submitted data:', formData.value);
  }
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
};

const navigateTo = (route: string) => {
  router.push(route);
};

const handleLogout = async () => {
  try {
    await logoutUser()
    router.push('/login')
  } catch (error) {
    console.log(error)
  }
}

onMounted(() => {
  userStore.getTokenFromLocal()
  userStore.getUserInfo()
})


</script>

<style>
.logo {
  max-height: 100%;
  max-width: 100%;
  width: 230px;
}

/* Добавьте стили при необходимости */
</style>
