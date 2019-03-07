let app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data() {
    return {
      messages: {},
      loading: true,
      routines: [],
      new_routine: {
        name: null
      },
      pending_adding: false,
      pending_update: 0
    }
  },
  created() {
    axios.defaults.headers.common['X-CSRFToken'] = this.$cookies.get('csrftoken')

    axios.interceptors.response.use(null, (error) => {
      let messages = []

      if (error.response.status == 400) {
        for (const field in error.response.data) {
          let msgs = error.response.data[field]
          for (let msg of msgs) {
            messages.push({type: 'danger', text: field + ' : ' + msg})
          }
        }
      } else {
        messages.push({type: 'danger', text: gettext('Oups... Looks like an error occured :/')})
      }

      this.messages = messages
      console.log(error)

      return Promise.reject(error)
    })
  },
  mounted() {
    axios
      .get('/api/routines/')
      .then(response => {
        this.routines = response.data.results
      })
      .finally(() => this.loading = false)
  },
  methods: {
    refreshRoutines: function () {
      axios
        .get('/api/routines/')
        .then(response => {
          this.routines = response.data.results
        })
    },
    createRoutine: function (routine) {
      this.pending_adding = true

      axios
        .post('/api/routines/', {
          name: routine.name
        })
        .then(response => {
          this.new_routine = {
            name: null
          }
          this.refreshRoutines()
        })
        .finally(() => this.pending_adding = false)
    },
    updateRoutine: function (routine) {
      this.pending_update = routine.id

      axios
        .patch('/api/routines/' + routine.id + '/', {
          name: routine.name
        })
        .finally(() => this.pending_update = 0)
    },
    deleteRoutine: function (routine) {
      axios
        .delete('/api/routines/' + routine.id + '/')
        .then(response => {
          $('#modal-delete-' + routine.id).modal('hide')
          this.refreshRoutines()
        })
    }
  }
})
