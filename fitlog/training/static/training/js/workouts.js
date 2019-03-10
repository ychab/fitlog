const app = new Vue({
  ... baseResourceApp,
  data() {
    return {
      messages: {},
      formErrors: {},
      modalMessages: {},

      loadingWorkout: true,
      loadingRoutines: true,
      loadingExercises: true,

      resources: [],
      routines: [],
      exercises: [],

      creating: false,
      updating: false,
      deleting: false,

      resourcePath: 'workouts',
      resourceFields: {
        name: {
          type: 'string',
          default: ''
        },
        routine: {
          type: 'int',
          default: 0
        },
        // Should be override because too much specific
        workout_exercises: {
          type: 'array',
          default: []
        }
      },

      newResource: null,
      newWorkoutExercises: [],

      workoutExerciseFields: {
        exercise: {
          type: 'int',
          default: 0
        },
        order: {
          type: 'int',
          default: 0
        },
        sets: {
          type: 'int',
          default: 5
        },
        reps: {
          type: 'int',
          default: 10
        },
        rest_period: {
          type: 'int',
          default: 90
        },
      },
    }
  },
  mounted() {
    this.reset()

    axios
      .get('/api/workouts/')
      .then(response => {
        this.resources = response.data.results
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
    _getMessageErrors: baseResourceApp.methods._getMessageErrors,
    _getFormErrors: baseResourceApp.methods._getFormErrors,
    hasFormFieldErrors: baseResourceApp.methods.hasFormFieldErrors,
    refresh: baseResourceApp.methods.refresh,

    _collectFieldValues(resource) {
      let postData = {}
      for (const fieldName in this.resourceFields) {
        postData[fieldName] = resource[fieldName]
      }
      return postData
    },
    _prepareNewWorkoutExercise() {
      let newWorkoutExercise = {}
      for (const fieldName in this.workoutExerciseFields) {
        let field = this.workoutExerciseFields[fieldName]
        newWorkoutExercise[fieldName] = field.default
      }
      return newWorkoutExercise
    },
    reset() {
      let newResource = {}

      for (const fieldName in this.resourceFields) {
        let field = this.resourceFields[fieldName]
        newResource[fieldName] = field.default
      }
      newResource.workout_exercises = []

      this.newResource = newResource
    },
    addWorkoutExercise() {
      this.newResource.workout_exercises.push(this._prepareNewWorkoutExercise())
    },
    removeWorkoutExercise(index) {
      this.newResource.workout_exercises.splice(index, 1)
    },
    createResource(resource) {
      this.creating = true

      axios
        .post('/api/' + this.resourcePath + '/', this._collectFieldValues(resource))
        .then(response => {
          $('#modal-create-resource').modal('hide')
          this.reset()
          this.formErrors = {}
          this.refresh()
        })
        .catch(error => {
          this.modalMessages = this.messages  // @todo, yes ugly fix I know!!
          this.messages = {}  // @todo, yes ugly fix I know!!
          // this.modalMessages = this._getMessageErrors(error)
        })
        .finally(() => this.creating = false)
    },
    updateResource(resource) {
      this.updating = resource.id

      axios
        .patch('/api/' + this.resourcePath + '/' + resource.id + '/', this._collectFieldValues(resource))
        .then(response => {
          this.formErrors = {}
        })
        .finally(() => this.updating = false)
    },
    deleteResource(resource) {
      this.deleting = true

      axios
        .delete('/api/' + this.resourcePath + '/' + resource.id + '/')
        .then(response => {
          $('#modal-delete-' + resource.id).modal('hide')
          this.refresh()
        })
        .finally(() => this.deleting = false)
    }
  }
});
