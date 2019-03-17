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
        }
      },
      
      exercises: [],
      workouts: [],

      newResource: null,
      newExerciseSelector: null,
      newExerciseChoices: null,
      newExerciseSets: {},
      trainingSetFields: {
        exercise: {
          type: 'int',
          default: null,
        },
        set: {
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

    // _getFormErrors(error) {
    //   let errors = []
    //   let messages = []
    //
    //   if (error.response.status == 400) {
    //     for (const field in error.response.data) {
    //       if (field !== 'non_field_errors') {
    //         if (field === 'training_sets') {
    //           messages.push({type: 'danger', text: field + ' : ' + msg})
    //         } else {
    //           errors[field] = error.response.data[field]
    //         }
    //       }
    //     }
    //   }
    //
    //   return errors
    // },

    addExerciseSets(exerciseId) {
      let exerciseName = null
      for (let exercise of this.exercises) {
        if (exercise.id == exerciseId) {
          exerciseName = exercise.name
          break;
        }
      }

      if (!exerciseId || !exerciseName) {
        this.formErrors = {
          'newExerciseSelector': [gettext('Please select an exercise')]
        }
      } else {
        // Append new exercise sets
        let newExerciseSets = {... this.newExerciseSets}
        newExerciseSets[exerciseId] = {
          exercise: {
            id: exerciseId,
            name: exerciseName
          },
          sets: []
        }
        // Remove selected exercises for the choice list
        let newExerciseChoices = {... this.newExerciseChoices}
        delete newExerciseChoices[exerciseId]

        this.newExerciseSets = newExerciseSets
        this.newExerciseSelector = null
        this.newExerciseChoices = newExerciseChoices
        this.formErrors = {}
      }
    },
    removeExerciseSets(key) {
      let exercise = this.newExerciseSets[key].exercise

      // Reappend exercise in choices because it was removed from card
      let newExerciseChoices = {... this.newExerciseChoices}
      newExerciseChoices[exercise.id] = exercise.name

      let newExerciseSets = {... this.newExerciseSets}
      delete newExerciseSets[key]

      this.newExerciseSets = newExerciseSets
      this.newExerciseChoices = newExerciseChoices
      this.formErrors = {}
    },

    _prepareNewExerciseSetRow() {
      let newExerciseSetRow = {}

      for (const fieldName in this.trainingSetFields) {
        let field = this.trainingSetFields[fieldName]
        newExerciseSetRow[fieldName] = field.default
      }

      return newExerciseSetRow
    },
    addExerciseSetRow(exerciseId) {
      let row = this._prepareNewExerciseSetRow()
      row.exercise = exerciseId
      row.set = this.newExerciseSets[exerciseId].sets.length + 1
      this.newExerciseSets[exerciseId].sets.push(row)
    },
    removeExerciseSetRow(exerciseId, index) {
      this.newExerciseSets[exerciseId].sets.splice(index, 1)
    },

    workoutSelectorChange() {
      this.newExerciseSelector = null
      this._resetExerciseChoices()
      this.formErrors = {}
      let newExerciseSets = {}

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
        this.newExerciseSets = newExerciseSets
        return
      }

      // Otherwise, first order exercices.
      let workout_exercises = []
      for (workout_exercise of workout.workout_exercises) {
        workout_exercises.splice(workout_exercise.order, 0, workout_exercise);
      }

      // Then build exercises sets, based on the workout exercises
      for (let workout_exercise of workout_exercises) {
        newExerciseSets[workout_exercise.exercise.id] = {
          exercise: {
            id: workout_exercise.exercise.id,
            name: workout_exercise.exercise.name
          },
          sets: []
        }

        for (let i = 0; i < workout_exercise.sets; i++) {
          newExerciseSets[workout_exercise.exercise.id].sets.push({
            exercise: workout_exercise.exercise.id,
            set: i + 1,
            reps: workout_exercise.reps,
            weight: null,
            rest_period: workout_exercise.rest_period
          })
        }
      }

      this.newExerciseSets = newExerciseSets
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
      this.newResource = newResource
    },
    reset() {
      this._resetExerciseChoices()
      this._resetResource()
      this.newExerciseSelector = null
      this.newExerciseSets = {}
    },

    _collectFieldValues(resource) {
      let postData = {}
      for (const fieldName in this.resourceFields) {
        let value = resource[fieldName]
        postData[fieldName] = value
      }

      postData['training_sets'] = []
      for (let key in this.newExerciseSets) {
        for (let set of this.newExerciseSets[key].sets) {
          postData['training_sets'].push({
            exercise: set.exercise,
            set: set.set,
            reps: set.reps,
            weight: set.weight,
            rest_period: set.rest_period
          })
        }
      }

      return postData
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
