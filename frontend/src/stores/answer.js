import { defineStore } from 'pinia'
import { ref } from 'vue'
import Swal from 'sweetalert2'
import http from '../services/http'
import router from '@/router'

export const useAnswerStore = defineStore('answer', () => {
  const toastStack = ref([]) // Stack to keep track of active toasts
  const examId = router.currentRoute.value.params.id

  const toast = Swal.mixin({
    toast: true,
    position: 'bottom-end', // Default position, can be adjusted dynamically
    showConfirmButton: false,
    timer: 500,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  const maxFiles = 10 // Maximum number of files

  const rules = ref([
    (v) => (!!v && v.length > 0) || 'At least one file is required',
    (v) => (v && v.length <= maxFiles) || `You can upload up to ${maxFiles} files only`
  ])
  const files = ref([]) // Note the change to an array since multiple files are allowed

  const form = ref(false)
  async function onSubmit() {
    if (examId === undefined) {
      // Add a new toast to the stack
      toastStack.value.push(
        await toast.fire({
          icon: 'error',
          title: 'Error: Exam ID is missing'
        })
      )
      return
    }
    for (const file of files.value) {
      // console.log(file)
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('id', examId)
        const res = await http.post('/answers/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        fetchAnswers()
        // Add a new toast to the stack
        toastStack.value.push(
          await toast.fire({
            icon: 'success',
            title: `File ${res.filename} uploaded successfully, waiting for grading...`
          })
        )
      } catch (error) {
        console.error(error)
        // Add a new toast to the stack
        toastStack.value.push(
          await toast.fire({
            icon: 'error',
            title: `Error uploading file ${file.name}`
          })
        )
      }
    }
  }

  const columns = ref([
    {
      title: 'Filename',
      key: 'fileName'
    },
    {
      title: 'Status',
      key: 'status'
    },
    {
      title: 'Score',
      key: 'score'
    },
    {
      title: 'Actions',
      key: 'actions',
      sortable: false
    }
  ])

  const answers = ref([])
  async function fetchAnswers() {
    const id = examId
    try {
      const res = await http.get(`/answers/exam/${id}`)
      answers.value = res.data
    } catch (error) {
      console.log(error)
    }
  }

  const dialog = ref(false)
  const selectedFileUrl = ref('')
  function openDialog(url) {
    selectedFileUrl.value = url
    dialog.value = true
  }

  function deleteItem(item) {
    Swal.fire({
      title: 'Are you sure?',
      text: 'You will not be able to recover this file!',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, keep it'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const res = await http.delete(`/answers/${item.id}`)
          if (res.status === 200) {
            Swal.fire({
              title: 'Deleted!',
              text: 'Your file has been deleted.',
              icon: 'success',
              showConfirmButton: false,
              timer: 1500
            })
            fetchAnswers(item.examId)
          }
        } catch (error) {
          console.error(error)
          Swal.fire('Error!', 'An error occurred while deleting the file.', 'error')
        }
      } else if (result.dismiss === Swal.DismissReason.cancel) {
        Swal.fire('Cancelled', 'Your file is safe :)', 'error')
      }
    })
  }
  return {
    maxFiles,
    rules,
    files,
    form,
    onSubmit,
    columns,
    answers,
    fetchAnswers,
    dialog,
    selectedFileUrl,
    openDialog,
    deleteItem
  }
})
