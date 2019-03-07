const newItemTemplate = {
  name: null
}

const objVue = {... baseVueApp, itemResource: 'exercises', newItemTemplate: newItemTemplate}

let app = new Vue(objVue);

// let app = new Vue({
//   delimiters: ['[[', ']]'],
//   el: '#app',
//   data () {
//     return {
//       messages: {},
//       loading: true,
//       exercises: [],
//       new_exercise: {
//         name: null
//       },
//       pending_adding: false,
//       pending_update: 0
//     }
//   },
//   created() {
//     axios.defaults.headers.common['X-CSRFToken'] = this.$cookies.get('csrftoken')
//
//     axios.interceptors.response.use(null, (error) => {
//       let messages = []
//
//       if (error.response.status == 400) {
//         for (const field in error.response.data) {
//           let msgs = error.response.data[field]
//           for (let msg of msgs) {
//             messages.push({type: 'danger', text: field + ' : ' + msg})
//           }
//         }
//       } else {
//         messages.push({type: 'danger', text: gettext('Oups... Looks like an error occured :/')})
//       }
//
//       this.messages = messages
//       console.log(error)
//
//       return Promise.reject(error)
//     })
//   },
//   mounted() {
//     axios
//       .get('/api/exercises/')
//       .then(response => {
//         this.exercises = response.data.results
//       })
//       .finally(() => this.loading = false)
//   },
//   methods: {
//     refreshExercises: function () {
//       axios
//         .get('/api/exercises/')
//         .then(response => {
//           this.exercises = response.data.results
//         })
//     },
//     createExercise: function (exercise) {
//       this.pending_adding = true
//
//       axios
//         .post('/api/exercises/', {
//           name: exercise.name
//         })
//         .then(response => {
//           this.new_exercise = {
//             name: null
//           }
//           this.refreshExercises()
//         })
//         .finally(() => this.pending_adding = false)
//     },
//     updateExercise: function (exercise) {
//       this.pending_update = exercise.id
//
//       axios
//         .patch('/api/exercises/' + exercise.id + '/', {
//           name: exercise.name
//         })
//         .finally(() => this.pending_update = 0)
//     },
//     deleteExercise: function (exercise) {
//       axios
//         .delete('/api/exercises/' + exercise.id + '/')
//         .then(response => {
//           $('#modal-delete-' + exercise.id).modal('hide')
//           this.refreshExercises()
//         })
//     }
//   }
// })
