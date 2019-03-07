const workoutModel = {
  name: null,
  routine: null,
  exercises: [],
}
const newWorkout = {...workoutModel}

let app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app',
  data() {
    return {
      messages: {},

      loadingWorkout: true,
      loadingRoutines: true,
      loadingExercises: true,

      workouts: [],
      routines: [],
      exercises: [],

      newWorkout,
      pendingAdd: false,
      pendingUpdate: 0
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
      .get('/api/workouts/')
      .then(response => {
        this.workouts = response.data.results
      })
      .finally(() => this.loadingWorkout = false)

    axios
      .get('/api/routines/')
      .then(response => {
        this.routines = response.data.results
      })
      .finally(() => this.loadingRoutines = false)

    axios
      .get('/api/exercises/')
      .then(response => {
        this.exercises = response.data.results
      })
      .finally(() => this.loadingExercises = false)
  },
  methods: {
    refreshWorkouts: function () {
      axios
        .get('/api/workouts/')
        .then(response => {
          this.workouts = response.data.results
        })
    },
    resetWorkoutModel() {
      this.new_workout = {
        name: null,
        routine: null,
        exercises: [],
      }
    },
    createWorkout: function (workout) {
      this.pendingAdd = true

      axios
        .post('/api/workouts/', {
          name: workout.name,
          routine: workout.routine,
          exercises: workout.exercises,
        })
        .then(response => {
          this.resetWorkoutModel()
          this.refreshWorkouts()
        })
        .finally(() => this.pendingAdd = false)
    },
    updateWorkout: function (workout) {
      this.pendingUpdate = workout.id

      axios
        .patch('/api/workouts/' + workout.id + '/', {
          name: workout.name
        })
        .finally(() => this.pendingUpdate = 0)
    },
    deleteWorkout: function (workout) {
      axios
        .delete('/api/workouts/' + workout.id + '/')
        .then(response => {
          $('#modal-delete-' + workout.id).modal('hide')
          this.refreshWorkouts()
        })
    }
  }
})
