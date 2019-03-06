var app = new Vue({
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
    axios.defaults.headers.common['X-CSRFToken'] = this.$cookies.get('csrftoken');
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
      this.pending_adding = true;

      axios
        .post('/api/routines/', {
          name: routine.name
        })
        .then(response => {
          this.new_routine = {
            name: null
          };
          this.refreshRoutines();
        })
        .finally(() => this.pending_adding = false)
    },
    updateRoutine: function (routine) {
      this.pending_update = routine.id;

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
          $('#modal-delete-' + routine.id).modal('hide');
          this.refreshRoutines();
        })
    }
  }
});
