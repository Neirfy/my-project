<template>
  <v-navigation-drawer v-model="drawer" :rail="rail" permanent @click="rail = false">
    <v-list-item prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg" title="John Leider" nav>
      <template v-slot:append>
        <v-btn icon="mdi-chevron-left" variant="text" @click.stop="rail = !rail"></v-btn>
      </template>
    </v-list-item>

    <v-divider />

    <v-list>
      <v-list-item color="#FF9140" link prepend-icon="mdi-account-multiple" title="Пользователи" :to="'/admin/users'" />
      <v-divider thickness="2" />
      <!-- <template v-for="report in reports" :key="report.title">
        <v-list-item
          color="#FF9140"
          link
          :prepend-icon="report.icon"
          :title="report.title"
          :to="`/reports/${report.link}`"
        />
        <v-divider thickness="2" />
      </template> -->

    </v-list>

    <template #append>
      <div class="pa-2">
        <v-btn
          block
          title="Выйти"
          @click="() =>{}"
        >
        <v-icon icon="mdi-logout" />
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { useDrawerStore } from '@/stores/drawer';
import { storeToRefs } from 'pinia';

const items = [
  { title: 'Главная', icon: 'mdi-home', route: '/' },
  { title: 'О нас', icon: 'mdi-information', route: '/about' },
  { title: 'Контакты', icon: 'mdi-phone', route: '/contact' },
];

// const drawerStore = useDrawerStore();
// const { drawer } = storeToRefs(drawerStore);

const drawer = ref(true);
const rail = ref(true);
const router = useRouter();

const navigateTo = (route) => {
  router.push(route);
};
</script>
