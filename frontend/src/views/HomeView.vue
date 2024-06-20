<template>
  <div class="app-container">
    <header>
      <input type="text" placeholder="ค้นหา" class="search-bar" />
      <h1>การสร้างการสอบ</h1>
      <button class="add-exam-btn">เพิ่มการสอบ</button>
    </header>
    
    <table>
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
            <div class="dropdown">
              <button class="dropbtn">...</button>
              <div class="dropdown-content">
                <a href="#">สร้างเฉลย</a>
                <a href="#">ตรวจข้อสอบ</a>
                <a href="#">ลบ</a>
              </div>
            </div>
          </td>
        </tr>
        <!-- You can add more rows here -->
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
body, html {
  margin: 0;
  padding: 0;
  font-family: 'Arial', sans-serif;
  background-color: #4B3D33;
  color: #fff;
}

.app-container {
  padding: 20px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  padding: 5px;
  border-radius: 5px;
  border: none;
}

.add-exam-btn {
  padding: 5px 10px;
  background-color: #fff;
  color: #4B3D33;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

h1 {
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #333;
}

td.options {
  position: relative;
}

.dropbtn {
  background-color: #333;
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px;
  border-radius: 5px;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #333;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: white;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #575757;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown:hover .dropbtn {
  background-color: #575757;
}
</style>
