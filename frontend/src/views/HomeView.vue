<script setup>
import router from '@/router'
import { useExamStore } from '@/stores/exam'
import { onMounted } from 'vue'
const examStore = useExamStore()

onMounted(() => {
  examStore.fetchExams()
})
</script>
<!-- eslint-disable vue/valid-v-slot -->
<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" elevation="8" rounded="lg">
      <v-data-table :headers="examStore.columns" :items="examStore.exams">
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>ข้อมูลการสอบของฉัน</v-toolbar-title>
            <v-btn color="success" variant="plain" @click="router.push({ name: 'addexam' })">
              เพิ่มข้อมูล
            </v-btn>
          </v-toolbar>
        </template>
        <template #item.createdAt="{ item }">
          {{ new Date(item.createdAt).toLocaleDateString() }}
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon
            class="me-2"
            size="small"
            @click="router.push({ name: 'uploadanswers', params: { id: item.id } })"
          >
            mdi-note-search-outline
          </v-icon>
          <v-icon size="small" @click="examStore.deleteItem(item)"> mdi-delete </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>
