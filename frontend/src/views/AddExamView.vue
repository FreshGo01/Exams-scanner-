<script setup>
import { watch } from 'vue'
import { useExamStore } from '@/stores/exam'
const examStore = useExamStore()

// อัปเดต questions เมื่อจำนวนคำถามเปลี่ยนแปลง
watch(
  () => examStore.numberOfQuestions,
  () => {
    examStore.updateQuestions()
  }
)

const items = [
  {
    title: 'Home',
    disabled: false,
    href: '/'
  },
  {
    title: 'Add Exam',
    disabled: true
  }
]
</script>

<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" elevation="8" style="width: 1000px" rounded="lg">
      <v-breadcrumbs :items="items"></v-breadcrumbs>
      <v-card-title class="text-h4 text-center mb-10">Add Exam</v-card-title>
      <v-form v-model="examStore.form" @submit.prevent="examStore.onSubmit">
        <div class="text-subtitle-1 text-medium-emphasis">Topic</div>
        <v-text-field
          v-model="examStore.AddForm.topic"
          density="compact"
          placeholder="ใส่หัวข้อการสอบ เช่น สอบเก็บคะแนน"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Details</div>
        <v-text-field
          v-model="examStore.AddForm.details"
          density="compact"
          placeholder="ใส่รายละเอียดของการสอบ เช่น สอบเก็บคะแนน ครั้งที่ 1 รายวิชาวิทยาศาสตร์เพื่อชีวิต ประจำปีการศึกษา 2564"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">ประเภทการสอบ</div>
        <v-select
          v-model="examStore.AddForm.answerssheet_template"
          :items="['Multiple Choice']"
          variant="outlined"
        ></v-select>

        <div class="text-subtitle-1 text-medium-emphasis">จำนวนข้อ</div>
        <v-number-input
          v-model="examStore.numberOfQuestions"
          :max="25"
          :min="1"
          :step="1"
        ></v-number-input>

        <div class="text-subtitle-1 text-medium-emphasis">เฉลย</div>
        <div v-for="question in examStore.questions" :key="question.id" class="mb-4">
          <div>Question {{ question.id }}</div>
          <v-row>
            <v-col cols="auto" v-for="option in question.options" :key="option.label">
              <v-checkbox v-model="option.value" :label="option.label"></v-checkbox>
            </v-col>
          </v-row>
        </div>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue"
            size="large"
            type="submit"
            variant="tonal"
            :disabled="!examStore.canSubmit"
          >
            <span class="mr-2">Complete</span>
            <v-icon right>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>
