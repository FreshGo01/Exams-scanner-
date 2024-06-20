<script setup>
import { ref } from 'vue'
const form = ref(false)
const CourseTitle = ref(null)
const CourseCode = ref(null)
const AcademicYear = ref(null)
const ExamType = ref(null)

function onSubmit() {
  return
}
</script>

<template>
  <v-container class="d-flex align-center justify-center">
    <v-card class="mx-auto pa-12 pb-8" elevation="8" style="width: 1000px" rounded="lg">
      <v-form v-model="form" @submit.prevent="onSubmit">
        <div class="text-subtitle-1 text-medium-emphasis">วิชา</div>
        <v-text-field
          v-model="CourseTitle"
          density="compact"
          placeholder="ใส่ชื่อวิชา"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">รหัสวิชา</div>
        <v-text-field
          v-model="CourseCode"
          density="compact"
          placeholder="ใส่รหัสวิชา"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">ปีการศึกษา</div>
        <v-text-field
          v-model="AcademicYear"
          density="compact"
          placeholder="ใส่ปีการศึกษา"
          variant="outlined"
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">ประเภทการสอบ</div>
        <v-select
          v-model="ExamType"
          label="เลือกประเภทการสอบ"
          :items="['สอบกลางภาค', 'สอบปลายภาค', 'สอบเก็บคะแนน', 'อื่น ๆ']"
          variant="outlined"
          clearable
        ></v-select>

        <v-divider></v-divider>
            <div>เฉลยจร้าาาาาาาาาาาาาาาาา</div>
        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <!-- ปุ่ม Complete Registration ในกรอบ -->
          <v-btn color="blue" size="small" variant="tonal" text right>
            <span class="mr-2">Complete</span>
            <v-icon right>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>
