import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import http from '../services/http'
import router from '@/router'
import Swal from 'sweetalert2'

export const useExamStore = defineStore('exam', () => {
  const columns = ref([
    {
      title: 'Topic',
      align: 'start',
      sortable: true,
      key: 'topic'
    },
    {
      title: 'Details',
      key: 'details'
    },
    {
      title: 'Template',
      key: 'anwerssheet_template'
    },
    {
      title: 'Created At',
      key: 'createdAt'
    },
    {
      title: 'Status',
      key: 'status'
    },
    {
      title: 'Actions',
      key: 'actions',
      sortable: false
    }
  ])

  const exams = ref([])
  async function fetchExams() {
    try {
      const res = await http.get('/exams')
      exams.value = res.data
    } catch (error) {
      console.error(error)
    }
  }

  function clearItems() {
    exams.value = []
  }

  const form = ref(false)
  const AddForm = ref({
    topic: '',
    details: '',
    answerssheet_template: 'Multiple Choice'
  })

  const numberOfQuestions = ref(0)
  const questions = ref([])

  // ฟังก์ชันที่จะถูกเรียกเมื่อส่งฟอร์ม
  async function onSubmit() {
    const body = {
      topic: AddForm.value.topic,
      details: AddForm.value.details,
      correctAnswer: JSON.stringify(
        questions.value.map((question) => {
          const correctAnswers = question.options
            .map((option, index) => (option.value ? String.fromCharCode(65 + index) : null))
            .filter((answer) => answer !== null)
          return { [question.id]: correctAnswers }
        })
      ),
      answerssheet_template: AddForm.value.answerssheet_template
    }
    // console.log(body)
    try {
      const res = await http.post('/exams', body)
      // console.log(res)
      if (res.status === 201) {
        // router.push({ name: 'home' })
        Swal.fire({
          title: 'Success!',
          text: 'Exam has been created successfully!',
          icon: 'success',
          confirmButtonText: 'OK'
        }).then(() => {
          router.push({ name: 'home' })
        })
      }
    } catch (error) {
      console.error(error)
    }
  }

  // อัปเดต questions เมื่อจำนวนคำถามเปลี่ยนแปลง
  function updateQuestions() {
    this.questions = Array.from({ length: this.numberOfQuestions }, (_, index) => ({
      id: index + 1,
      options: Array.from({ length: 5 }, (_, i) => ({
        label: String.fromCharCode(65 + i),
        value: false
      }))
    }))
  }

  // ตรวจสอบว่าสามารถส่งฟอร์มได้หรือไม่
  const canSubmit = computed(() => {
    return (
      AddForm.value.topic !== '' &&
      AddForm.value.details !== '' &&
      numberOfQuestions.value > 0 &&
      questions.value.every((question) => question.options.some((option) => option.value))
    )
  })

  function deleteItem(item) {
    Swal.fire({
      title: 'Are you sure?',
      text: 'You will not be able to recover this exam!',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, keep it'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const res = await http.delete(`/exams/${item.id}`)
          if (res.status === 200) {
            Swal.fire('Deleted!', 'Your exam has been deleted.', 'success')
            fetchExams()
          }
        } catch (error) {
          console.error(error)
        }
      } else if (result.dismiss === Swal.DismissReason.cancel) {
        Swal.fire('Cancelled', 'Your exam is safe :)', 'error')
      }
    })
  }

  return {
    columns,
    exams,
    fetchExams,
    clearItems,
    form,
    AddForm,
    numberOfQuestions,
    questions,
    onSubmit,
    updateQuestions,
    canSubmit,
    deleteItem
  }
})
