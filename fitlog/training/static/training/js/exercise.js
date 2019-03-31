const app = new Vue({
  ... baseResourceApp,
  data() {
    return {
      ...baseResourceApp.data(),

      loadingExercises: true,
      loadingMuscles: true,

      resourcePath: 'exercises',
      resourceFields: {
        name: {
          type: 'string',
          default: ''
        },
        muscle: {
          type: 'string',
          default: ''
        }
      },

      muscles: null
    }
  },
  mounted() {
    this.reset()

    axios
      .get('/api/exercises/')
      .then(response => {
        this.resources = response.data.results
        this._updatePager(response.data.count)
      })
      .finally(() => this.loadingExercises = false)

    axios
      .get('/api/exercises/muscles/')
      .then(response => {
        this.muscles = response.data
      })
      .finally(() => this.loadingMuscles = false)
  }
})
