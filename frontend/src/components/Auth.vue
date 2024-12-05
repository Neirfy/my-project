<template>
  <v-container class="d-flex justify-center align-center">
    <v-card class="w-50" max-width="400">
      <v-card-title>
        Вход
      </v-card-title>
      <v-card-text>
        <v-form ref="loginForm" v-model="valid" lazy-validation>
          <v-text-field v-model.trim="login" label="Логин" :rules="loginRules" required />
          <v-text-field v-model.trim="password" label="Пароль" :rules="passwordRules"
            :type="showPassword ? 'text' : 'password'" required append-inner-icon="mdi-eye"
            @click:append-inner="showPassword = !showPassword" />
          <v-alert v-if="errorMessage" type="error" dismissible>
            {{ errorMessage }}
          </v-alert>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :disabled="!valid" color="primary" @click="handleSubmit">
          Войти
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { loginUser } from '@/api/auth'
import { useUserStore } from '@/stores/user';

const valid = ref(false);
const login = ref('');
const password = ref('');
const errorMessage = ref('')
const showPassword = ref(false);
const router = useRouter();
const userStore = useUserStore()

const loginRules = [
  (v: string) => !!v || 'Логин обязателен',
];

const passwordRules = [
  (v: string) => !!v || 'Пароль обязателен',
];

const handleSubmit = async () => {
  errorMessage.value = '';
  if (valid.value) {
    const response = await loginUser(login.value, password.value);
    if (response.success) {
      localStorage.setItem('login', new Date().toString())
      userStore.token = response.data.data.access_token;
      userStore.user = response.data.data.user;
      router.push('/')
    } else {
      errorMessage.value = response.details.msg
    }
  }
};
</script>

<style scoped>
.v-container {
  height: 100vh;
}
</style>
