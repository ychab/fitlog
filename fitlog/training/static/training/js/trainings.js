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
      newExerciseSelector: null,
      newExerciseChoices: null,
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

    _getExerciceName(exerciseId) {
      let exerciseName = null
      for (let exercise of this.exercises) {
        if (exercise.id == exerciseId) {
          exerciseName = exercise.name
          break;
        }
      }
      return exerciseName
    },

    _prepareNewTrainingExercise() {
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
    addTrainingExercise(exerciseId) {
      let exerciseName = this._getExerciceName(exerciseId)

      if (!exerciseId || !exerciseName) {
        this.formErrors = {
          'newExerciseSelector': [gettext('Please select an exercise')]
        }
      } else {
        let trainingExercise = this._prepareNewTrainingExercise()
        trainingExercise.exercise = exerciseId
        this.newResource.training_exercises.push(trainingExercise)

        delete this.newExerciseChoices[exerciseId]

        this.newExerciseSelector = null
        this.formErrors = {}
      }
    },
    removeTrainingExercise(key) {
      let exerciseId = this.newResource.training_exercises[key].exercise
      vm.$set(this.newExerciseChoices, exerciseId, this._getExerciceName(exerciseId))
      vm.$delete(this.newResource.training_exercises, key)
      this.formErrors = {}
    },

    _getTrainingExerciseIndex(exerciseId) {
      let trainingExerciseIndex = null
      for (let i in this.newResource.training_exercises) {
        let trainingExercise = this.newResource.training_exercises[i]
        if (trainingExercise.exercise === exerciseId) {
          trainingExerciseIndex = i
          break
        }
      }
      return trainingExerciseIndex
    },
    _prepareNewTrainingExerciseSet() {
      let newSet = {}
      for (const fieldName in this.trainingExerciseSetFields) {
        let field = this.trainingExerciseSetFields[fieldName]
        newSet[fieldName] = field.default
      }
      return newSet
    },
    addTrainingExerciseSet(exerciseId) {
      let trainingExerciseIndex = this._getTrainingExerciseIndex(exerciseId)
      let set = this._prepareNewTrainingExerciseSet()
      set.order = this.newResource.training_exercises[trainingExerciseIndex].training_exercise_sets.length + 1
      this.newResource.training_exercises[trainingExerciseIndex].training_exercise_sets.push(set)
    },
    removeTrainingExerciseSet(exerciseId, index) {
      let trainingExerciseIndex = this._getTrainingExerciseIndex(exerciseId)
      this.newResource.training_exercises[trainingExerciseIndex].training_exercise_sets.splice(index, 1)
    },

    workoutSelectorChange() {
      this.newResource.training_exercises = []
      this.newExerciseSelector = null
      this._resetExerciseChoices()
      this.formErrors = {}

      // Retrieve the workout object if one selected
      let workout = null
      for (let w of this.workouts) {
        if (w.id == this.newResource.workout) {
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
        let newTrainingExercise = this._prepareNewTrainingExercise()
        newTrainingExercise['exercise'] = workout_exercise.exercise.id

        // Then for each training exercise, create the sets
        for (let i = 0; i < workout_exercise.sets; i++) {
          newTrainingExercise.training_exercise_sets.push({
            order: i + 1,
            reps: workout_exercise.reps,
            weight: null,
            rest_period: workout_exercise.rest_period
          })
        }

        this.newResource.training_exercises.push(newTrainingExercise)
      }
    },

    _resetExerciseChoices() {
      let exerciseChoices = {}
      for (let exercise of this.exercises) {
        exerciseChoices[exercise.id] = exercise.name
      }
      this.newExerciseChoices = exerciseChoices
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
      this.newExerciseSelector = null
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
})

$('#modal-create-resource').on('hidden.bs.modal', function (e) {
  vm.$root.closeModal();
})
