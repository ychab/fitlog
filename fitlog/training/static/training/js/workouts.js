const vm = new Vue({
  ... baseResourceApp,
  data() {
    return {
      ... baseResourceApp.data(),

      loadingWorkouts: true,
      loadingRoutines: true,
      loadingExercises: true,

      routines: [],
      exercises: [],

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
        this._updatePager(response.data.count)
      })
      .finally(() => this.loadingWorkouts = false)

    axios
      .get('/api/routines/', {
        params: {
          page: 1,
          page_size: 10000  // All
        }
      })
      .then(response => {
        this.routines = response.data.results
      })
      .finally(() => this.loadingRoutines = false)

    axios
      .get('/api/exercises/', {
        params: {
          page: 1,
          page_size: 10000,  // All
        }
      })
      .then(response => {
        this.exercises = response.data.results
      })
      .finally(() => this.loadingExercises = false)
  },
  methods: {
    ... baseResourceApp.methods,

    _collectUpdateFieldValues(resource) {
      // @FIXME for relation, didn't find a better way to remove extra data...
      // @TODO - to fix it, do like in training "component": ust returns ID from
      //  back and add method helper to found item name...
      let postData = {}

      for (const fieldName in this.resourceFields) {
        let value = resource[fieldName]

        switch (fieldName) {

          case 'routine':
            postData[fieldName] = value.id
            break;

          case 'workout_exercises':
            postData[fieldName] = value
            // Special handling for related object... Override by ID only.
            for (const index in resource[fieldName]) {
              postData[fieldName][index]['exercise'] = resource[fieldName][index].exercise.id
            }
            break;

          default:
            postData[fieldName] = value
        }
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
      let workoutExercise = this._prepareNewWorkoutExercise()
      workoutExercise.order = this.newResource.workout_exercises.length
      this.newResource.workout_exercises.push(workoutExercise)
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
          this.modalMessages = {}
          this.refresh()
        })
        .catch(error => {
          this.modalMessages = this.messages
          this.messages = {}  // @todo, yes ugly fix I know!!
        })
        .finally(() => this.creating = false)
    },
    updateResource(resource) {
      this.updating = resource.id

      axios
        .patch('/api/' + this.resourcePath + '/' + resource.id + '/', this._collectUpdateFieldValues(resource))
        .then(response => {
          $('#modal-update-' + resource.id).modal('hide')
          this.formErrors = {}
          this.modalMessages = {}
          this.refresh()
        })
        .catch(error => {
          this.modalMessages = this.messages
          this.messages = {}  // @todo, yes ugly fix I know!!
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

$('#modal-create-resource').on('hidden.bs.modal', function (e) {
  vm.$root.closeModal();
})

// @todo - fixme for edit modal, dynamically added and thus, cannot be bind...