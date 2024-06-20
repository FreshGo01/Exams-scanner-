<script setup></script>

<template>
  <v-card class="mx-auto pa-12 pb-8" elevation="8" style="width: 1800px" rounded="lg">
    <header class="d-flex align-center">
      <h1 class="text-center">การสร้างการสอบ</h1>
      <v-spacer></v-spacer>
      <v-btn>เพิ่มการสอบ</v-btn>
    </header>

    <v-table>
      <thead>
        <tr>
          <th>วิชา</th>
          <th>รหัสวิชา</th>
          <th>ปีการศึกษา</th>
          <th>ประเภทการสอบ</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>ENGLISH</td>
          <td>123456</td>
          <td>2567</td>
          <td>สอบปลายภาค</td>
          <td class="options">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props"><v-icon icon="mdi-settings-helper"></v-icon></v-btn>
              </template>
              <v-list>
                <v-list-item>
                  <v-list-item-title>สร้างเฉลย</v-list-item-title>
                  <v-list-item-title>ตรวจข้อสอบ</v-list-item-title>
                  <v-list-item-title>ลบ</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>
