<script setup>
// import router from '@/router'
import { useAnswerStore } from '@/stores/answer'
import { onMounted } from 'vue'
const answerStore = useAnswerStore()
const items = [
  {
    title: 'Home',
    disabled: false,
    href: '/'
  },
  {
    title: 'Upload Answers',
    disabled: true
  }
]

onMounted(() => {
  answerStore.fetchAnswers()
})
</script>
<!-- eslint-disable vue/valid-v-slot -->
<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" elevation="8" rounded="lg" style="width: 1000px">
      <v-breadcrumbs class="mb-6" :items="items"></v-breadcrumbs>
      <v-card-title class="text-h4 text-center mb-10">Upload Answers</v-card-title>
      <v-form v-model="answerStore.form" @submit.prevent="answerStore.onSubmit(examId)">
        <v-row>
          <v-col>
            <v-file-input
              :rules="answerStore.rules"
              accept="image/png, image/jpeg, image/bmp"
              label="Upload image"
              prepend-icon="mdi-camera"
              placeholder="Choose an image file, or drag it here"
              v-model="answerStore.files"
              multiple
              counter
              show-size
            ></v-file-input>
          </v-col>
          <v-col cols="auto">
            <v-btn
              color="blue"
              size="large"
              variant="tonal"
              :disabled="!answerStore.form"
              type="submit"
            >
              Upload
            </v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn
              color="success"
              size="large"
              variant="tonal"
              @click="answerStore.fetchAnswers()"
              prepend-icon="mdi-refresh"
              >Refresh</v-btn
            >
          </v-col>
        </v-row>
      </v-form>
      <v-row>
        <v-data-table :headers="answerStore.columns" :items="answerStore.answers">
          <template v-slot:item.actions="{ item }">
            <v-icon
              class="me-2"
              size="small"
              @click="answerStore.openDialog(`http://localhost:3000/uploads/${item.image}`)"
            >
              mdi-image-search-outline
            </v-icon>
            <v-icon size="small" @click="answerStore.deleteItem(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-row>
    </v-card>
    <v-dialog v-model="answerStore.dialog" width="auto">
      <v-img :src="answerStore.selectedFileUrl" cover max-width="600" width="auto"></v-img>
    </v-dialog>
  </v-container>
</template>
