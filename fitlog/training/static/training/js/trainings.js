const vm = new Vue({
  ... baseResourceApp,
  data() {
    return {
      ... baseResourceApp.data(),

      loadingTrainings: true,
      loadingExercises: true,
      loadingWorkouts: true,

      resourcePath: 'trainings',
      resourceFields: {
        date: {
          type: 'date',
          default: null,
        },
        workout: {
          type: 'int',
          default: null
        },
        training_exercises: {
          type: 'array',
          default: []
        }
      },
      
      exercises: [],
      workouts: [],

      newResource: null,
      exerciseSelector: null,
      exerciseChoices: null,
      trainingExerciseFields: {
        exercise: {
          type: 'int',
          default: null
        },
        training_exercise_sets: {
          type: 'array',
          default: []
        }
      },
      trainingExerciseSetFields: {
        order: {
          type: 'int',
          default: null
        },
        reps: {
          type: 'int',
          default: 10
        },
        weight: {
          type: 'int',
          default: null
        },
        rest_period: {
          type: 'int',
          default: 90
        },
      }
    }
  },
  mounted() {
    this.reset()

    axios
      .get('/api/trainings/')
      .then(response => {
        this.resources = response.data.results
        this._updatePager(response.data.count)
      })
      .finally(() => this.loadingTrainings = false)

    axios
      .get('/api/exercises/')
      .then(response => {
        this.exercises = response.data.results
      })
      .finally(() => this.loadingExercises = false)

    axios
      .get('/api/workouts/')
      .then(response => {
        this.workouts = response.data.results
      })
      .finally(() => this.loadingWorkouts = false)
  },
  methods: {
    ... baseResourceApp.methods,

    getExerciseName(exerciseId) {
      let exerciseName = null
      for (let exercise of this.exercises) {
        if (exercise.id == exerciseId) {
          exerciseName = exercise.name
          break
        }
      }
      return exerciseName
    },
    getWorkoutName(workoutId) {
      let workoutName = null
      for (let workout of this.workouts) {
        if (workout.id == workoutId) {
          workoutName = workout.name
          break
        }
      }
      return workoutName
    },

    _prepareTrainingExercise() {
      let newExercise = {}
      for (const fieldName in this.trainingExerciseFields) {
        let field = this.trainingExerciseFields[fieldName]
        if (field.type === 'array') {
          newExercise[fieldName] = []
        } else {
          newExercise[fieldName] = field.default
        }
      }
      return newExercise
    },
    addTrainingExercise(resource, exerciseId) {
      let exerciseName = this.getExerciseName(exerciseId)

      if (!exerciseId || !exerciseName) {
        this.formErrors = {
          'exerciseSelector': [gettext('Please select an exercise')]
        }
      } else {
        let trainingExercise = this._prepareTrainingExercise()
        trainingExercise.exercise = exerciseId
        resource.training_exercises.push(trainingExercise)

        delete this.exerciseChoices[exerciseId]

        this.exerciseSelector = null
        this.formErrors = {}
      }
    },
    removeTrainingExercise(resource, key) {
      let exerciseId = resource.training_exercises[key].exercise
      vm.$set(this.exerciseChoices, exerciseId, this.getExerciseName(exerciseId))
      vm.$delete(resource.training_exercises, key)
      this.formErrors = {}
    },

    _getTrainingExerciseIndex(resource, exerciseId) {
      let trainingExerciseIndex = null
      for (let i in resource.training_exercises) {
        let trainingExercise = resource.training_exercises[i]
        if (trainingExercise.exercise === exerciseId) {
          trainingExerciseIndex = i
          break
        }
      }
      return trainingExerciseIndex
    },
    _prepareTrainingExerciseSet() {
      let newSet = {}
      for (const fieldName in this.trainingExerciseSetFields) {
        let field = this.trainingExerciseSetFields[fieldName]
        newSet[fieldName] = field.default
      }
      return newSet
    },
    addTrainingExerciseSet(resource, exerciseId) {
      let trainingExerciseIndex = this._getTrainingExerciseIndex(resource, exerciseId)
      let set = this._prepareTrainingExerciseSet()
      set.order = resource.training_exercises[trainingExerciseIndex].training_exercise_sets.length + 1
      resource.training_exercises[trainingExerciseIndex].training_exercise_sets.push(set)
    },
    removeTrainingExerciseSet(resource, exerciseId, index) {
      let trainingExerciseIndex = this._getTrainingExerciseIndex(resource, exerciseId)
      resource.training_exercises[trainingExerciseIndex].training_exercise_sets.splice(index, 1)
    },

    workoutSelectorChange(resource) {
      resource.training_exercises = []
      this.exerciseSelector = null
      this._resetExerciseChoices()
      this.formErrors = {}

      // Retrieve the workout object if one selected
      let workout = null
      for (let w of this.workouts) {
        if (w.id == resource.workout) {
          workout = w;
          break;
        }
      }
      // If none selected, reset everything and quit.
      if (!workout) {
        return
      }

      // Otherwise, first order exercises.
      let workout_exercises = []
      for (workout_exercise of workout.workout_exercises) {
        workout_exercises.splice(workout_exercise.order, 0, workout_exercise);
      }

      // Iterate over ordered workout exercises template
      for (let workout_exercise of workout_exercises) {
        // Build the training exercise
        let trainingExercise = this._prepareTrainingExercise()
        trainingExercise['exercise'] = workout_exercise.exercise.id

        // Then for each training exercise, create the sets
        for (let i = 0; i < workout_exercise.sets; i++) {
          trainingExercise.training_exercise_sets.push({
            order: i + 1,
            reps: workout_exercise.reps,
            weight: null,
            rest_period: workout_exercise.rest_period
          })
        }

        resource.training_exercises.push(trainingExercise)
      }
    },

    _resetExerciseChoices() {
      let exerciseChoices = {}
      for (let exercise of this.exercises) {
        exerciseChoices[exercise.id] = exercise.name
      }
      this.exerciseChoices = exerciseChoices
    },
    _resetResource() {
      let newResource = {}
      for (const fieldName in this.resourceFields) {
        let field = this.resourceFields[fieldName]
        newResource[fieldName] = field.default
      }
      newResource.date = dateToday
      newResource.training_exercises = []

      this.newResource = newResource
    },
    reset() {
      this._resetExerciseChoices()
      this._resetResource()
      this.exerciseSelector = null
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
        .patch('/api/' + this.resourcePath + '/' + resource.id + '/', this._collectFieldValues(resource))
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
    },

    // filter() {
    //   this.filtering = true
    //   let params = {}
    //
    //   axios
    //     .get('/api/trainings/', {
    //       params: params
    //     })
    //     .then(response => {
    //       this.resources = response.data.results
    //     })
    //     .finally(() => this.filtering = false)
    // },

    _updatePager(count) {
      this.pager.count = count
      this.pager.current = 1
      this.pager.previous = this.pager.current > 1 ? this.pager.current - 1 : false
      this.pager.next = (this.pager.current * this.pageSize) < this.pager.count ? this.pager.current + 1 : false

      let totalPages = this.pager.count / this.pageSize

      this.pager.pages = []
      // Previous pages
      while (this.pager.current -1 > 0 && (this.pager.pages.length < (this.pager.max / 2))) {
        this.pager.pages.push(this.pager.current - 1)
      }
      // Current page
      this.pager.pages.push(this.pager.current)
      // Next pages
      while (this.pager.current + 1 < totalPages && (this.pager.pages.length < this.pager.max)) {
        this.pager.pages.push(this.pager.current + 1)
      }
    },

    changePage(pageNum) {
      this.paging = true

      axios
        .get('/api/trainings/', {
          params: {
            page: pageNum,
            page_size: this.pageSize
          }
        })
        .then(response => {
          this.resources = response.data.results
          this._updatePager(response.data.count)
        })
        .finally(() => this.paging = false)
    }
  }
})

$('#modal-create-resource').on('hidden.bs.modal', function (e) {
  vm.$root.closeModal();
})

// @todo - fixme for edit modal, dynamically added and thus, cannot be bind...
